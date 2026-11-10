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

// Secciones de la portada, en orden. La asigna ingest/cluster.py según sources/temas.yaml.
export const SECCIONES = {
  bolsa: 'Mercado de valores',
  economia: 'Economía',
};

// Slugs cuya clasificación fue revisada (revisado: true en sources/media.yaml).
function revisados() {
  const txt = readFileSync(resolve(process.cwd(), '../sources/media.yaml'), 'utf8');
  return new Set([...txt.matchAll(/^\s+([\w-]+):\s*\{[^}]*revisado:\s*true/gm)].map((m) => m[1]));
}

const MIN = 60_000;
const H = 3_600_000;
const D = 24 * H;
const VENTANA_DIAS = 14; // la portada solo lista hechos con alguna nota de los últimos 14 días

function lag(ms) {
  if (ms < 10 * MIN) return 'a la par';
  if (ms < H) return `+${Math.round(ms / MIN)} min`;
  if (ms < D) return `+${Math.round(ms / H)} h`;
  const d = Math.floor(ms / D);
  const h = Math.round((ms % D) / H);
  return h ? `+${d} d ${h} h` : `+${d} d`;
}

// Quién publicó primero entre las fuentes que Cotejo lee y cuánto después se sumó cada una.
// La BVA publica solo la fecha (sin hora): aparece sin desfase.
function cobertura(notas) {
  const primera = new Map();
  for (const n of notas) {
    if (!n.published_at || n.slug === 'bva') continue;
    const t = new Date(n.published_at).getTime();
    if (!primera.has(n.slug) || t < primera.get(n.slug).t) primera.set(n.slug, { nombre: n.medio, t });
  }
  const orden = [...primera.values()].sort((a, b) => a.t - b.t);
  const medios = orden.map((m, i) => ({ nombre: m.nombre, lag: i === 0 ? null : lag(m.t - orden[0].t) }));
  for (const n of notas) if (n.slug === 'bva' && !medios.some((m) => m.nombre === n.medio)) medios.push({ nombre: n.medio, lag: null });
  return { medios, conOrden: orden.length > 1 };
}

// Orden provisional de la portada: 40 % medios distintos, 25 % volumen de notas, 35 % frescura. No mide impacto de mercado.
function relevancia(e, ahora) {
  const c = Math.min(1, Math.log(1 + e.medios) / Math.log(1 + 8));
  const n = Math.min(1, Math.log(1 + e.notas.length) / Math.log(1 + 20));
  const f = Math.exp(-Math.max(0, (ahora - new Date(e.fecha).getTime()) / H) / 24);
  return 0.4 * c + 0.25 * n + 0.35 * f;
}

export async function cargarEventos() {
  const ok = revisados();
  const client = new pg.Client({ connectionString: DB });
  await client.connect();
  const { rows } = await client.query(`
    SELECT e.id, e.title, e.topic, e.first_seen_at, e.updated_at,
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
    if (!por.has(r.id)) por.set(r.id, { id: r.id, title: r.title, seccion: r.topic, updated: r.updated_at, notas: [] });
    por.get(r.id).notas.push(r);
  }
  const ahora = Date.now();
  const todos = [...por.values()]
    .map((e) => {
      e.medios = new Set(e.notas.map((n) => n.slug)).size;
      e.clasificado = e.notas.every((n) => ok.has(n.slug));
      e.cubiertos = [...new Set(e.notas.map((n) => n.tipo))];
      e.ciegos = tiposActivos.filter((t) => !e.cubiertos.includes(t));
      e.fecha = e.notas.map((n) => n.published_at).filter(Boolean).sort().at(-1) ?? e.updated;
      e.soloBva = e.notas.every((n) => n.slug === 'bva');
      e.cobertura = cobertura(e.notas);
      e.rel = relevancia(e, ahora);
      return e;
    })
    .filter((e) => e.seccion in SECCIONES);
  // Hechos con cobertura de prensa (1 medio basta en Mercado de valores, 2 en Economía)
  const eventos = todos.filter((e) => !e.soloBva && e.medios >= (e.seccion === 'bolsa' ? 1 : 2));
  // Comunicados de la BVA: fuente primaria, aparte de los hechos con cobertura
  const comunicados = todos.filter((e) => e.soloBva).sort((a, b) => new Date(b.fecha) - new Date(a.fecha));
  const portada = eventos
    .filter((e) => ahora - new Date(e.fecha).getTime() <= VENTANA_DIAS * D)
    .sort((a, b) => b.rel - a.rel || new Date(b.fecha) - new Date(a.fecha));
  return { eventos, portada, comunicados, tiposActivos };
}

export const fmt = (d) =>
  new Intl.DateTimeFormat('es-PY', { dateStyle: 'medium', timeStyle: 'short', timeZone: 'America/Asuncion' }).format(new Date(d));
export const fmtCorto = (d) =>
  new Intl.DateTimeFormat('es-PY', { day: 'numeric', month: 'short', timeZone: 'America/Asuncion' }).format(new Date(d));
