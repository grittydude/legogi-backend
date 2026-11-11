#!/usr/bin/env bash
# Runs inside the API container before the server starts, every time the
# container starts. It is the Dockerfile's ENTRYPOINT: it does its preparation,
# then `exec "$@"` replaces this script with the CMD (uvicorn), so uvicorn
# receives Docker's stop signal directly.
set -euo pipefail

# Nothing to prepare yet. Later PRs add, in order:
#   PR 6: wait until the database accepts connections
#   PR 8: apply database migrations (alembic upgrade head)
echo "prestart: ready"

exec "$@"
