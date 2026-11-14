# Deployment & Local Run Guide

## 1. One-Click Docker (Recommended)

```bash
git clone https://github.com/5Username/focalpoint-os.git
cd focalpoint-os
docker compose up --build
```

- Backend: http://localhost:8000
- Frontend: http://localhost:5173

## 2. Manual Local Run

### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## 3. GitHub Pages (Public Demo)

1. Go to the repository on GitHub
2. Settings → Pages
3. Source: Deploy from a branch
4. Branch: `main` / folder: `/ (root)` or use a `gh-pages` workflow later
5. For a proper static demo you can build the frontend (`npm run build`) and serve the `dist` folder.

## 4. Showing Samples to NGO Clients

Share these files directly:
- `samples/weekly-brief-example.md`
- `samples/travel-risk-pack-example.md`

They are written to look professional and can be exported to PDF from any browser (Print → Save as PDF).
