# FocalPoint OS

**Advanced multi-tenant toolkit for NGO Security Focal Points in Kenya, East Africa and humanitarian contexts.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-one--click-blue.svg)](docker-compose.yml)
[![i18n](https://img.shields.io/badge/i18n-EN%20%7C%20SW%20%7C%20FR%20%7C%20AR-purple.svg)](#)

> Built for real field conditions — low bandwidth, intermittent connectivity, and busy Security Focal Points.

---

## Key Capabilities

- Weekly Security Briefs (ethical public OSINT) + PDF + HTML email
- Travel Risk Packs (go / no-go) + PDF
- Offline Incident Logger (PWA)
- Crisis Overview with map layers, polygons and heatmap
- Multi-tenant NGO Workspaces
- User registration, login (JWT), email verification, password reset
- Workspace invite links
- Role-based access (owner / admin / member / viewer)
- API keys for automation
- Background scheduler for weekly briefs
- Analytics dashboard + audit log
- SQLite (default) or Postgres
- Multi-language UI (English, Kiswahili, French, Arabic)
- One-click Docker Compose

---

## Quick Start

```bash
git clone https://github.com/5Username/focalpoint-os.git
cd focalpoint-os
docker compose up --build
```

- Frontend: http://localhost:5173
- Backend:  http://localhost:8000
- API docs: http://localhost:8000/docs

---

## Documentation

- `docs/PRODUCTION.md` — Production deployment checklist
- `docs/AUTH.md` — Authentication guide
- `docs/POSTGRES.md` — Postgres setup
- `docs/INVITES.md` — Workspace invite links
- `docs/DOCKER.md` — Docker instructions
- `docs/ADVANCED.md` — Advanced features

---

## Disclaimer

FocalPoint OS is a **research and coordination tool**. It structures publicly available information. It does **not** provide licensed security advice, formal risk certification, or intelligence products.

---

## License

MIT
