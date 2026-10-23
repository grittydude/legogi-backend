#!/usr/bin/env bash
# Fails if the code has lint errors, is not formatted, or has type errors.
# CI runs exactly this script.
set -euo pipefail

poetry run ruff check app
poetry run ruff format --check app
poetry run mypy app
