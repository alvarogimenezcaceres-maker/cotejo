# Metodología

## Fuentes y recolección
- Solo se guarda título, un fragmento de hasta 300 caracteres, el enlace y la fecha. Nunca el texto completo.
- Se respeta el robots.txt de cada sitio: si bloquea nuestro lector, ese medio no se ingiere.
- Se usa RSS; hay una pausa de 2 segundos entre pedidos al mismo sitio.

## Clasificación de medios
- Eje: oficialismo, independiente, crítico del gobierno, público, fuente primaria. No hay eje izquierda-derecha.
- Criterios: propiedad, vínculos, línea editorial y rectificaciones.
- Mientras una clasificación figure como "revisado: false" es provisional y no se muestra al público.

## Qué muestra el sitio
- Solo hechos con al menos dos notas. Sin resumen: titulares, fragmentos y enlaces a cada medio.
- La agrupación por hecho es automática (similitud de texto) y puede equivocarse; cada hecho dice que fue agrupado automáticamente.
- Un evento se puede despublicar de inmediato si alguien reporta un error.

## Qué temas cubre Cotejo
Cotejo se centra en la economía de Paraguay, con prioridad al mercado de valores: la Bolsa de Valores de Asunción, las casas de bolsa, bonos, emisores, fondos, la Superintendencia de Valores y el Banco Central, además de banca, comercio, producción, precios y tipo de cambio. La política solo entra cuando tiene un componente económico.
Al recolectar, una nota se guarda solo si su título o fragmento menciona temas de bolsa o de economía. Las noticias sobre otros países se guardan únicamente si también mencionan a Paraguay.
La lista completa de palabras está en `sources/temas.yaml` y es pública. El filtro es simple y puede dejar pasar o perder alguna nota; si detectas un error, repórtalo y se ajusta la lista.
Este filtro decide qué se recolecta. No cambia las reglas de neutralidad: los hechos sobre denuncias, acusaciones o candidatos se muestran solo con titulares y enlaces, sin resumen generado.
La portada agrupa los hechos en dos secciones: Mercado de valores y Economía. Un hecho va en Mercado de valores si alguna de sus notas menciona términos de bolsa. En Economía se listan hechos cubiertos por al menos dos medios distintos; en Mercado de valores basta uno, porque hay pocas fuentes que lo cubren.

## Qué fuentes no se usan
Cotejo respeta el `robots.txt` de cada sitio. No se leen Reddit ni X (Twitter): sus reglas prohíben el acceso automatizado, y además sus publicaciones no son verificables con la regla de dos fuentes independientes.
