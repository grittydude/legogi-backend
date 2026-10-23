#!/usr/bin/env bash
# Runs the test suite with a coverage report. Extra arguments go to pytest:
#
#     bash scripts/test.sh -k version      # only tests whose name contains "version"
#     bash scripts/test.sh -x              # stop at the first failure
#
# CI runs this script.
set -euo pipefail

poetry run pytest --cov=app --cov-report=term-missing "$@"
