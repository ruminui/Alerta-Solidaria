# Manual del operador e integrador — Alerta Solidaria

**Estado NO_GO para emergencias públicas.** Piloto local, sin alertas tempranas, sin rescatistas conectados ni fabricantes asociados.

## Instalación local para pruebas
Se necesitan Python 3.11+, Node 18+ y navegador moderno. Ejecutar desde raíz:
1. python -m unittest discover -s tests -p 'test_*.py' -v
2. node --test tests/test_ui.cjs
3. node --check app/app.js
4. python backend/server.py
5. Abrir http://127.0.0.1:8765 (sólo en la computadora de desarrollo).
No abrir puertos ni utilizar datos reales de damnificados. Mapa OSM y USGS requieren internet. Google Maps precisa Maps JavaScript API, clave restringida por dominio/API y facturación según https://developers.google.com/maps/documentation/javascript/get-api-key

## Comprobación de funcionalidades
Crear usuario ficticio; seleccionar zona; publicar ofrecimiento/solicitud sintética; comprobar marcador redondeado; consultar chat zonal; abrir enlace de WhatsApp SIN enviarlo; resolver publicación; exportar cuenta, salir, reingresar y borrar cuenta. Consultar sismos USGS sólo como registro posterior; verificar error visible si fuente cae. Revisar purga de pedidos de 72 h, chat de 24 h y reportes de 30 días. Las copias de seguridad deben tener ciclo propio.

## Android / iPhone
Android: ver native/android y docs/SAMSUNG_INTEGRATION_PLAYBOOK_EN.md. Código WebView, sin APK firmado ni prueba física.
iOS: ver native/ios y docs/APPLE_INTEGRATION_PLAYBOOK_EN.md. Código SwiftUI/WebKit; necesita Mac, Xcode, proyecto válido, cuenta de desarrollador, URL HTTPS, firma y TestFlight antes de cualquier distribución.
Aprobación de avisos privilegiados, Cell Broadcast y EEW requieren acuerdos con el sistema y autoridades.

## GATES de producción obligatorios
- Validación independent de seguridad, datos personales, accesibilidad y anti-fraude.
- Contratos con protección civil/ONG y operadores; credenciales verificables.
- Infraestructura HTTPS resistente, alertas falsas bloqueadas, moderación humana, auditorías y simulacros.
- Dispositivos Android/iPhone reales; batería/roaming/offline, latencia, datos corruptos, fallas y rollback.
- Documentar distribución y permisos por marca; no afirmar aceptación sin comprobante.
**Resultado actual:** código de estudio + pruebas locales, NO servicio de emergencias.
