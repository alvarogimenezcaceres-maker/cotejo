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
Cotejo se centra en la política y la economía de Paraguay y en sus relaciones con otros países y organismos (Mercosur, Brasil, Argentina, Estados Unidos, Taiwán, China, Itaipú, entre otros).
Al recolectar, una nota se guarda solo si su título o fragmento menciona instituciones o actores políticos de Paraguay, o temas generales de política y economía. Las noticias sobre otros países se guardan únicamente si también mencionan a Paraguay.
La lista completa de palabras está en `sources/temas.yaml` y es pública. El filtro es simple y puede dejar pasar o perder alguna nota; si detectas un error, repórtalo y se ajusta la lista.
Este filtro decide qué se recolecta. No cambia las reglas de neutralidad: los hechos sobre denuncias, acusaciones o candidatos se muestran solo con titulares y enlaces, sin resumen generado.
La portada agrupa los hechos en tres secciones: Política, Economía y Nexos internacionales. Un hecho va en "Nexos internacionales" si menciona a un actor extranjero y a Paraguay; si no, va donde haya más palabras coincidentes. Solo se listan hechos cubiertos por al menos dos medios distintos.
