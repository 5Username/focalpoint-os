# FocalPoint OS — Production Deployment Checklist

Use this checklist before putting FocalPoint OS into production for real NGO clients.

## 1. Secrets & Configuration

- [ ] Set a strong `SECRET_KEY` (long random string)
- [ ] Configure real `DATABASE_URL` (Postgres recommended)
- [ ] Configure SMTP settings for email:
  - `SMTP_HOST`
  - `SMTP_PORT`
  - `SMTP_USER`
  - `SMTP_PASSWORD`
  - `SMTP_FROM`
- [ ] Change default Postgres password in `docker-compose.yml`
- [ ] Never commit `.env` files or credentials

## 2. Database

- [ ] Use Postgres in production (not SQLite)
- [ ] Enable automated backups
- [ ] Consider adding Alembic for formal schema migrations
- [ ] Test restore procedure

## 3. Security

- [ ] Serve only over HTTPS
- [ ] Set secure CORS origins (replace `allow_origins=["*"]`)
- [ ] Rotate API keys periodically
- [ ] Enforce strong passwords (already minimum 6 characters — consider increasing)
- [ ] Enable email verification before full access if required by policy
- [ ] Review audit logs regularly
- [ ] Rate-limit authentication endpoints (recommended)

## 4. Email

- [ ] Test registration verification emails
- [ ] Test password reset emails
- [ ] Test weekly brief HTML emails
- [ ] Test workspace invite emails
- [ ] Use a reputable transactional email provider (SendGrid, Mailgun, Amazon SES, etc.)

## 5. Application

- [ ] Run with a production process manager (systemd, Docker, Kubernetes)
- [ ] Put a reverse proxy in front (Nginx / Caddy / Traefik)
- [ ] Enable health checks (`/health`)
- [ ] Set up monitoring and alerting
- [ ] Configure log rotation

## 6. Frontend

- [ ] Build the frontend for production (`npm run build`)
- [ ] Serve static files via CDN or reverse proxy
- [ ] Update API base URL to production backend
- [ ] Test offline incident logging on real mobile devices

## 7. Legal & Operational

- [ ] Confirm the disclaimer is visible (research & coordination tool only)
- [ ] Document data retention policy
- [ ] Ensure staff understand this is **not** licensed security advice
- [ ] Define support / escalation process for NGO clients

## 8. Go-live smoke test

- [ ] Register a new user
- [ ] Verify email
- [ ] Create a workspace
- [ ] Invite a member
- [ ] Generate a weekly brief + PDF
- [ ] Generate a travel risk pack + PDF
- [ ] Log an offline incident and sync
- [ ] Confirm scheduled brief email arrives
- [ ] Check analytics dashboard and audit log

---

**Recommended stack for production**

- Backend: FastAPI + Uvicorn/Gunicorn behind Nginx
- Database: Postgres 16
- Cache / queue (future): Redis
- Email: transactional provider
- Frontend: static build served by Nginx or Vercel/Netlify
- Containers: Docker Compose or Kubernetes
