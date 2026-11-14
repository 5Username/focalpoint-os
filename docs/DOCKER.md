# One-Click Docker Guide

## Prerequisites
- Docker Desktop (or Docker Engine + Compose) installed

## Run everything with one command

```bash
git clone https://github.com/5Username/focalpoint-os.git
cd focalpoint-os
docker compose up --build
```

That’s it.

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API docs: http://localhost:8000/docs

## Useful commands

```bash
# Stop
docker compose down

# Rebuild after code changes
docker compose up --build

# View logs
docker compose logs -f
```

## Notes
- The first run downloads images and installs dependencies (can take a few minutes).
- Subsequent starts are much faster.
- Data and code are mounted so changes on your machine appear inside the containers.
