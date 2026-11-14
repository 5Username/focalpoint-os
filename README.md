# FocalPoint OS

**Professional toolkit for NGO Security Focal Points (SFPs) in Kenya, East Africa and humanitarian contexts worldwide.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://python.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-blue.svg)](https://www.typescriptlang.org/)
[![Docker](https://img.shields.io/badge/Docker-one--click-blue.svg)](docker-compose.yml)
[![PWA](https://img.shields.io/badge/PWA-Offline%20Capable-green.svg)](#)
[![i18n](https://img.shields.io/badge/i18n-EN%20%7C%20SW%20%7C%20FR%20%7C%20AR-purple.svg)](#)

> Built for real field conditions — low bandwidth, intermittent connectivity, and busy Security Focal Points who need clean, professional outputs fast.

---

## Why FocalPoint OS?

NGO Security Focal Points are time-poor. They need:

- Fast weekly situation overviews from **public sources only**
- Clean travel risk decisions they can share with management
- Simple incident logging that actually works **offline**

Most tools are either too heavy or too basic. This one is designed to be practical.

---

## Core Modules

| Module | Purpose | Typical Price (Kenya) |
|--------|---------|-----------------------|
| **Weekly Security Brief** | Structured brief from ethical public OSINT | KES 3,000–5,000 / month |
| **Travel Risk Pack** | One-page go / no-go checklist | KES 1,000 per pack |
| **Offline Incident Logger** | Field form → Google Sheets sync | KES 5,000 setup + 2,000/month |

---

## Key Features

- **Multi-language** (English, Kiswahili, French, Arabic) — ready for international NGOs & humanitarian teams
- **One-click Docker** setup
- **Offline-first** Incident module (Service Worker + local queue)
- **Ethical public OSINT** layer (attribution required, no private data)
- **PDF-ready** outputs (browser Print → Save as PDF)
- **Google Sheets** integration path
- Clean TypeScript + Python architecture
- Mobile-first, field-friendly UI

---

## Quick Start (One Command)

```bash
git clone https://github.com/5Username/focalpoint-os.git
cd focalpoint-os
docker compose up --build
```

Then open:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000

See `docs/DEPLOY.md` for manual setup and GitHub Pages instructions.

---

## Language Support

| Code | Language |
|------|----------|
| `en` | English |
| `sw` | Kiswahili |
| `fr` | Fran\u00e7ais |
| `ar` | \u0627\u0644\u0639\u0631\u0628\u064a\u0629 |

Ideal for organisations working across East Africa, Francophone Africa and the Middle East / North Africa.

---

## Ethical OSINT Approach

- Only publicly available sources
- Clear attribution
- No login walls, no private APIs without consent
- Designed for coordination and research, **not** licensed intelligence products

---

## Project Structure

```
focalpoint-os/
├── backend/          # Python FastAPI + ethical OSINT services
├── frontend/         # TypeScript + React + PWA + i18n
├── samples/          # Professional example outputs
├── docs/             # Architecture + Deploy guides
├── docker-compose.yml
└── README.md
```

---

## Roadmap

- [x] Multi-language support (EN / SW / FR / AR)
- [x] One-click Docker
- [x] Offline PWA + queue
- [x] Ethical OSINT service layer
- [x] Professional sample outputs
- [x] Google Sheets path
- [ ] Full PDF generation service
- [ ] More public source connectors (ReliefWeb, etc.)
- [ ] Multi-tenant NGO workspaces

---

## Disclaimer

FocalPoint OS is a **research and coordination tool**. It structures publicly available information. It does **not** provide licensed security advice, formal risk certification, or intelligence products.

---

## License

MIT

Built for humanitarian and NGO field reality.
