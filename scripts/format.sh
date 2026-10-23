#!/usr/bin/env bash
# Fixes what can be fixed automatically: import order, simple lint issues,
# and formatting.
set -euo pipefail

poetry run ruff check --fix app
poetry run ruff format app
