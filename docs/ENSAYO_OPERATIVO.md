# Ensayos seguros y barreras para un prototipo de emergencias

## Uso permitido
- Piloto local con cuentas ficticias y zonas ficticias, sin usarlo para pedir rescatistas.
- Verificar que cualquier pantalla de publicaciones indique que NO contacta a servicios de emergencia.
- No subir coordenadas de personas reales ni domicilios.

## Casos esenciales antes de release
1. Desconexión total: aparece guía estática ya cacheada; solicitudes, chat y fuentes no aseguran funcionar offline.
2. Sismo USGS: los tiempos/ubicaciones son registros posteriores, no alerta anticipada. Simular con fixture sintético sin reenviar públicamente.
3. Publicación de más de 72 h deja de aparecer; mensaje de más de 24 h también; en la próxima versión definir borrado físico y retención.
4. Sin Google Maps key, OSM como respaldo; proveedores de tiles pueden bloquear tráfico. Ninguno es mapa de evacuación autorizado.
5. Ubicación aproximada; corroborar que no se exponen coordenadas exactas ni PII en APIs públicas.
6. Denuncia de contenido falso: reportes requieren moderación humana inexistente; jamás publicar sin esa capacidad.
7. Prueba de dispositivos Android/iPhone reales con fuente tipográfica grande, VoiceOver/TalkBack, conexión lenta, modo ahorro de batería.
8. No lanzar notificación de evacuación ni sirena crítica sin una fuente oficial autorizada y verificada.
9. Ensayar APNs/FCM, push VAPID o Bluetooth/mesh sólo con autorizaciones, datos sintéticos y consentimiento.
10. Verificar legalidad local y relaciones con Protección Civil y operadoras antes de prometer funcionalidad de emergencia.

## Cómo evaluar eficacia, no sólo interfaz
- Precisión/geofencing en polígonos, edad de alertas, porcentaje de entrega, falsos positivos, latencia p50/p95, batería, acceso sin conectividad.
- Registrar fuente y firmar mensajes, deduplicación, caducidad y revocación de alertas, pruebas con operadores.
- Redundancia fuera de Google Maps y WhatsApp; push común no es Cell Broadcast y no garantiza activación rápida.
