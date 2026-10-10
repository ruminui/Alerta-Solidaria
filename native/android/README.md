# Galaxy / Android — Código fuente de integración

Proyecto Gradle Kotlin para Android WebView (API 26+) con geolocalización por permiso runtime y enlaces externos. No implementa Cell Broadcast, el sistema Google Earthquake Alerts ni sirenas del sistema. No se incluye Google Maps SDK nativo; el mapa se renderiza en la PWA hospedada por el equipo.

Antes de compilar: configurar `SERVICE_URL` con **HTTPS de servidor real** en `app/build.gradle.kts`, instalar Android Studio/SDK, Gradle wrapper adecuado, compilar y firmar; usar Android Remote Test Lab de Samsung en caso de disponibilidad. No configurar WebView para HTTP público. No dar por aprobado el APK sin pruebas en teléfonos reales.

A futuro: Jetpack Compose, geofencing con permisos granulares, push FCM y canales Android, foreground/background policies, R8, network security config, deep links firmados, publicación en Galaxy Store/Google Play. Sólo integrar con alerta sísmica del sistema si el fabricante publica APIs y autoriza.
