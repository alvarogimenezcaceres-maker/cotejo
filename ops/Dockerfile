# Imagen del ciclo de Cotejo: ingesta + agrupación + build del sitio.
FROM node:24-bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-venv ca-certificates \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
RUN python3 -m venv /venv
COPY ingest/requirements.txt ingest/requirements.txt
RUN /venv/bin/pip install --no-cache-dir -r ingest/requirements.txt
COPY web/package.json web/package-lock.json web/
RUN cd web && npm ci
COPY . .
ENV PATH="/venv/bin:$PATH" FASTEMBED_CACHE_PATH=/cache
CMD ["sh", "ops/cycle.sh"]
