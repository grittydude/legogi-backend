# legogi-backend

[![CI](https://github.com/grittydude/legogi-backend/actions/workflows/ci.yml/badge.svg)](https://github.com/grittydude/legogi-backend/actions/workflows/ci.yml)

API for the [L'egogi](https://github.com/grittydude/legogi) personal finance app,
built with FastAPI.

The project layout follows the MSF FastAPI template (`app/` with `core`, `db`,
`api`, `models`, `actions`, `services`), written from scratch rather than
depending on msflib.

## Requirements

- Python 3.11+
- [Poetry](https://python-poetry.org/) 2.x (`pipx install poetry`)

## Getting started

```bash
poetry install                               # create .venv and install dependencies
cp .env-example .env                         # optional: local settings, git-ignored
poetry run uvicorn app.main:app --reload     # start the API on http://127.0.0.1:8000
```

Then open:

- http://127.0.0.1:8000/health: the health check
- http://127.0.0.1:8000/api/v1/version: name, version and environment of the running API
- http://127.0.0.1:8000/docs: interactive API docs (Swagger UI)
- http://127.0.0.1:8000/redoc: the same docs, read-only

## Configuration

Settings live in `app/core/config.py` and are read from environment variables,
or from a `.env` file in the project root. `.env-example` lists every setting
with its default. Versioned endpoints are served under `/api/v1`.

## Docker (optional)

`compose.yml` runs the API with every service it uses: Postgres, Redis,
Mailpit (catches outgoing email) and SeaweedFS (S3-compatible storage standing
in for Cloudflare R2). With [Docker Desktop](https://www.docker.com/products/docker-desktop/)
installed:

```bash
docker compose up --build --wait     # build the API image and start everything
docker compose down                  # stop; add --volumes to delete the data
```

| Service | Address |
| --- | --- |
| API | http://127.0.0.1:8000 |
| Postgres | `127.0.0.1:5432` |
| Redis | `127.0.0.1:6379` |
| Mailpit inbox | http://127.0.0.1:8025 |
| S3 storage | http://127.0.0.1:8333 |

Docker isn't required for development: the `poetry run uvicorn` steps above
are enough. CI builds the image and starts this stack on every pull request.

## Scripts

| Script | What it does |
| --- | --- |
| `scripts/test.sh` | Runs the tests with a coverage report. Extra arguments go to pytest, e.g. `-k version` or `-x`. CI runs this. |
| `scripts/lint.sh` | Lint, format check and type check. CI runs this. |
| `scripts/format.sh` | Auto-fixes imports, simple lint issues and formatting. |
