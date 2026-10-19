#!/bin/sh
# Ciclo de Cotejo: ingesta, agrupación y build del sitio estático. Se repite cada CYCLE_SECONDS.
# Si un paso falla, se registra y el ciclo sigue; el sitio anterior queda publicado.
while true; do
  echo "[$(date -u +%FT%TZ)] ciclo"
  python ingest/ingest.py || echo "ingesta falló"
  python ingest/cluster.py || echo "agrupación falló"
  if (cd web && npm run build --silent); then
    rm -rf /site/* && cp -r web/dist/. /site/
    echo "sitio actualizado"
  else
    echo "build falló; se mantiene el sitio anterior"
  fi
  sleep "${CYCLE_SECONDS:-3600}"
done
