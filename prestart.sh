#!/usr/bin/env bash
# Runs inside the API container before the server starts, every time the
# container starts. It is the Dockerfile's ENTRYPOINT: it does its preparation,
# then `exec "$@"` replaces this script with the CMD (uvicorn), so uvicorn
# receives Docker's stop signal directly.
set -euo pipefail

# 1. Wait until the database accepts connections (up to 60 tries, 1s apart).
python -m app.backend_pre_start

# 2. Apply database migrations: added in PR 8 (alembic upgrade head).

echo "prestart: ready"

exec "$@"
