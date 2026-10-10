# iPhone / SwiftUI — Integración nativa inicial

Fuente SwiftUI `@main` + `WKWebView` con dominio HTTPS aprobado. No hay `.xcodeproj` ni IPA ni App Store submission porque Xcode, Apple Developer, equipo de firma, perfil y Mac no están disponibles aquí.

1. En Xcode para macOS: File → New Project → iOS App, SwiftUI, bundle ID propio del proyecto.
2. Añadir ambos archivos `.swift`; establecer una URL real HTTPS en `CommunityWebView.serviceURL`.
3. Info.plist: definir `NSLocationWhenInUseUsageDescription` explicando que el usuario selecciona voluntariamente ubicación para un pedido de ayuda.
4. Añadir capacidades, accesibilidad y gestión de alertas **solo después de revisión de seguridad**. Las notificaciones críticas requieren entitlement aprobado por Apple; no se incluye tal derecho aquí.
5. Evaluar `WKUIDelegate` para permiso geolocalización y límites de navegación en Xcode y teléfonos físicos; sin ese gate no distribuir.

La interfaz de la PWA se ajusta con botón `Estilo iPhone`. Esta implementación nativa es una base de integración, no una app de emergencia certificada.
