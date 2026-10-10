# Colaborar sin comprometer seguridad

Se aceptan contribuciones sobre tests, accesibilidad, UX, documentación, internacionalización, fuentes verificables y privacidad; ninguna contribución habilita la plataforma para emergencias reales automáticamente.

1. Abrí un issue explicando el problema y si existe un organismo oficial responsable.
2. Evitá subir datos reales de damnificados, fotografías con EXIF, geolocalizaciones precisas, teléfonos, contraseñas, logs sensibles o claves de Google Maps.
3. Implementá cambios pequeños con tests reproducibles: `python -m unittest discover -s tests -p 'test_*.py' -v`, `node --test tests/test_ui.cjs`, `node --check app/app.js`.
4. Diferenciá **datos posteriores** del **sistema de alerta temprana**. Nunca inventes latencias o garantías.
5. Requerimos consentimiento y fuente autorizada para integrar alertas y servicios públicos. No se aceptan apariencias que simulen afiliación a Apple, Samsung, Google, NOAA, USGS, SINAPROC o el 911.

Los PR se revisan antes de fusionarse. Mantener licencia MIT y atribuciones de terceros. No reutilizar código de Simworld sin auditoría de licencia y autorización expresa.
