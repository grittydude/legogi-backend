# legogi-backend

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
poetry run uvicorn app.main:app --reload     # start the API on http://127.0.0.1:8000
```

Then open:

- http://127.0.0.1:8000/health: the health check
- http://127.0.0.1:8000/docs: interactive API docs (Swagger UI)
- http://127.0.0.1:8000/redoc: the same docs, read-only

## Scripts

| Script | What it does |
| --- | --- |
| `scripts/lint.sh` | Lint, format check and type check. CI runs this. |
| `scripts/format.sh` | Auto-fixes imports, simple lint issues and formatting. |
