# The API's container image, built in two stages:
#   1. builder: installs Poetry and the production dependencies into /app/.venv
#   2. runtime: copies only that .venv and the app code, so Poetry and build
#      leftovers never reach the image we run.

# ---- Stage 1: build the virtualenv ------------------------------------------
FROM python:3.11-slim AS builder

ENV POETRY_VERSION=2.5.1 \
    POETRY_NO_INTERACTION=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN pip install "poetry==${POETRY_VERSION}"

WORKDIR /app

# Copy only the dependency files first. Docker caches each step, so this slow
# install reruns only when these three files change, not on every code edit.
# poetry.toml puts the virtualenv in /app/.venv.
COPY pyproject.toml poetry.lock poetry.toml ./
RUN poetry install --only main --no-ansi

# ---- Stage 2: the image we run -----------------------------------------------
FROM python:3.11-slim

# Don't write .pyc files, print logs straight away, and use the venv's Python.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

# Run as an ordinary user: if the app is ever compromised, the attacker is not
# root inside the container.
RUN useradd --create-home --uid 1000 app

WORKDIR /app

COPY --from=builder /app/.venv ./.venv
COPY app ./app
COPY --chmod=0755 prestart.sh ./

USER app

EXPOSE 8000

# Docker marks the container "healthy" once /health answers. The slim image has
# no curl, so Python makes the request.
HEALTHCHECK --interval=10s --timeout=3s --start-period=10s --retries=3 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2)"]

# prestart.sh prepares the container, then runs CMD in its place.
ENTRYPOINT ["./prestart.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
