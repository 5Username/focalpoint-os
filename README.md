# FocalPoint OS

**Professional toolkit for NGO Security Focal Points (SFPs) in Kenya & East Africa.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-blue.svg)](https://www.typescriptlang.org/)
[![PWA Ready](https://img.shields.io/badge/PWA-Offline%20Capable-green.svg)](#)

> Built for real field conditions — low bandwidth, intermittent connectivity, and busy Security Focal Points who need clean outputs fast.

---

## The Problem
NGO Security Focal Points are time-poor. They need:
- Fast weekly situation overviews
- Clean travel risk decisions
- Simple incident logging that works offline

Most tools are either too heavy or too basic. FocalPoint OS is designed to be practical.

---

## Three Core Modules

| Module | What it does | Pricing (Kenya) |
|--------|--------------|-----------------|
| **Weekly Security Brief** | Structured brief from public sources | KES 3,000–5,000 / month |
| **Travel Risk Pack** | One-page go / no-go checklist | KES 1,000 per pack |
| **Offline Incident Logger** | Field form → Google Sheets sync | KES 5,000 setup + 2,000/month |

---

## Features

- **Multi-language architecture**: Python (FastAPI) + TypeScript (React + Vite + Tailwind)
- **Offline-first Incident module** (Service Worker + local queue)
- **Google Sheets ready** (service account + OAuth path)
- Clean, professional outputs suitable for Country Directors and donors
- Mobile-first design
- Clear separation between research/coordination and licensed advice

---

## Quick Start

### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

---

## Project Structure

```
focalpoint-os/
├── backend/               # Python FastAPI
│   ├── app/
│   │   ├── routers/       # briefs, travel, incidents
│   │   └── services/      # Google Sheets, OSINT stubs
│   └── requirements.txt
├── frontend/              # TypeScript + React + PWA
│   ├── src/
│   │   ├── pages/         # Briefs, Travel, Incidents
│   │   ├── components/
│   │   └── lib/           # offline queue, api
│   ├── public/            # manifest + service worker
│   └── ...
├── samples/               # Professional example outputs
├── docs/
└── README.md
```

---

## Sample Outputs

See the `/samples` folder for:
- Example Weekly Security Brief (Markdown)
- Example Travel Risk Pack (one-page style)

These are designed to look professional enough to forward internally.

---

## Roadmap

- [x] Clean multi-language architecture
- [x] Full frontend modules
- [x] Offline PWA support for incidents
- [x] Google Sheets service layer
- [x] Professional sample outputs
- [ ] Real public OSINT connectors (with attribution)
- [ ] PDF export for briefs & travel packs
- [ ] Multi-NGO tenancy
- [ ] Kiswahili interface option

---

## Disclaimer

FocalPoint OS is a **research and coordination tool**. It compiles and structures publicly available information. It does **not** constitute licensed security advice, risk assessment certification, or formal intelligence product.

---

## License

MIT

Built for field reality in Kenya and East Africa.
