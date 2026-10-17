"""Despublica un evento de Cotejo: el sitio deja de generarlo en el próximo build.

Hace: registra el evento en `unpublished` con el motivo. Con --restore lo vuelve a publicar.
No hace: no borra notas ni eventos, no reconstruye el sitio.

Uso: py ingest/unpublish.py ID "motivo"   |   py ingest/unpublish.py ID --restore
"""
import os
import sys

import psycopg

DB = os.environ.get("COTEJO_DB", "postgresql://cotejo:cotejo_dev@127.0.0.1:5433/cotejo")


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    event_id, arg = int(sys.argv[1]), sys.argv[2]
    with psycopg.connect(DB) as conn:
        if arg == "--restore":
            n = conn.execute("DELETE FROM unpublished WHERE event_id=%s", (event_id,)).rowcount
            print("republicado" if n else "no estaba despublicado")
        else:
            conn.execute(
                "INSERT INTO unpublished (event_id, reason) VALUES (%s,%s) "
                "ON CONFLICT (event_id) DO UPDATE SET reason=EXCLUDED.reason, unpublished_at=now()",
                (event_id, arg),
            )
            print(f"evento {event_id} despublicado")


if __name__ == "__main__":
    main()
