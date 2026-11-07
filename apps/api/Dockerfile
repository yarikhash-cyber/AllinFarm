# syntax=docker/dockerfile:1.7
# AllinFarm API. Build context: repository root.
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never \
    UV_PROJECT_ENVIRONMENT=/app/.venv

WORKDIR /app

# Optional extra CA certificate for networks with a TLS-inspecting proxy
# (build secret "extra_ca", see compose.override.example.yaml). Nothing stays in the image.
RUN --mount=type=secret,id=extra_ca,required=false \
    set -eu; \
    if [ -s /run/secrets/extra_ca ]; then \
      cat /etc/ssl/certs/ca-certificates.crt /run/secrets/extra_ca > /tmp/ca.pem; \
      export PIP_CERT=/tmp/ca.pem; \
    fi; \
    pip install --no-cache-dir uv==0.11.32; \
    rm -f /tmp/ca.pem

# Dependencies first, so code changes do not reinstall them.
COPY pyproject.toml uv.lock ./
COPY apps/api/pyproject.toml apps/api/pyproject.toml
COPY packages/engine/pyproject.toml packages/engine/pyproject.toml
COPY packages/units/pyproject.toml packages/units/pyproject.toml
RUN --mount=type=secret,id=extra_ca,required=false \
    set -eu; \
    if [ -s /run/secrets/extra_ca ]; then \
      cat /etc/ssl/certs/ca-certificates.crt /run/secrets/extra_ca > /tmp/ca.pem; \
      export SSL_CERT_FILE=/tmp/ca.pem; \
    fi; \
    uv sync --frozen --no-dev --no-install-workspace --package allinfarm-api; \
    rm -f /tmp/ca.pem

COPY packages packages
COPY apps/api apps/api
RUN uv sync --frozen --no-dev --offline --package allinfarm-api

RUN useradd --system --uid 10001 --home-dir /app allinfarm
USER allinfarm

ENV PATH="/app/.venv/bin:$PATH"
WORKDIR /app/apps/api
EXPOSE 8000
HEALTHCHECK --interval=5s --timeout=3s --start-period=10s --retries=12 \
  CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/api/health', timeout=2).status == 200 else 1)"

# Migrations run on every start; they are idempotent.
CMD ["sh", "-c", "alembic upgrade head && exec uvicorn allinfarm_api.main:app --host 0.0.0.0 --port 8000 --proxy-headers"]
