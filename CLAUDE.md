# Cotejo

Agregador open source (AGPL-3.0) de noticias de Paraguay. Agrupa las notas por hecho, muestra cómo lo cubrió cada medio y qué tipo de medios no lo cubrió (punto ciego). Stack: Python 3.11+ (usar `py`), PostgreSQL + pgvector, sitio estático Astro, cron. Entorno: Windows. Despliegue: VPS con Docker Compose.

## REGLAS DE AHORRO
- Responde en español, corto. Sin preámbulos. Al final de cada paso, máximo 3 líneas.
- No leas archivos enteros si sirve grep o un rango de líneas. No me muestres el código que escribes: solo nombre del archivo y qué hace.
- Filtra salidas largas; muéstrame solo errores o una tabla breve.
- Una fase a la vez. Al terminar cada fase: commit local con mensaje corto, detente y espera mi "sigue".
- No instales dependencias ni crees archivos fuera de lo pedido. No agregues funciones extra.
- Si algo falla dos veces seguidas, detente y dime el error en vez de seguir intentando.

## REGLAS DE PRODUCTO (no negociables)
- Se guarda solo título, fragmento de máx. 300 caracteres, enlace y fecha. Nunca el texto completo de las notas.
- Respetar robots.txt, pausa de 2 s por sitio, user-agent propio y RSS antes que scraping.
- Los resúmenes solo afirman lo confirmado por al menos 2 fuentes independientes. Cada afirmación lleva sus enlaces; si no se puede respaldar, no hay resumen y solo se muestran titulares.
- Eventos sobre denuncias, acusaciones o candidatos: sin resumen generado, solo titulares y enlaces.
- Todo resumen se etiqueta "generado automáticamente". Debe existir cola de reportes de error y forma rápida de despublicar un evento.
- La clasificación de medios vive en un YAML público con criterios documentados (propiedad, vínculos, línea editorial, rectificaciones). Eje: oficialismo / independiente / crítico del gobierno / público / fuente primaria. Nada de eje izquierda-derecha automático.

## REGLAS DE SEGURIDAD
- Nunca envíes correos ni mensajes: no configures SMTP, no uses conectores de email, no escribas código que los envíe salvo que yo lo pida explícitamente.
- Antes de leer, copiar, modificar o ejecutar algo FUERA de la carpeta del proyecto, pregúntame y espera mi respuesta.
- Siempre pregunta antes de tocar: .env, claves, tokens, credenciales, carpetas personales (Documentos, Descargas, Escritorio), navegador, ~/.ssh, variables de entorno del sistema, registro de Windows.
- No hagas push ni publiques en ningún servicio sin mi confirmación.
- Antes de instalar cualquier dependencia o skill, dime qué es y de dónde viene. No uses paquetes sin mantenimiento reciente.
- Ante la duda sobre si algo es sensible, pregunta.

## REGLAS DE DOCUMENTACIÓN
- Todo cambio se registra en docs/CHANGELOG.md (fecha, qué cambió y por qué), en una o dos líneas.
- Cada decisión importante va en docs/decisiones.md con el motivo.
- Cada módulo tiene un docstring corto: qué hace y qué no hace.
- Toda regla de neutralidad o seguridad editorial queda en docs/metodologia.md, en lenguaje claro para un lector no técnico.
- Documenta mientras construyes, no al final.
