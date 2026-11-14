# Advanced Features Guide

## 1. Multi-tenant NGO Workspaces

Each NGO can have its own workspace with preferred region and language.

```bash
# Create a workspace
curl -X POST http://localhost:8000/api/workspaces/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Example NGO Kenya", "region": "Kenya", "primary_language": "en"}'

# List workspaces
curl http://localhost:8000/api/workspaces/
```

## 2. Automated Weekly Brief Scheduling

Configure a weekly brief for a workspace:

```bash
curl -X POST http://localhost:8000/api/workspaces/{ws_id}/schedule \
  -H "Content-Type: application/json" \
  -d '{"day_of_week": "monday", "hour": 7, "timezone": "Africa/Nairobi"}'
```

In production you would connect this to:
- APScheduler / Celery inside the backend
- External cron job
- GitHub Actions scheduled workflow that calls the generate endpoint

## 3. GeoJSON Export & Map Layers

```bash
# Get illustrative public hotspots as GeoJSON
curl http://localhost:8000/api/geo/hotspots

# Download as .geojson file
curl -O -J http://localhost:8000/api/geo/hotspots.geojson
```

The Crisis page already renders a Leaflet map. Additional layers can be toggled in future UI updates.

## 4. Recommended Production Next Steps

- Replace in-memory workspace store with SQLite or Postgres
- Add authentication (API keys or simple JWT per workspace)
- Connect the schedule to a real task runner
- Add more public data layers (with clear attribution)
