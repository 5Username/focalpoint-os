# Redis Rate Limiting (Production Recommendation)

The current rate limiter is an **in-memory** implementation.  
It works for single-process demos but is **not suitable** for multi-worker or multi-server deployments.

## Why Redis?

- Shared state across all workers / containers
- Atomic increments and expirations
- Battle-tested for rate limiting patterns

## Recommended approach

### 1. Add Redis to Docker Compose

```yaml
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    restart: unless-stopped
```

### 2. Install dependency

```bash
pip install redis
```

### 3. Example Redis rate limiter

```python
import redis
from time import time
from fastapi import Request, HTTPException

r = redis.Redis(host="redis", port=6379, decode_responses=True)

async def redis_rate_limit(request: Request, max_requests: int = 20, window: int = 60):
    client = request.client.host if request.client else "unknown"
    key = f"rl:{client}:{request.url.path}"
    pipe = r.pipeline()
    pipe.incr(key)
    pipe.expire(key, window)
    results = pipe.execute()
    count = results[0]
    if count > max_requests:
        raise HTTPException(status_code=429, detail="Too many requests")
```

### 4. Alternative libraries

- `slowapi` (very popular with FastAPI)
- `fastapi-limiter`

### 5. Production tips

- Rate-limit by IP **and** by user ID when authenticated
- Use stricter limits on `/login`, `/register`, `/password-reset`
- Return `Retry-After` header when possible
- Monitor 429 rates in your observability stack

---

The current in-memory limiter is intentionally simple so the project runs with zero extra infrastructure.  
Replace it with Redis before going to multi-instance production.
