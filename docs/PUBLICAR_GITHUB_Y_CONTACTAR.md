# Guía de publicación y presentación institucional (10 de octubre de 2026)

## 1. Publicar la fuente en un repositorio SEPARADO

Crear el repositorio en una sola pantalla con este enlace oficial, que precarga propietario, nombre, descripción y visibilidad:

https://github.com/new?owner=ruminui&name=alerta-solidaria&description=Open-source+experimental+community+emergency+map+-+NOT+an+early+warning+or+dispatch+system&visibility=public

- Confirmar que el propietario es `ruminui`, repositorio `alerta-solidaria` y visibilidad `Public`.
- **Marcar "Add a README file"** para crear rama `main`. No activar templates automáticos ni licencias extra, porque el ZIP ya contiene README y LICENSE.
- Hacer clic en **Create repository**. Esa aprobación sólo puede darla el propietario autenticado.
- Informar el enlace resultante al asistente. Con el repositorio creado, el conector GitHub podrá crear los nuevos archivos y actualizar el README inicial, sin tocar Simworld.
- El repositorio **sólo divulga código experimental**; no significa que el servicio esté desplegado ni sea seguro para situaciones reales.

Este entorno no dispone del permiso `create repository` en el conector de GitHub ni de GitHub CLI autenticado. No se declara un repositorio creado si no existe.

## 2. Apple: feedback del iPhone, no entrega no solicitada del software

Apple acepta feedback sobre características existentes en https://www.apple.com/feedback/iphone/ y solicitudes técnicas de API en https://developer.apple.com/feedback-assistant/. La política https://www.apple.com/legal/intellectual-property/policies/ideas.html indica que Apple no acepta proyectos/ideas completas no solicitadas. **No adjuntar el ZIP** ni atribuir al fabricante compromisos que no hizo.

Mensaje breve: `docs/FEEDBACK_APPLE_PUBLICO_ES.md`.

## 3. Samsung: comentarios Galaxy mediante Members

Samsung informa https://developer.samsung.com/faq?ct=CT011000 que el soporte Developer **no acepta ideas no solicitadas** y recomienda Samsung Members para feedback de teléfonos. Entrada argentina https://www.samsung.com/ar/apps/samsung-members/. Texto breve: `docs/FEEDBACK_SAMSUNG_PUBLICO_ES.md`.

## 4. Entrega real del código a fabricantes

Esperar a que exista contacto institucional que expresamente invite a enviar repositorios y confirme condiciones. Solo entonces remitir enlace GitHub público, licencia MIT, alcance y pruebas. Registrar fecha, canal, ID/ticket de recepción, contacto y respuesta en `docs/REGISTRO_ENTREGA.csv`.

Estados: `PUBLICACION_PENDIENTE`, `FEEDBACK_PENDIENTE`, `RECEPCION_NO_CONFIRMADA`, `ALIANZA_NO_ACORDADA`.
