-- Esquema de Cotejo. Guarda solo título, fragmento (máx. 300 caracteres), enlace y fecha.
-- No guarda el texto completo de las notas.
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS sources (
    id          SERIAL PRIMARY KEY,
    slug        TEXT UNIQUE NOT NULL,
    name        TEXT NOT NULL,
    tipo        TEXT NOT NULL CHECK (tipo IN ('oficialismo','independiente','critico','publico','fuente_primaria')),
    feed_url    TEXT,
    active      BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS articles (
    id           BIGSERIAL PRIMARY KEY,
    source_id    INT NOT NULL REFERENCES sources(id),
    url          TEXT NOT NULL UNIQUE,
    title        TEXT NOT NULL,
    snippet      TEXT CHECK (char_length(snippet) <= 300),
    published_at TIMESTAMPTZ,
    fetched_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    embedding    vector(384)  -- multilingual-e5-small
);
CREATE INDEX IF NOT EXISTS articles_published_idx ON articles (published_at);
CREATE INDEX IF NOT EXISTS articles_source_idx ON articles (source_id);

CREATE TABLE IF NOT EXISTS events (
    id            BIGSERIAL PRIMARY KEY,
    title         TEXT NOT NULL,
    topic         TEXT NOT NULL DEFAULT 'otros'
                  CHECK (topic IN ('politica','salud','educacion','economia','seguridad','ambiente','otros')),
    sensitive     BOOLEAN NOT NULL DEFAULT FALSE,  -- denuncias, acusaciones, candidatos: sin resumen
    summary       JSONB,                           -- afirmaciones con URLs; NULL = solo titulares
    covered_types TEXT[] NOT NULL DEFAULT '{}',
    missing_types TEXT[] NOT NULL DEFAULT '{}',    -- punto ciego
    first_seen_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS event_articles (
    event_id   BIGINT NOT NULL REFERENCES events(id) ON DELETE CASCADE,
    article_id BIGINT NOT NULL REFERENCES articles(id) ON DELETE CASCADE,
    PRIMARY KEY (event_id, article_id)
);

-- Cola de reportes de error enviados por lectores.
CREATE TABLE IF NOT EXISTS reports (
    id          BIGSERIAL PRIMARY KEY,
    event_id    BIGINT REFERENCES events(id) ON DELETE SET NULL,
    message     TEXT NOT NULL,
    status      TEXT NOT NULL DEFAULT 'abierto' CHECK (status IN ('abierto','revisado','resuelto','descartado')),
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    resolved_at TIMESTAMPTZ
);

-- Eventos despublicados: el sitio no los genera.
CREATE TABLE IF NOT EXISTS unpublished (
    event_id       BIGINT PRIMARY KEY REFERENCES events(id) ON DELETE CASCADE,
    reason         TEXT NOT NULL,
    unpublished_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
