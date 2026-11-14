# FocalPoint OS

**Professional toolkit for NGO Security Focal Points (SFPs) in Kenya & East Africa.**

Three core modules in one clean, modular system:

1. **Weekly Security Brief Generator**  
   Automated collection of public OSINT sources + clean formatting for busy SFPs.  
   Price target: KES 3,000–5,000 / month per NGO.

2. **Travel Risk Pack Compiler**  
   One-page branded go/no-go checklist for any destination using public risk data.  
   Price: KES 1,000 per pack.

3. **Offline Incident Report System**  
   Field-ready form that works without internet, then syncs to Google Sheets.  
   Setup: KES 5,000 + KES 2,000/month.

---

## Why this exists
NGO Security Focal Points are often stretched thin. They need fast, reliable, low-bandwidth tools that actually work in the field — not another heavy dashboard.

FocalPoint OS is designed for:
- Low connectivity environments
- Rapid briefing generation
- Simple field incident logging
- Clear, professional outputs that can be shared with management or donors

> This is a research & coordination tool only. It does not provide licensed security advice.

---

## Architecture (Multi-language by design)

```
focalpoint-os/
├── backend/          # Python (FastAPI)
│   ├── app/
│   ├── services/      # OSINT collectors, risk compilers, sheet sync
│   └── ...
├── frontend/         # TypeScript + Vite + Tailwind (PWA ready)
├── shared/           # Types & schemas (TypeScript + Python models)
├── scripts/          # CLI tools & automation
├── docs/
└── docker/           # Easy local + production deploy
```

**Languages & Tech intentionally mixed for quality + stars:**
- **Python** — Backend, OSINT, data processing, Google Sheets
- **TypeScript** — Modern frontend + type safety
- **HTML/CSS/JS** — Offline-capable PWA core
- **Shell + Docker** — Deployment & automation
- **Markdown + JSON** — Configuration & briefs

---

## Quick Start (Development)

```bash
# Backend
cd backend
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

---

## Modules Overview

### 1. Weekly Security Brief
- Pulls from public sources (news, government advisories, open threat intel)
- Structures into clean weekly format
- Export as Markdown / PDF / email-ready
- Designed for SFPs who only have 15 minutes on Monday morning

### 2. Travel Risk Pack
- Input: Destination + travel dates + organization profile
- Output: One-page branded checklist (go / no-go / mitigate)
- Sources: Public travel advisories, crime stats, health, political risk

### 3. Offline Incident Logger
- Works fully offline (Service Worker + local storage)
- Syncs to Google Sheet when connection returns
- Simple form optimized for field staff on phones
- Categories: Security, Medical, Logistics, Safeguarding, Other

---

## Roadmap for High GitHub Visibility
- [x] Clean modular architecture
- [ ] Full offline PWA for Incident module
- [ ] Sample weekly brief templates (Kenya + regional)
- [ ] Google Sheets OAuth + service account support
- [ ] CLI for bulk Travel Risk Packs
- [ ] Docker Compose one-command deploy
- [ ] Contribution guide + good first issues
- [ ] Example outputs that look professional

---

## License
MIT — use it, improve it, deploy it for your NGO.

Built for real field work in Kenya and East Africa.
