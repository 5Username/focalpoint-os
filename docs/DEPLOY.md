# Deployment & Local Run Guide

## 1. One-Click Docker (Easiest)

```bash
git clone https://github.com/5Username/focalpoint-os.git
cd focalpoint-os
docker compose up --build
```

- Frontend: http://localhost:5173
- Backend:  http://localhost:8000
- API docs: http://localhost:8000/docs

Full details in `docs/DOCKER.md`.

## 2. Manual Local Run

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

## 3. GitHub Pages (Public Demo Landing)

The repository is structured so a simple static landing page can be served from the root or a `docs/` / `gh-pages` branch.

Recommended for a clean public demo:
1. Build the frontend: `cd frontend && npm run build`
2. Copy the contents of `frontend/dist` to a `gh-pages` branch or use GitHub Actions to publish it.
3. Or keep a lightweight static `index.html` at the repo root for a pure GitHub Pages experience.

## 4. PDF Export

Once the backend is running, you can request PDFs via:

`POST /api/pdf/generate`

with body:
```json
{
  "type": "brief",
  "data": { ... brief object ... }
}
```
or `"type": "travel"`.

## 5. Showing samples to NGO clients

Share:
- `samples/weekly-brief-example.md`
- `samples/travel-risk-pack-example.md`

They print cleanly to PDF from any browser.
