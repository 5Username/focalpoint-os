# FocalPoint OS

**Advanced toolkit for NGO Security Focal Points (SFPs) in Kenya, East Africa and humanitarian contexts worldwide.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://python.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-blue.svg)](https://www.typescriptlang.org/)
[![Docker](https://img.shields.io/badge/Docker-one--click-blue.svg)](docker-compose.yml)
[![PWA](https://img.shields.io/badge/PWA-Offline%20Capable-green.svg)](#)
[![i18n](https://img.shields.io/badge/i18n-EN%20%7C%20SW%20%7C%20FR%20%7C%20AR-purple.svg)](#)

> Built for real field conditions — low bandwidth, intermittent connectivity, and busy Security Focal Points who need clean, professional outputs fast.

---

## Core Capabilities

| Module | Description |
|--------|-------------|
| **Weekly Security Briefs** | Structured briefs from ethical public OSINT + PDF export |
| **Travel Risk Packs** | One-page go/no-go checklists + PDF |
| **Offline Incident Logger** | Field form that works offline → Google Sheets path |
| **Crisis Overview + Map** | Humanitarian context with Leaflet map |
| **Multi-tenant Workspaces** | Separate NGO workspaces with own settings |
| **GeoJSON Export** | Download illustrative public hotspot data |
| **Brief Scheduling** | Configure automated weekly brief generation |
| **Multi-language** | English • Kiswahili • Français • العربية |

---

## Quick Start (One Command)

```bash
git clone https://github.com/5Username/focalpoint-os.git
cd focalpoint-os
docker compose up --build
```

- Frontend: http://localhost:5173
- Backend:  http://localhost:8000
- API docs: http://localhost:8000/docs

See `docs/DOCKER.md` and `docs/ADVANCED.md` for full details.

---

## Advanced Features

- **Multi-tenant NGO workspaces** — each organisation can have its own space and settings
- **Automated weekly brief scheduling** — configure day/time per workspace
- **GeoJSON export** of illustrative public hotspot data
- **Leaflet map** on the Crisis module
- **Server-side PDF generation** (ReportLab)
- **Ethical public OSINT** layer with attribution

---

## Disclaimer

FocalPoint OS is a **research and coordination tool**. It structures publicly available information. It does **not** provide licensed security advice, formal risk certification, or intelligence products.

---

## License

MIT

Built for humanitarian and NGO field reality.
