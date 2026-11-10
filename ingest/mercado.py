"""Pulso de mercado de Cotejo: guarda cotizaciones de referencia (USD/PYG del BCP y de mercado, Bitcoin, Ethereum, oro).

Hace: consulta tres APIs públicas gratuitas (Frankfurter, ExchangeRate-API y CoinGecko), con user-agent propio, y guarda
el valor y la hora de cada dato para que el sitio muestre el último valor y una serie corta. USD/PYG se pide
como máximo cada 6 h (la fuente actualiza una vez al día). El oro es PAXG, un token respaldado en oro: es un
sustituto, no la cotización de la onza en el mercado de metales.
La cotización referencial del BCP se toma de Frankfurter (proyecto abierto que republica el dato del BCP, un valor por día hábil);
el sitio del BCP no se lee porque bloquea el acceso automatizado.
No hace: no evade bloqueos, no predice ni recomienda, no usa claves ni cuentas.

Uso: py ingest/mercado.py   (BD: variable COTEJO_DB, por defecto localhost:5433)
"""
import os
from datetime import date, datetime, timedelta, timezone

import psycopg
import requests

USER_AGENT = "CotejoBot/0.1 (+https://github.com/alvarogimenezcaceres-maker/cotejo; agregador abierto sin fines de lucro)"
DB = os.environ.get("COTEJO_DB", "postgresql://cotejo:cotejo_dev@127.0.0.1:5433/cotejo")
TIMEOUT = 20
FX_CADA_HORAS = 6
BCP_CADA_HORAS = 3
BCP_DIAS = 21
CRIPTO = {"bitcoin": "BTC", "ethereum": "ETH", "pax-gold": "XAU"}

SCHEMA = """
CREATE TABLE IF NOT EXISTS market_quotes (
    id         BIGSERIAL PRIMARY KEY,
    symbol     TEXT NOT NULL,
    value      DOUBLE PRECISION NOT NULL,
    change_pct DOUBLE PRECISION,
    as_of      TIMESTAMPTZ NOT NULL,
    fetched_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    source     TEXT NOT NULL,
    UNIQUE (symbol, as_of)
)"""


def get_json(url):
    r = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT)
    r.raise_for_status()
    return r.json()


def fetch_fx():
    """(valor guaraníes por dólar, hora del dato) o None."""
    d = get_json("https://open.er-api.com/v6/latest/USD")
    if d.get("result") != "success":
        return None
    return float(d["rates"]["PYG"]), datetime.fromtimestamp(d["time_last_update_unix"], timezone.utc)


def fetch_bcp():
    """[(día hábil, guaraníes por dólar)] de los últimos días: cotización referencial interbancaria del BCP."""
    desde = (date.today() - timedelta(days=BCP_DIAS)).isoformat()
    d = get_json(f"https://api.frankfurter.dev/v2/rates?providers=BCP&base=USD&quotes=PYG&from={desde}")
    return [(date.fromisoformat(x["date"]), float(x["rate"])) for x in d if x.get("quote") == "PYG"]


def fetch_cripto():
    """[(símbolo, valor en dólares, variación 24 h en %, hora del dato)]."""
    ids = ",".join(CRIPTO)
    d = get_json(
        f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd"
        "&include_24hr_change=true&include_last_updated_at=true")
    out = []
    for cid, sym in CRIPTO.items():
        x = d.get(cid)
        if x and "usd" in x:
            ts = x.get("last_updated_at")
            as_of = datetime.fromtimestamp(ts, timezone.utc) if ts else datetime.now(timezone.utc)
            out.append((sym, float(x["usd"]), x.get("usd_24h_change"), as_of))
    return out


def guardar(conn, symbol, value, change, as_of, source):
    return conn.execute(
        """INSERT INTO market_quotes (symbol, value, change_pct, as_of, source) VALUES (%s,%s,%s,%s,%s)
           ON CONFLICT (symbol, as_of) DO NOTHING""",
        (symbol, value, change, as_of, source)).rowcount


def main():
    with psycopg.connect(DB, connect_timeout=30) as conn:
        conn.execute(SCHEMA)
        nuevas = 0
        bcp_reciente = conn.execute(
            "SELECT count(*) FROM market_quotes WHERE symbol='USDPYG_BCP' AND fetched_at > now() - make_interval(hours => %s)",
            (BCP_CADA_HORAS,)).fetchone()[0]
        if bcp_reciente:
            print("USDPYG_BCP: dato nuevo hace menos de 3 h, se omite")
        else:
            try:
                serie = fetch_bcp()
                for dia, valor in serie:
                    nuevas += guardar(conn, "USDPYG_BCP", valor, None,
                                      datetime(dia.year, dia.month, dia.day, tzinfo=timezone.utc), "BCP (vía Frankfurter)")
                if serie:
                    print(f"USDPYG_BCP: {serie[-1][1]:.2f} ({serie[-1][0]}), {len(serie)} días")
            except Exception as e:
                print(f"USDPYG_BCP: error {e}")
        reciente = conn.execute(
            "SELECT count(*) FROM market_quotes WHERE symbol='USDPYG' AND fetched_at > now() - make_interval(hours => %s)",
            (FX_CADA_HORAS,)).fetchone()[0]
        if reciente:
            print("USDPYG: pedido hace menos de 6 h, se omite")
        else:
            try:
                fx = fetch_fx()
                if fx:
                    nuevas += guardar(conn, "USDPYG", fx[0], None, fx[1], "ExchangeRate-API")
                    print(f"USDPYG: {fx[0]:.2f} ({fx[1]:%Y-%m-%d %H:%M} UTC)")
            except Exception as e:
                print(f"USDPYG: error {e}")
        try:
            for sym, valor, cambio, as_of in fetch_cripto():
                nuevas += guardar(conn, sym, valor, cambio, as_of, "CoinGecko")
                print(f"{sym}: {valor} ({cambio if cambio is None else round(cambio, 2)} % 24 h)")
        except Exception as e:
            print(f"cripto: error {e}")
        print(f"mercado: {nuevas} cotizaciones nuevas")


if __name__ == "__main__":
    main()
