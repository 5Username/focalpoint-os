# FocalPoint OS Architecture

## Design Principles
1. **Offline-first** where it matters (Incident logging)
2. **Low bandwidth** friendly
3. **Modular** — each module can be used independently
4. **Professional output** — something an SFP can send to Country Director without embarrassment
5. **Multi-language codebase** for quality and maintainability

## Backend (Python + FastAPI)
- Clear routers per module
- Pydantic models for validation
- Ready for Google Sheets service account integration
- Easy to extend with real OSINT collectors

## Frontend (TypeScript + React + Vite + Tailwind)
- Fast, modern, type-safe
- PWA-ready structure for offline capability
- Mobile-first (field staff use phones)

## Future
- Service Worker + IndexedDB for full offline incident queue
- Real public OSINT connectors (with rate limiting and source attribution)
- PDF generation for Travel Risk Packs and Weekly Briefs
- Multi-tenant support for different NGOs
