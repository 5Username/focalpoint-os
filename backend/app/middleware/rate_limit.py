"""
Simple in-memory rate limiter for auth endpoints.
For production, replace with Redis-based limiting.
"""

from time import time
from collections import defaultdict
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int = 20, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window = window_seconds
        self.hits = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        # Only rate-limit auth routes
        path = request.url.path
        if path.startswith("/api/auth/"):
            client = request.client.host if request.client else "unknown"
            key = f"{client}:{path}"
            now = time()
            # Drop old hits
            self.hits[key] = [t for t in self.hits[key] if now - t < self.window]
            if len(self.hits[key]) >= self.max_requests:
                raise HTTPException(status_code=429, detail="Too many requests. Please try again later.")
            self.hits[key].append(now)
        return await call_next(request)
