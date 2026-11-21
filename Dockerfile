# =============================================================================
# Stage 1: Build the React + TypeScript + Tailwind + Monaco Web UI
# =============================================================================
FROM node:22-alpine AS web-builder
WORKDIR /build/web

COPY web/package.json web/package-lock.json* ./
RUN npm ci --no-fund --no-audit

COPY web/ ./
RUN npm run build

# =============================================================================
# Stage 2: Python 3.13 Runtime Image with uv + pytest
# =============================================================================
FROM python:3.13-slim AS runtime
WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /app/.pyquest

COPY pyproject.toml uv.lock* ./
COPY src/ /app/src/

RUN uv sync --no-dev --frozen || uv sync --no-dev

COPY curriculum/ /app/curriculum/
COPY --from=web-builder /build/web/dist /app/web/dist

ENV PYQUEST_HOST=0.0.0.0
ENV PYQUEST_PORT=8080
ENV PYQUEST_DB_PATH=/app/.pyquest/progress.db
ENV PYQUEST_CURRICULUM_DIR=/app/curriculum
ENV PYQUEST_WEB_DIST_DIR=/app/web/dist
ENV MPLBACKEND=Agg

EXPOSE 8080

HEALTHCHECK --interval=15s --timeout=5s --retries=3 --start-period=10s \
  CMD curl -sf http://127.0.0.1:8080/api/health || exit 1

CMD ["uv", "run", "--no-dev", "pyquest", "serve", "--host", "0.0.0.0", "--port", "8080"]
