// Lectura de la BD al compilar. No escribe nada; el sitio es estático.
import pg from 'pg';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

const DB = process.env.COTEJO_DB ?? 'postgresql://cotejo:cotejo_dev@127.0.0.1:5433/cotejo';
export const TIPOS = {
  oficialismo: 'Oficialismo',
  independiente: 'Independiente',
  critico: 'Crítico del gobierno',
  publico: 'Público',
  fuente_primaria: 'Fuente primaria',
};

// Slugs cuya clasificación fue revisada (revisado: true en sources/media.yaml).
function revisados() {
  const txt = readFileSync(resolve(process.cwd(), '../sources/media.yaml'), 'utf8');
  return new Set([...txt.matchAll(/^\s+([\w-]+):\s*\{[^}]*revisado:\s*true/gm)].map((m) => m[1]));
}

export async function cargarEventos() {
  const ok = revisados();
  const client = new pg.Client({ connectionString: DB });
  await client.connect();
  const { rows } = await client.query(`
    SELECT e.id, e.title, e.first_seen_at, e.updated_at,
           s.slug, s.name AS medio, s.tipo,
           a.title AS nota, a.url, a.snippet, a.published_at
    FROM events e
    JOIN event_articles ea ON ea.event_id = e.id
    JOIN articles a ON a.id = ea.article_id
    JOIN sources s ON s.id = a.source_id
    WHERE NOT EXISTS (SELECT 1 FROM unpublished u WHERE u.event_id = e.id)
    ORDER BY e.id, a.published_at`);
  const tiposActivos = (await client.query('SELECT DISTINCT tipo FROM sources WHERE active')).rows.map((r) => r.tipo);
  await client.end();

  const por = new Map();
  for (const r of rows) {
    if (!por.has(r.id)) por.set(r.id, { id: r.id, title: r.title, updated: r.updated_at, notas: [] });
    por.get(r.id).notas.push(r);
  }
  const eventos = [...por.values()]
    .map((e) => {
      e.medios = new Set(e.notas.map((n) => n.slug)).size;
      e.clasificado = e.notas.every((n) => ok.has(n.slug));
      e.cubiertos = [...new Set(e.notas.map((n) => n.tipo))];
      e.ciegos = tiposActivos.filter((t) => !e.cubiertos.includes(t));
      e.fecha = e.notas.map((n) => n.published_at).filter(Boolean).sort().at(-1) ?? e.updated;
      return e;
    })
    .filter((e) => e.notas.length >= 2)
    .sort((a, b) => b.medios - a.medios || b.fecha - a.fecha);
  return { eventos, tiposActivos };
}

export const fmt = (d) =>
  new Intl.DateTimeFormat('es-PY', { dateStyle: 'medium', timeStyle: 'short', timeZone: 'America/Asuncion' }).format(new Date(d));
