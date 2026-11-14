# Authentication Guide

FocalPoint OS supports two authentication methods:

## 1. User Login (JWT) — Primary

### Register
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "you@ngo.org", "password": "secret123", "full_name": "Jane Doe"}'
```

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=you@ngo.org&password=secret123"
```

Use the returned `access_token` as:
```
Authorization: Bearer <token>
```

### Current user
```bash
curl http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer <token>"
```

## 2. API Key (Workspace) — Machine access

Still supported for automation and scheduled jobs.

```
X-API-Key: fp_xxxxxxxxxxxx
```

API keys are created automatically when you create a workspace.
