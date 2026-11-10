# Cotejo: rediseño y evolución estratégica

Documento de propuesta. Fecha de los datos medidos: 2026-11-10 (sitio publicado, 71 hechos).
Nada de lo aquí propuesto está implementado. Cada decisión que contradice una regla del proyecto
está marcada con **[DECISIÓN]** y reunida en la sección 19.

---

## 0. Veredicto del inversor (leer primero)

**Hoy no financiaría el crecimiento. Sí pondría capital semilla condicionado a tres hitos.**

Lo que vale la pena: la idea ("un mismo hecho, contado por varios medios") es correcta, es
difícil de copiar *si* se acumulan datos de cobertura con marca de tiempo, y la metodología
neutral con enlaces es creíble. Lo que impide invertir hoy:

1. **La ventaja competitiva está desactivada.** El punto ciego (qué tipo de medio no cubrió)
   no se muestra en ninguna página porque ningún medio está revisado. Hoy el sitio es una lista de titulares.
2. **Los datos son demasiado delgados para el Radar.** En Economía, 31 de 40 hechos tienen
   2 medios; el máximo es 4. Un "radar" de 2 puntos es una línea. La causa es de fuentes, no de diseño (sección 1.3).
3. **Hay defectos que un lector financiero detecta en un minuto**, incluido uno que introduje yo (sección 2, P0).
4. **No hay modelo de sostenibilidad ni cortafuegos editorial.** Si el dinero llega de bancos o casas de bolsa que Cotejo cubre, la neutralidad queda comprometida.

**Hitos para liberar capital:** (a) 15 o más medios y fuentes primarias con cobertura legal verificada,
(b) Radar de Cobertura publicado con al menos 3 medios en el 40 % de los hechos,
(c) clasificación de medios revisada y publicada con evidencia.

---

## 1. Diagnóstico del sitio actual

### 1.1 Qué funciona (y debe conservarse)
| Aspecto | Evidencia | Por qué importa |
|---|---|---|
| Rapidez | 30 KB de HTML, 0 JavaScript, 0 imágenes | Carga instantánea incluso con mala conexión móvil |
| Transparencia | "Agrupado automáticamente", "Sin resumen: solo titulares y enlaces", enlace de reporte de error | Credibilidad editorial rara en el país |
| Neutralidad estructural | No hay resúmenes inventados ni opiniones | Es el diferencial frente a portales que editorializan |
| Modo oscuro y foco visible | `prefers-color-scheme`, `:focus-visible` con contorno de 3 px | Accesibilidad base mejor que la media |
| Tipografía editorial | Serif de sistema, escala clara, acento rojo ladrillo único | Identidad propia, no clon de Yahoo Finance |
| Datos abiertos de origen | Cada nota enlaza al medio original | Cotejo no compite con los medios: los dirige tráfico |

### 1.2 Qué resulta anticuado o limita la credibilidad
- **Estética de periódico impreso, no de plataforma financiera.** Fondo papel `#f3efe4`, cuerpo serif de 18 px, columna de 62 rem. Transmite "blog culto", no "terminal de datos". No hay una sola cifra en la portada.
- **Cero jerarquía.** El hecho nº 1 y el nº 71 pesan igual: mismo tamaño, misma tipografía. No hay hero, ni "tema del día", ni agrupación por importancia.
- **El orden es medios (desc.) y luego fecha.** Un hecho de hace 6 días con 4 medios supera a uno de hoy con 3. No existe la noción de "hoy" ni de frescura.
- **Fechas absolutas** ("10 nov. 2026, 6:28 a. m.") sin relativo ("hace 3 h"). En finanzas el *cuándo* es el dato.
- **Avisos de proceso interno en cada página:** "La clasificación de medios está en revisión; no se muestra el punto ciego". Es honestidad bienintencionada, pero comunica "producto sin terminar" en la propuesta central.
- **Sin búsqueda, sin filtros, sin RSS propio, sin metadatos para compartir** (no hay `og:title`; un enlace pegado en WhatsApp sale pelado).
- **Las secciones separan por tema pero no por relevancia.** Mercado de valores y Economía son listas planas.

### 1.3 Qué limita el crecimiento (medido)
| Medición (2026-11-10) | Resultado | Lectura crítica |
|---|---|---|
| Hechos en portada | 71 (31 Mercado de valores, 40 Economía) | Volumen aceptable |
| Medios por hecho, Economía | 2 medios: 31 · 3: 7 · 4: 2 | **Mediana = 2.** El Radar sería casi vacío |
| Medios por hecho, Mercado de valores | 1 medio: 27 de 31 | Casi todo es la BVA sola (comunicados), no cobertura cruzada |
| Medios activos | 8 prensa + BVA | La Nación (la que más cubre bolsa) no tiene RSS: **ausente**. Infonegocios, 5Días, BCP y El Nacional (categoría) bloquean por `robots.txt` |
| Clasificación revisada | 0 de 9 | El eje editorial (oficialismo/independiente/crítico) no existe en pantalla |
| Resúmenes | 0 | Coherente con las reglas, pero la home no ofrece nada "accionable" |

**Conclusión:** el cuello de botella es **cobertura de fuentes**, no diseño. Un rediseño bonito sobre 8 fuentes
solo da una lista bonita.

---

## 2. Problemas críticos (ordenados)

| # | Problema | Evidencia | Gravedad |
|---|---|---|---|
| **P0-1** | **Hecho falso de 105 notas.** Todos los comunicados de la BVA ("Hecho de relevancia: X") se agrupan en un solo evento titulado "Hecho de relevancia: MUNICIPALIDAD DE VILLA ELISA", con "1 medio · 105 notas". | `/evento/8795/` | Crítica. **Lo causó mi incorporación de la BVA**: los títulos plantilla tienen similitud coseno alta entre sí. Presenta como un hecho a 105 empresas distintas |
| **P0-2** | **Títulos de evento obsoletos.** El título es el de la primera nota. `/evento/7085/` abarca del 3 al 7 de nov. y se titula "asociación de asegurados exige juicio político…" mientras sus notas más nuevas hablan de detención y destitución | `/evento/7085/` | Alta. El lector entiende mal de qué trata el hecho |
| **P0-3** | **Ranking sin frescura.** Ordena por medios y fecha: una historia vieja con muchos medios tapa la noticia de hoy | Orden de la portada | Alta |
| **P1-1** | Punto ciego y tipo de medio apagados (0/9 revisados) | Todas las páginas de evento | Alta: es el diferencial |
| **P1-2** | Sin cruce temporal. Se listan notas en orden cronológico, pero **no se calcula ni muestra quién publicó primero ni el desfase** | Página de evento | Alta: el dato ya existe (`published_at`) y no se explota |
| **P1-3** | Fuentes insuficientes (sección 1.3) | Mediciones | Alta |
| **P2-1** | Sin búsqueda, RSS, `og:*`, sitemap, favicon propio | Código de `Base.astro` | Media |
| **P2-2** | La política queda fuera del filtro, pero el hecho más cubierto hoy mezcla política y banca (Ueno + Peña). Falta criterio editorial público para los hechos mixtos | Portada | Media |
| **P2-3** | Los comunicados de la BVA solo traen el nombre de la entidad como título. No dicen *qué* pasó | `bva.py`, listados | Media. Requiere abrir la ficha, hoy fuera de alcance por regla |

---

## 3. Oportunidades

1. **El desfase de publicación es un dato inédito.** Ningún portal paraguayo muestra quién cuenta primero y quién replica. Ya tenemos `published_at`.
2. **"Silencio informativo":** comunicados de la BVA que ningún medio recogió en 48 h. Cruza fuente primaria con prensa. Nadie lo ofrece.
3. **Cifras en conflicto:** cuando dos medios reportan montos distintos para el mismo hecho, mostrarlo.
4. **Archivo acumulable.** Cada día de datos de cobertura es un activo que un competidor no puede reconstruir hacia atrás.
5. **Datos abiertos (AGPL):** publicar el conjunto de cobertura como CSV/JSON diario atrae a periodistas, académicos y casas de bolsa que lo citen.

---

## 4. Nueva propuesta de valor

> **Cotejo: cómo se construyó cada noticia económica de Paraguay, y qué comunicado oficial nadie contó.**

De "agregador de noticias" a **"plataforma de inteligencia de cobertura"**. Importante: la inteligencia
se deriva de **metadatos de cobertura** (quién, cuándo, cuánto, con qué palabras), no de opinión ni de
predicción de mercado. Esa frontera es lo que protege la credibilidad.

Principio rector: *toda funcionalidad debe responder una de estas tres preguntas sobre un hecho:*
**¿quién lo contó, cuándo, y en qué se diferenciaron?**

---

## 5. Arquitectura de información y mapa de navegación

```
Cotejo
├── Hoy                      (home: hero + hechos de hoy + pulso de mercado)
│   ├── Hecho del día        (hero con Radar resumido)
│   ├── Hechos de hoy        (ordenados por Índice de Relevancia)
│   └── Comunicados sin cobertura   (silencio informativo)
├── Mercado de valores       (BVA, bonos, casas de bolsa, emisores)
├── Economía                 (BCP, tipo de cambio, bancos, comercio, agro)
├── Emisores y bancos        (fichas: cobertura + comunicados en una línea de tiempo)
├── Medios                   (ficha por medio: propiedad, velocidad, rectificaciones)
├── Radar                    (vista semanal del ecosistema: quién lidera, quién replica)
├── Buscar                   (búsqueda en toda la hemeroteca)
├── Datos abiertos           (CSV/JSON, API estática, licencia)
└── Metodología              (criterios, filtro temático, clasificación, límites)
```

Navegación móvil: barra inferior con 4 destinos (Hoy · Mercado · Economía · Buscar); Emisores,
Medios y Datos en el menú. Barra superior fija con el pulso de mercado, colapsable.

---

## 6. Radar de Cobertura (funcionalidad estrella)

### 6.1 Qué datos permiten hoy y cuáles no

| Quiero mostrar | ¿Posible con lo que se guarda? | Cómo |
|---|---|---|
| Qué medios cubrieron | Sí | `source` de cada nota del evento |
| Primer medio en publicar | **Sí** | mínimo de `published_at` |
| Medios que se sumaron y el desfase | **Sí** | diferencia de `published_at` |
| Palabras/conceptos por medio | Parcial | Solo sobre título + fragmento (≤300 caracteres): TF-IDF y entidades |
| Diferencias de enfoque | Parcial | Diferencias léxicas de titulares; no es análisis narrativo profundo |
| **Información que aportó cada medio** | **No** | No se guarda el texto completo (regla). Solo se puede mostrar "cifras y entidades nuevas en el titular/fragmento" |
| Impacto económico | Parcial | Solo montos citados en titulares (G. X millones); nunca estimaciones propias |

Honestidad de marca: el Radar mostrará **"aportes visibles en titular/fragmento"**, no "aportes del medio".
Prometer más sería engañoso.

### 6.2 Cinco propuestas (más una)

**A. Carriles de cobertura (swimlanes).** Eje X: tiempo. Un carril por medio. Un punto por nota,
con el primero resaltado y etiquetas de desfase ("+3 h 20 min"). Es la vista más legible y se puede
construir hoy con los datos existentes.
```
HECHO: Ueno Bank — 20 notas · 4 medios · 3 nov → 7 nov
              3 nov     4 nov     5 nov     6 nov     7 nov
ABC Color     ●─────────●●───●────●●─────────●●●──●────●●
Última Hora          ●(+14h)──────●──────●─────●─────●
Hoy                              ●(+31h)────────●
La Clave                                   ●(+2d 3h)
 ★ primero: ABC Color 3 nov 9:09    último en sumarse: La Clave +54 h
```

**B. Cascada de propagación.** Árbol: la nota inicial y las que le siguen, conectadas por similitud y
orden temporal ("esta replica a aquella"). Distingue *aporte original* de *eco*. Complejidad media.

**C. Mapa de calor medio × día.** Para hechos largos: filas = medios, columnas = días, intensidad = nº de
notas. Muestra quién sostiene la historia y quién la abandona. Muy bueno para móvil.

**D. Comparación léxica de titulares.** Dos o tres titulares lado a lado con las palabras distintivas
resaltadas ("detenido" / "aprehendido" / "queda en reclusión"). Se calcula por TF-IDF sobre titulares.

**E. Grafo del ecosistema (nivel semanal, no por hecho).** Nodos = medios; flechas = "suele publicar
después de" con grosor por frecuencia y etiqueta de desfase mediano. Produce el **Índice de liderazgo**
de cada medio. Requiere meses de datos y más fuentes; es V2/V3.

**F. Huella de cobertura (radial).** Un radar polar por emisor/tema: ejes = medios, radio = nº de notas
en 30 días. Sirve como firma visual compartible. Es el único que justifica el nombre "Radar" literal.

### 6.3 Recomendación
- **MVP:** A + D (carriles + comparación léxica), embebidos en cada página de evento. Datos ya disponibles.
- **V2:** C (calor) y F (huella) en fichas de emisor y de medio.
- **V3:** E (grafo) cuando haya 15+ medios y meses de historia.

### 6.4 Reglas de rigor del Radar
- "Primero" significa "primero **en las fuentes que Cotejo lee**", siempre con esa nota al pie. Un medio
  no leído puede haber publicado antes.
- Las fechas de RSS pueden ser de actualización, no de primera publicación. Mostrar un aviso de margen
  de error; no calcular desfases menores a 10 minutos.
- La BVA publica solo la fecha (sin hora): se excluye de los desfases horarios.
- Un hecho de un solo medio no genera Radar: muestra "cobertura única" explícitamente.

---

## 7. Nueva home: wireframes

### 7.1 Escritorio
```
┌───────────────────────────────────────────────────────────────────────────┐
│ COTEJO  Hoy  Mercado  Economía  Emisores  Medios  Radar  Datos   [Buscar⌕] │
├───────────────────────────────────────────────────────────────────────────┤
│ USD/PYG 6.266 ▲0,1%  │ S&P 500 …  │ Nasdaq …  │ BTC 73.697  │ ETH 2.063  │
│ Oro …  │ Petróleo …           datos con retraso · fuente y hora al hover  │
├───────────────────────────────────────────────────────────────────────────┤
│ HECHO DEL DÍA                                          Índice relevancia 91│
│ Ueno Bank: del colapso a la imputación                                    │
│ 4 medios · 20 notas · de 3 a 7 nov · cobertura sostenida                  │
│ ┌ Radar (carriles) ────────────────────────────────────────────────────┐ │
│ │ ABC      ●──●●──●──●●────●●●                                         │ │
│ │ ÚH          ●────●─────●───●                                         │ │
│ │ Hoy              ●────────●                                          │ │
│ └──────────────────────────────────────────────────────────────────────┘ │
│ Primero: ABC Color · 3 nov 9:09   Se sumaron: ÚH +14 h · Hoy +31 h        │
│ Qué dicen los titulares: "colapso" · "imputación" · "prisión preventiva"  │
├───────────────────────────────┬───────────────────────────────────────────┤
│ HECHOS DE HOY (por relevancia)│ COMUNICADOS SIN COBERTURA                 │
│ 87  Dólar bajo: pérdida agro  │ Hecho de relevancia · BANCOP SA · hace 2 d │
│     3 medios · hace 2 h  ●●●  │ Nueva emisión · Banco Atlas · 30 oct       │
│ 74  Petropar actualiza precios│ → 0 medios lo recogieron en 48 h           │
│     2 medios · hace 5 h   ●●  ├───────────────────────────────────────────┤
│ …                             │ TENDENCIAS (7 días)                        │
│                               │ Bancos: Ueno ▲▲ · Itaú · Atlas             │
│                               │ Temas: CDA ▲ · tipo de cambio ▲ · bonos    │
└───────────────────────────────┴───────────────────────────────────────────┘
```

### 7.2 Móvil (375 px)
```
┌────────────────────────┐
│ COTEJO            ⌕  ☰ │
│ USD/PYG 6.266 ▲ ‹→›    │  ← pulso, desliza horizontal
├────────────────────────┤
│ HECHO DEL DÍA     91   │
│ Ueno Bank: del colapso │
│ a la imputación        │
│ ABC●─●●─●●●            │  ← carriles simplificados
│ ÚH   ●──●───●          │
│ 4 medios · 20 notas    │
├────────────────────────┤
│ Hoy · Mercado · Econom.│  ← pestañas
│ 87 Dólar bajo…  ●●●    │
│ 74 Petropar…    ●●     │
├────────────────────────┤
│ Hoy  Mercado  Eco  ⌕   │  ← barra inferior
└────────────────────────┘
```

### 7.3 Página de evento (Radar completo)
```
← Hoy / Economía
Ueno Bank: del colapso a la imputación            [Seguir este emisor]
4 medios · 20 notas · 3 nov 9:09 → 7 nov 19:03 · Agrupado automáticamente
Índice de relevancia 91 ⓘ    Tono de la cobertura: negativo (68 %) ⓘ
─────────────────────────────────────────────────────────────────────
RADAR   [Carriles] [Calor] [Cascada]                  zoom ─●─────
  (swimlane interactivo; clic en un punto abre la nota original)
─────────────────────────────────────────────────────────────────────
CÓMO CAMBIÓ EL RELATO
 3 nov  "asociación de asegurados exige juicio político…"
 5 nov  "Fiscalía incluye a … en su investigación"
 7 nov  "Fiscalía imputa y pide prisión preventiva"
─────────────────────────────────────────────────────────────────────
CIFRAS CITADAS (con enlace)        ⚠ Cifras en conflicto: 1
 G. 373.838 millones · MEF ·  ABC · Hoy        US$ 355 millones · ÚH
─────────────────────────────────────────────────────────────────────
NOTAS (20)  ordenadas por hora · filtro por medio
 ABC Color · 3 nov 9:09 · "…"  [↗]
─────────────────────────────────────────────────────────────────────
Esto no es asesoramiento financiero · ¿Error en este hecho?
```

### 7.4 Ficha de emisor / banco
```
BANCOP SA                                  Seguir ☆
Línea de tiempo: comunicados BVA ■  notas de prensa ●
 oct ──■──────●──●────────■─────────●●●── nov
 Comunicados 12 · Notas 31 · Medios que lo cubren: 6 · Silencios: 2
```

---

## 8. Inteligencia financiera por noticia

Las reglas del proyecto (resúmenes solo con 2+ fuentes y enlaces; sin opinión) obligan a esta
formulación. Se sustituyen las inferencias libres por **señales mecánicas auditables**.

| Pedido | Implementación propuesta | Por qué así |
|---|---|---|
| ¿Por qué importa? | **Plantilla con hechos verificables**: "Involucra a *X* (BCP/BVA/banco), cita montos de *G. Y*, lo cubrieron *N* medios en *T* horas." No es prosa generada | Evita afirmaciones sin respaldo |
| Riesgos / Oportunidades | **No como texto generado.** Mostrar entidades mencionadas en cada polaridad **citando la frase del titular**. Una IA que afirme "quién se beneficia" sería opinión sin 2 fuentes **[DECISIÓN 3]** | Riesgo legal y de credibilidad |
| Sentimiento alcista/bajista | Renombrar **"Tono de la cobertura": positivo / negativo / neutral**, calculado sobre titulares con un léxico en español (público y versionado). No predice mercados | "Alcista/bajista" suena a recomendación de inversión |
| Impacto económico | Solo **montos que el propio medio cita**, con enlace. Nunca estimaciones propias | Mismo motivo |
| Resumen ejecutivo del día | **Extractivo**: los 3 hechos con mayor Índice y para cada uno una línea construida desde los titulares y sus enlaces, sin generar texto nuevo | Regla de 2 fuentes |
| Hechos sobre denuncias/candidatos | **Sin resumen**, como dicta la regla; solo carriles y titulares | Regla vigente |

### 8.1 Índice de Relevancia (0 a 100), cálculo exacto
Cada componente se normaliza entre 0 y 1. Los pesos son fijos, públicos y versionados.

```
R = 100 × ( 0,30·C + 0,20·V + 0,20·M + 0,15·F + 0,15·D )

C  Cobertura   = min(1, ln(1 + medios_distintos) / ln(1 + 8))
V  Velocidad   = min(1, notas_en_primeras_6_h / 6)
M  Materialidad= min(1, 0,5·[tiene término de bolsa]
                       + 0,3·[cita monto en G. o US$]
                       + 0,2·[menciona entidad vigilada: BCP, BVA, banco, emisor])
F  Frescura    = exp( − horas_desde_la_última_nota / 24 )
D  Diversidad  = tipos_de_medio_distintos / 5   (solo con medios revisados;
                 si no, D = 0 y los demás pesos se reescalan a 1)
```
- Se calcula en el ciclo de ingesta, sin IA, y se guarda con la versión de la fórmula.
- **No mide impacto de mercado.** Mide atención mediática y materialidad observable. Se dirá así en pantalla (ⓘ).
- Calibración: comparar el top diario con la selección de un editor humano durante 4 semanas y ajustar pesos; publicar cada cambio en `docs/decisiones.md`.

---

## 9. Pulso de mercado (solo gratuito)

Probado hoy desde esta máquina:

| Indicador | Fuente | Estado | Notas |
|---|---|---|---|
| USD/PYG | `open.er-api.com` (ExchangeRate-API, plan abierto) | **Funciona**: 6.266,41 al 2026-11-10 00:02 UTC | Actualización diaria; exige atribución. **No es la cotización oficial del BCP** (el sitio del BCP bloquea nuestro acceso). Etiquetar "referencia internacional" |
| Bitcoin, Ethereum | CoinGecko API pública | **Funciona**: BTC 73.697 USD, ETH 2.062,96 USD | Límites de uso y atribución; sin SLA |
| S&P 500, Nasdaq, oro, petróleo | Stooq (CSV) | **No verificado**: mis consultas devolvieron página de error | Alternativas por validar: FRED (clave gratuita, requeriría un secreto) o EIA. **[DECISIÓN 5]** |

Realismo técnico: el sitio es estático y el ciclo corre cada pocas horas (GitHub retrasa los cron).
No es "en vivo". Por eso toda cifra lleva hora de captura visible y el pulso nunca se presenta como tiempo real.
Alternativa: consulta desde el navegador del lector (CORS permitiendo) para criptos, con caché de 60 s.

---

## 10. Tendencias

- **Empresas y bancos más mencionados (7 días):** conteo de entidades de una lista pública
  (`sources/entidades.yaml`: bancos, casas de bolsa, emisores, instituciones). Mostrar variación frente a la semana previa.
- **Temas en crecimiento:** términos de `temas.yaml` con mayor aumento relativo de notas, con umbral mínimo para evitar ruido.
- **Sectores más cubiertos:** categorías sectoriales asignadas por palabras clave (bancario, agro, energía, comercio, bursátil).
- Todo se calcula con conteos, no con IA, y cada barra enlaza a las notas que la componen.

---

## 11. Enfoque en Paraguay y cobertura exterior

Prioridad (orden de peso en el Índice de Relevancia y en la portada):
1. BVA y mercado de valores, bonos corporativos, emisores, casas de bolsa.
2. BCP, tipo de cambio, sistema bancario.
3. Economía real: agro, comercio, energía, precios.
4. Nexos exteriores **con vínculo explícito a Paraguay** (Mercosur, Brasil, Argentina, EE. UU., China/Taiwán).
5. Cripto y *commodities* como contexto del pulso, no como noticias propias, salvo que mencionen a Paraguay.

Cobertura de EE. UU. y Latinoamérica sin vínculo con Paraguay **queda fuera**, por la decisión ya tomada y
documentada el 2026-11-10 ("descartar sin vínculos"). **[DECISIÓN 4]** si se quiere cambiarla.

---

## 12. Retención y *engagement* (sin *clickbait*)

| Mecanismo | Cómo funciona | Tiempo / recurrencia / profundidad |
|---|---|---|
| **Desde tu última visita** | Guarda en el navegador (`localStorage`) la última visita y marca qué hechos cambiaron. Sin cuentas | Recurrencia |
| **Seguir emisor/banco** | Lista local; la portada destaca sus hechos y comunicados | Recurrencia |
| **RSS/Atom por emisor y por tema** | Alertas sin correo ni cuenta (compatible con la regla de no enviar mensajes) | Recurrencia |
| **Fichas de emisor** | Todo sobre una entidad en una línea de tiempo | Profundidad |
| **Radar semanal** | Página fija cada lunes: quién lideró, qué hechos duraron más | Recurrencia |
| **Glosario contextual** | "CDA", "bono financiero", "hecho de relevancia" con definición breve al pasar el mouse | Tiempo y confianza |
| **Datos abiertos** | CSV/JSON diarios, citables | Alcance externo y backlinks |
| **Buscador de hemeroteca** | Búsqueda estática con filtros por medio, emisor y fechas | Profundidad |
| **Widget incrustable** | Un Radar para que medios o bancos lo pongan en sus sitios | Alcance |

Excluido por regla: boletín por correo, bots que envíen mensajes (Telegram/WhatsApp) y notificaciones *push*
**[DECISIÓN 6]**: son los mecanismos de retención más potentes y están prohibidos salvo pedido explícito.

---

## 13. Funcionalidades exclusivas (más de 10)

| # | Función | Valor (por qué FT, Bloomberg y Yahoo no la tienen) |
|---|---|---|
| 1 | **Radar de Cobertura** (carriles) | Muestra cómo se construyó la historia: quién, cuándo, desfase |
| 2 | **Silencio informativo** | Comunicados oficiales (BVA) que ningún medio recogió en 48 h. Los terminales no cruzan primarias con prensa local |
| 3 | **Cifras en conflicto** | Detecta montos distintos del mismo hecho entre medios (regex sobre titular/fragmento) y los muestra lado a lado |
| 4 | **Índice de liderazgo por medio** | Ranking mensual de quién publica primero y quién replica. Rendición de cuentas medible |
| 5 | **Detector de eco** | Distingue nota original de reproducción (similitud alta + desfase corto) |
| 6 | **"Cómo cambió el relato"** | Evolución del titular a lo largo de los días del hecho |
| 7 | **Comparador de titulares** | Dos o tres versiones del mismo hecho con diferencias léxicas resaltadas |
| 8 | **Ficha de emisor con comunicados + prensa** | Una línea de tiempo común que ningún portal ofrece para el mercado paraguayo |
| 9 | **Punto ciego por tipo de medio** | Qué *tipo* de medio no cubrió (ya diseñado; requiere revisión) |
| 10 | **Tono de cobertura por medio y emisor** | Cómo cubre cada medio a un mismo emisor a lo largo del tiempo, con léxico público |
| 11 | **Registro de rectificaciones** | Log público de correcciones detectadas, por medio. Criterio ya previsto en la metodología |
| 12 | **Conjunto de datos de cobertura abierto** | Un activo de datos citable, con licencia abierta |
| 13 | **Calendario de la BVA** | Nuevas emisiones y hechos de relevancia ordenados en el tiempo con cobertura asociada |

Cada función es **mecánica y auditable**. Ninguna depende de que un modelo "opine".

---

## 14. Tecnología (todo gratuito, abierto, autohospedable)

### 14.1 Recomendación: **evolucionar, no migrar**

| Capa | Propuesta del encargo | Recomendación | Motivo |
|---|---|---|---|
| Frontend | Next.js + React + TS + Tailwind | **Mantener Astro** + islas interactivas en React/Preact + TypeScript; Tailwind opcional | Sitio estático = 0 servidores, 0 costo, SEO y velocidad. Next.js exige servidor o Vercel y duplica trabajo. Solo el Radar necesita JS |
| Backend/ORM | PostgreSQL + Prisma | **PostgreSQL (Neon hoy, autohospedable después) + Python existente**; sin Prisma | La ingesta y el análisis ya están en Python; un ORM en JS aportaría otra capa sin beneficio |
| Gráficos | ECharts + Lightweight Charts | **SVG propio para carriles** (control total, 0 KB de librería) y **Lightweight Charts** para USD/PYG; ECharts solo para el mapa de calor si hace falta | El Radar es una visual a medida |
| Búsqueda | MeiliSearch | **Pagefind** (índice estático, sin servidor) en MVP; **Meilisearch** cuando haya VPS | Pagefind mantiene el costo en cero y funciona sobre Pages |
| IA | Llama / DeepSeek / Mistral / Qwen | **Sin generación libre en MVP.** Para V2: modelos pequeños (Qwen/Mistral cuantizados con llama.cpp u Ollama) **solo para extracción estructurada** (entidades, cifras) validada con reglas contra el texto de origen | Ver 14.2 |
| Contenedores | Docker | **Docker Compose ya existe** (`ops/`) para autohospedaje; GitHub Actions + Pages siguen siendo el despliegue por defecto | Dos caminos: gratis en la nube o autohospedado |

### 14.2 Sobre la IA
- Un *runner* gratuito de GitHub tiene 2 vCPU y 7 GB de RAM: corre modelos pequeños, lento. Un modelo de 7B sin GPU exige un VPS de pago o un equipo propio.
- Texto generado libremente choca con la regla de "afirmar solo lo confirmado por 2 fuentes con enlaces". Se usará IA para **extraer**, nunca para **afirmar**.
- Cada extracción se verifica por reglas (la cifra o entidad debe aparecer literalmente en el titular/fragmento) y se descarta si no.

---

## 15. Sistema de diseño

**Dirección:** *Papel de mercado*. Conserva la identidad editorial (serif en titulares, tinta sobre papel, acento
ladrillo) y le suma densidad de datos: números tabulares, líneas finas y un instrumento visual propio (el carril).
No es Yahoo Finance (cuadrícula de tarjetas con gráficos genéricos) ni un portal (fotos y banners).

### 15.1 Tokens
```
Color (claro)   papel #F3EFE4  superficie #FBF8F0  tinta #1B1A17  gris #5C584D
                regla #CFC8B4  acento #B2331D (ladrillo)  foco #1F5FBF
Color (oscuro)  papel #17161A  superficie #1F1E22  tinta #ECE7DA  gris #A39E90
                regla #3A3730  acento #EE7A62
Semánticos      positivo #2F7D4F  negativo #B2331D  neutral #5C584D
                (el tono de cobertura nunca usa solo color: lleva icono y texto)
Medios (carriles) paleta categórica segura para daltonismo (tipo Okabe-Ito),
                asignada de forma estable por medio y NUNCA ligada a la clasificación editorial
Tipografía      titulares: serif (Iowan/Charter/Georgia), peso 700, 1.15
                cuerpo/UI: sans del sistema (Inter si se aloja), 16 px / 1.5
                datos: monoespaciada con numerales tabulares (Cascadia/ui-monospace)
                escala 12 · 14 · 16 · 20 · 28 · 40
Espaciado       base de 4 px: 4 · 8 · 12 · 16 · 24 · 32 · 48 · 64
Radio/borde     radio 2 px (editorial, casi recto); filetes de 1 px; doble filete en el mástil
Movimiento      150 ms, solo opacidad/posición; respeta prefers-reduced-motion
Ancho           contenido 72 rem; lectura 38 rem; carriles hasta 80 rem
Breakpoints     480 · 768 · 1100
```
- **Contraste:** todos los pares texto/fondo ≥ 4,5:1 (AA); el acento sobre papel se verifica antes de fijarlo.
- **Accesibilidad:** el Radar debe tener equivalente en tabla (carriles → lista ordenada con horas), navegación por teclado entre puntos, `aria-label` por nota, y resumen en texto ("ABC publicó primero; Hoy se sumó 31 h después").

### 15.2 Componentes recomendados
| Componente | Función |
|---|---|
| `MarketPulse` | Barra superior con cifras, hora de captura y fuente |
| `HeroFact` | Hecho del día con Radar resumido y metadatos |
| `FactRow` | Fila de hecho: Índice, título, medios, hace-cuánto, mini-carril (sparkline de puntos) |
| `CoverageLanes` | Carriles interactivos (SVG) con zoom, primero resaltado y desfases |
| `LexicalDiff` | Comparador de titulares con palabras distintivas |
| `NarrativeTimeline` | "Cómo cambió el relato" |
| `FigureTable` | Cifras citadas con medio y enlace; marca de conflicto |
| `RelevanceBadge` | Índice 0-100 con popover de fórmula |
| `ToneMeter` | Tono de cobertura con icono + texto |
| `EntityCard` | Ficha de emisor/banco con línea de tiempo |
| `SilenceList` | Comunicados sin cobertura |
| `SourceChip` | Medio con propiedad y estado de revisión |
| `TrendBars` | Barras de tendencia con enlace a las notas |
| `CommandSearch` | Búsqueda (Ctrl+K) |
| `MethodNote` | Nota metodológica contextual (ⓘ) |

---

## 16. Roadmap

### MVP (4 a 6 semanas): arreglar, activar y mostrar el Radar
1. **P0:** corregir el agrupamiento de la BVA (cada comunicado es su evento propio y no se une a otros); recalcular títulos de evento (nota más reciente o más representativa); ordenar por frescura + relevancia; ocultar avisos internos y reemplazarlos por una nota metodológica discreta.
2. **Ampliar fuentes** (sección 17).
3. **Carriles de cobertura** y comparación léxica en cada evento.
4. **Home nueva:** hecho del día, hechos por Índice, pulso con las 3 fuentes verificadas.
5. Metadatos `og:*`, favicon, sitemap, Atom propio, Pagefind.
6. Clasificación de medios **revisada** y punto ciego encendido.

### V2 (2 a 3 meses): inteligencia de cobertura
Índice de Relevancia publicado, tono de cobertura, cifras en conflicto, silencio informativo, fichas de emisor,
fichas de medio, índice de liderazgo, tendencias, calor y huella, RSS por entidad.

### V3 (6 meses o más): ecosistema
Grafo del ecosistema, detector de eco, extracción con modelo local validada, API y datos abiertos con licencia,
widget incrustable, Meilisearch (si hay servidor), registro de rectificaciones.

---

## 17. Prioridades (impacto frente a complejidad)

| Mejora | Impacto | Complejidad | Prioridad |
|---|---|---|---|
| Corregir mega-evento BVA y títulos obsoletos | Muy alto | Baja | **1** |
| Orden por frescura/relevancia | Alto | Baja | **2** |
| Carriles de cobertura | Muy alto | Media | **3** |
| Ampliar fuentes (sitemaps de noticias, nuevas RSS, permisos) | Muy alto | Media-alta | **4** |
| Clasificación de medios revisada | Alto | Media (trabajo editorial) | **5** |
| Home con hero + pulso | Alto | Media | 6 |
| Pagefind, `og:*`, Atom, sitemap | Medio | Baja | 7 |
| Silencio informativo | Alto | Media | 8 |
| Índice de Relevancia | Medio-alto | Media | 9 |
| Comparador léxico | Medio | Media | 10 |
| Fichas de emisor | Alto | Alta | 11 |
| Cifras en conflicto | Alto | Alta | 12 |
| Tono de cobertura | Medio | Media | 13 |
| Grafo de ecosistema | Medio | Alta | 14 |
| IA para extracción | Medio | Alta | 15 |

**Ampliar fuentes** es el cuello de botella real. Vías por explorar y validar: *sitemaps de noticias*
públicos (diseñados para ser leídos por bots; no verificados en La Nación), nuevas RSS de secciones de economía,
comunicados del BCP y de la SIV por vías permitidas, y **solicitar permiso a los medios** (lo hace una persona;
el proyecto no envía correos).

---

## 18. Métricas de éxito

| Nivel | Métrica | Meta a 6 meses |
|---|---|---|
| Estrella | **Hechos con Radar abierto por usuario semanal** | ≥ 1,5 |
| Producto | % de visitas que abren un hecho | ≥ 55 % |
| Producto | Profundidad (hechos por visita) | ≥ 2,5 |
| Retención | Retorno a 7 días / a 30 días | ≥ 25 % / ≥ 12 % |
| Retención | Visitas con "desde tu última visita" | ≥ 30 % de recurrentes |
| Datos | Medios activos con cobertura legal verificada | ≥ 15 |
| Datos | Hechos con 3+ medios | ≥ 40 % |
| Calidad | Tasa de reportes de error por 1.000 hechos | < 5, con respuesta en 48 h |
| Calidad | Precisión del agrupamiento (muestra humana mensual) | ≥ 90 % |
| Alcance | Citas externas / descargas del conjunto de datos | creciente mes a mes |

Medición **sin cookies de seguimiento**: analítica autoalojada y agregada (por ejemplo, Umami o Plausible CE
autohospedada) o conteo en servidor; sin datos personales.

---

## 19. Cómo convertir a Cotejo en la referencia nacional

1. **Ser la fuente de datos de cobertura más completa**: quien necesite saber "cómo se contó esto" lo busca aquí. Cobertura de 15+ medios y de las fuentes primarias (BVA, BCP, SIV).
2. **Metodología pública y auditable**: filtro, índice, léxico y clasificación en repositorio; cada cambio con fecha y motivo.
3. **Alianzas con tres tipos de actores**: facultades de economía y periodismo (validación), la BVA y el BCP (datos primarios), y medios (derecho a réplica y rectificación visible).
4. **Hitos de reputación**: "Radar semanal" citado por medios; conjunto de datos abierto usado en investigaciones.
5. **Sostenibilidad con cortafuegos editorial**: subvenciones y donantes sin vínculo con entidades cubiertas; si hay API o suscripción institucional, divulgar quién paga y vedar influencia sobre la cobertura. **No** aceptar financiación de bancos, casas de bolsa o emisores que Cotejo cubre sin un mecanismo de independencia documentado.
6. **Marco legal**: el modelo "título + fragmento corto + enlace" es el límite prudente; ampliar a texto completo requeriría acuerdos con cada medio.

---

## 20. Decisiones que necesito de ti

| # | Decisión | Mi recomendación |
|---|---|---|
| 1 | ¿Evolucionar sobre Astro + Python + Neon en vez de migrar a Next.js + Prisma + Meilisearch? | **Evolucionar**: gratis, rápido y sin servidor |
| 2 | ¿Corregir ya los defectos P0 (mega-evento BVA y títulos obsoletos) antes de cualquier rediseño? | **Sí, de inmediato** |
| 3 | "Quién se beneficia / riesgos / oportunidades": ¿solo como entidades citadas del titular, y no como texto generado? | **Solo citadas** (respeta la regla de 2 fuentes) |
| 4 | ¿Mantener fuera la información de EE. UU./Latinoamérica sin vínculo a Paraguay? | **Mantener** salvo como pulso |
| 5 | Pulso de mercado: ¿registro una clave gratuita de FRED (o similar) para índices y petróleo? Tendrías que crearla y guardarla como secreto | **Sí**, tras probar la cobertura gratuita |
| 6 | ¿Autorizas una vía de alertas activa (boletín o bot)? Hoy está prohibida | **No por ahora**: usar RSS por entidad |
| 7 | "Sentimiento" → ¿renombrarlo a **"tono de la cobertura"** y no usar "alcista/bajista"? | **Sí** |
| 8 | ¿Texto completo de notas para mejorar el análisis? Hoy prohibido por regla | **No**: riesgo legal y de neutralidad |
| 9 | Fuentes nuevas: ¿exploro sitemaps de noticias y RSS por sección, y preparo un borrador de solicitud de permiso para que tú lo envíes? | **Sí** |
| 10 | ¿Quién revisa y firma la clasificación de medios? | Una persona con criterio editorial y evidencia citada |
