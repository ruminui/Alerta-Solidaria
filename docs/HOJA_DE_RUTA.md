# Roadmap y decisiones de lanzamiento

| Etapa | Salida | Estado / requisito |
|---|---|---|
| A. Prototipo local verificable | Python/SQLite, PWA dos estilos, mapa, sala geográfica, enlace a WhatsApp, registro USGS | **Implementado y con tests unitarios**; no prueba de uso real multiusuario público |
| B. GIS y backend seguro | Postgres/PostGIS, cuentas verificadas, moderación 24/7, chat realtime, centro de ayuda, privacidad | Pendiente |
| C. Integración cartográfica Google | Proyecto Maps, clave HTTP referrer restringida, presupuesto y límites de consumo | Código listo para clave, no configurada |
| D. Alertas informativas push | APNs / FCM / consentimiento, fuentes oficiales verificadas y fallback | Pendiente |
| E. Alertas anticipadas reales | Integración EEW territorial donde existe, CAP, acuerdos Protección Civil | Bloqueada por convenios, equipos y certificación |
| F. Clientes nativos | Android (Jetpack Compose) e iOS (SwiftUI), widgets, permisos, accesibilidad | Documentos de integración y puentes fuente incluidos; compilación pendiente |
| G. Donaciones auditadas | Inventario ONG / necesidades / asignación / voluntarios / cadena de custodia | Pendiente; no pagos sin revisión jurídica |
| H. Fabricantes y despliegue | Revisiones y pruebas hardware, OEM APIs, Cell Broadcast si Estado lo aprueba, tiendas | Bloqueada por aceptación institucional y equipo de operaciones |

## Requisitos de aceptación «apto para emergencias»

1. Ninguna notificación sin evento de fuente oficial firmada y política geográfica comprobada.
2. Menor que 5 segundos p95 de entrega **solo** cuando la red y acuerdos permiten medirlo (objetivo, no promesa), trazado desde detección; nunca usar USGS feed público como fuente EEW.
3. Confirmación de entrega cuando exista, métricas de error y ejercicios con personas reales.
4. Funcionamiento de emergencia no dependiente de WhatsApp ni de tiles Google Maps.
5. Usuarios vulnerables no expuestos por ubicación exacta, nombre o patología.
6. Alertas accesibles, locuciones locales, vibración y texto claro; canal offline/mesh evaluado.
7. Contrato con autoridades y operadores que no confunda el chatbot comunitario con el 911.
8. No avanzar si los sistemas de moderación y protección de datos están incompletos.

## Repositorio independiente

Nombre sugerido: `ruminui/alerta-solidaria` **nuevo repositorio público y separado**. Ningún commit al repo Simworld/Exoinovaciones. Subir sólo esta carpeta, sin `.env`, claves de Google, DB ni datos personales. El control de origen se realiza con script `deploy/publicar_nuevo_repo.sh` tras crear y autenticar el repositorio (ver README).
