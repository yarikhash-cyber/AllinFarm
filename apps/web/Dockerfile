# syntax=docker/dockerfile:1.7
# AllinFarm site: build the static SPA, then serve it with Caddy.
# Build context: repository root.
FROM node:22-slim AS build

WORKDIR /app

# Optional extra CA certificate for networks with a TLS-inspecting proxy
# (build secret "extra_ca", see compose.override.example.yaml). Nothing stays in the image.
RUN --mount=type=secret,id=extra_ca,required=false \
    set -eu; \
    if [ -s /run/secrets/extra_ca ]; then export NODE_EXTRA_CA_CERTS=/run/secrets/extra_ca; fi; \
    npm install --global --no-fund --no-audit pnpm@10.28.0

COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./
COPY apps/web/package.json apps/web/package.json
RUN --mount=type=secret,id=extra_ca,required=false \
    set -eu; \
    if [ -s /run/secrets/extra_ca ]; then export NODE_EXTRA_CA_CERTS=/run/secrets/extra_ca; fi; \
    pnpm install --frozen-lockfile --filter web

COPY apps/web apps/web
RUN pnpm -C apps/web build

FROM caddy:2.10

COPY infra/caddy/Caddyfile /etc/caddy/Caddyfile
COPY --from=build /app/apps/web/build /srv
EXPOSE 8080
