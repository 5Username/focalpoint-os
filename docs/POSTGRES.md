# Postgres Migration & Docker Guide

## Default behaviour

By default FocalPoint OS uses **SQLite** (`focalpoint.db`).  
This is perfect for local development and single-server demos.

## Using Postgres

### Option A — Docker Compose (recommended)

The included `docker-compose.yml` already starts a Postgres 16 container.

```bash
docker compose up --build
```

Backend will automatically connect using:

```
DATABASE_URL=postgresql://focalpoint:focalpoint@db:5432/focalpoint
```

### Option B — External Postgres

```bash
export DATABASE_URL=postgresql://user:password@host:5432/focalpoint
```

Then start the backend normally. Tables are created automatically on startup.

## Switching from SQLite to Postgres

1. Set the `DATABASE_URL` environment variable.
2. Restart the backend — `init_db()` will create the required tables.
3. (Optional) Export data from SQLite and import into Postgres if you have existing records.

## Production notes

- Change `SECRET_KEY` to a long random string.
- Change the default Postgres password.
- Consider adding Alembic for formal migrations once the schema stabilises.
