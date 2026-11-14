"""
Redis-backed rate limiter with in-memory fallback.
"""

from time import time
from collections import defaultdict
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import os
import logging

logger = logging.getLogger("focalpoint.ratelimit")

try:
    import redis
    REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
    redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True, socket_connect_timeout=1)
    # Test connection
    redis_client.ping()
    USE_REDIS = True
    logger.info("Rate limiter using Redis")
except Exception as e:
    redis_client = None
    USE_REDIS = False
    logger.warning(f"Redis unavailable ({e}) — falling back to in-memory rate limiter")

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int = 20, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window = window_seconds
        self.hits = defaultdict(list)  # fallback store

    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        if not path.startswith("/api/auth/") and not path.startswith("/api/oauth/"):
            return await call_next(request)

        client = request.client.host if request.client else "unknown"
        key = f"rl:{client}:{path}"

        if USE_REDIS and redis_client:
            try:
                pipe = redis_client.pipeline()
                pipe.incr(key)
                pipe.expire(key, self.window)
                count, _ = pipe.execute()
                if count > self.max_requests:
                    raise HTTPException(status_code=429, detail="Too many requests. Please try again later.")
            except HTTPException:
                raise
            except Exception as e:
                logger.warning(f"Redis rate limit error: {e} — allowing request")
        else:
            # In-memory fallback
            now = time()
            self.hits[key] = [t for t in self.hits[key] if now - t < self.window]
            if len(self.hits[key]) >= self.max_requests:
                raise HTTPException(status_code=429, detail="Too many requests. Please try again later.")
            self.hits[key].append(now)

        return await call_next(request)
