# Deploy FocalPoint OS on Railway + Vercel

This guide gets the full system live.

## 1. Backend on Railway

1. Go to [https://railway.app](https://railway.app) and sign in with GitHub.
2. Click **New Project**.
3. Choose **Deploy from GitHub repo**.
4. Select the repository `focalpoint-os`.
5. Railway will detect the project. You may need to set the root directory to `backend` or use the Dockerfile.

### Add databases

- Click **+ New** → **Database** → **Add PostgreSQL**
- Click **+ New** → **Database** → **Add Redis**

### Environment Variables (Backend service)

Set these in the Backend service:

```
SECRET_KEY=generate-a-long-random-string-here
DATABASE_URL=${{Postgres.DATABASE_URL}}
REDIS_URL=${{Redis.REDIS_URL}}
OAUTH_REDIRECT_BASE=https://your-backend-name.up.railway.app
FRONTEND_URL=https://your-frontend.vercel.app
```

Optional (if you have them):
```
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
SMTP_HOST=...
SMTP_PORT=587
SMTP_USER=...
SMTP_PASSWORD=...
SMTP_FROM=...
```

### Important

- Make sure the backend service is using the `backend` folder (or the Dockerfile inside it).
- After deployment Railway will give you a public URL, for example:
  `https://focalpoint-os-production.up.railway.app`

Copy that URL — you will need it for the frontend.

---

## 2. Frontend on Vercel

1. Go to [https://vercel.com](https://vercel.com) and sign in with GitHub.
2. Click **Add New Project** → Import the same `focalpoint-os` repository.
3. Configure:
   - **Root Directory**: `frontend`
   - Framework Preset: Vite
4. Add Environment Variable:

```
VITE_API_URL=https://your-backend-name.up.railway.app
```

(Replace with the real Railway URL you got in step 1)

5. Click **Deploy**.

After a minute you will get a URL like:
`https://focalpoint-os.vercel.app`

---

## 3. Final connection

- Update `FRONTEND_URL` on Railway to your Vercel URL.
- Update `OAUTH_REDIRECT_BASE` if you are using Google login.
- In Google Cloud Console, add the callback URL:
  `https://your-backend.up.railway.app/api/oauth/google/callback`

---

## Quick Test

1. Open your Vercel URL
2. Register a new account
3. Create a workspace
4. Generate a brief

If something fails, check the Railway logs and the browser console.
