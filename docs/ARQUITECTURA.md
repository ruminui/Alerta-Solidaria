# Arquitectura de referencia (dos capas independientes)

## 1. Estado implementado en este ZIP

```text
Web/PWA accesible (Galaxy CSS / iPhone CSS)
    ├─ geolocalización con consentimiento
    ├─ Google Maps JS si hay API key restringida / Leaflet OSM respaldo
    ├─ wa.me (compartir, no gestión de grupos)
    ├─ pedidos y ofrecimientos / marcadores / chat por cuadrícula ~11 km
    └─ catálogo USGS público (datos observados, NO alerta anticipada)
          ↓ API same-origin, token sesión
Python stdlib HTTP + SQLite WAL (solo piloto local)
    ├─ sesiones con scrypt y token SHA-256 almacenado
    ├─ posts y chat
    ├─ ubicaciones exactas privadas en BD / públicas a 0,01º
    └─ reportes de abuso pendientes de tratamiento humano
```

## 2. Arquitectura objetivo de producción (no implementada)

```text
AUTORIDADES / DATOS
CAP oficial con firma, USGS, tsunami.gov, redes geofísicas regionales,
operadores WEA/Cell Broadcast, autoridades de protección civil
                       ↓ verificación firma / fuente / tiempo
Ingesta geoespacial: consumidores redundantes, normalización de eventos,
validación por jurisdicción, detección duplicados, niveles de confianza.
                       ↓ cola durable y mensajería idempotente
GEOTARGETING / POLICY
Polígonos con PostGIS, zonas vulnerables, ETA de ondas (solo con fuentes EEW),
política de severidad, supresión de notificaciones falsas, pruebas de 2 personas.
                       ↓
DELIVERY
Cell Broadcast (solo operadores/Estado) + APNs iOS + FCM Android + SMS + RCS
+ web push + Sirenas públicas + radio + satelital cuando exista convenio.
                       ↓
COMUNIDAD y LOGÍSTICA
Mapa Google Maps / app Android / app iOS / portal web, chat por zona,
SOS con ubicación cifrada, despacho a operadores verificados, donaciones de
insumos, inventario / puntos de entrega y cadena de custodia.
                       ↓
TRANSPARENCIA Y CONTROL
logs firmados, latencia y confiabilidad por canal, respaldo, auditoría,
portal de borrado/exportación, métricas separadas de alertas oficiales.
```

**Regla de prioridad:** primero instrucción oficial verificada; nunca una alerta generada por redes sociales pasa a «oficial» por popularidad. El software jamás debe enviar alertas de evacuación propias no validadas por la autoridad.

## 3. Herencia conceptual de Simworld

Fuente inspeccionada: `ruminui/Exoinovaciones`, rama `simworld-reactivation-2026`, carpeta `SIMWORLD/`, archivos `README.md` y `PROJECT_STATUS.json` (2026-09-15), privado. Simworld contiene MapLibre, publicaciones de donaciones/servicios, interacciones geolocalizadas, moderación y SQLite WAL. Se aprovecha el patrón de «listado espacial + ciclo de publicación + contacto seguro», pero se crea **nueva implementación**: `ALERTA_SOLIDARIA_2026`, MIT. **No copiar** la base de datos, los tokens, reputaciones, código con dependencia de licencia no auditada ni identidad de Simworld; no hacer commits en su repo. La infraestructura de la red humanitaria debe operar por separado.

## 4. Esquema de interacción por zona

- Cada pedido tiene `kind`, `category`, `description`, `status` y coordenadas privadas.
- Marcadores públicos = redondeo 0,01 grados (~1,1 km en latitud) para mitigar exposición; el redondeo **no garantiza anonimato**.
- Las zonas de chat = redondeo a 0,1 grados (~11 km en latitud); son una aproximación simple de piloto, no hexágonos reales. Producción: H3/S2 + límites administrativos y GIS.
- WhatsApp: desde la app se abre `https://wa.me/?text=...` con enlace cartográfico y texto opt-in; elegir chat/grupo existente es decisión del usuario. Para grupos geográficos internos **el producto dispone de su propio chat**; se requieren antispam, moderadores y identidad verificada antes de distribuirlo.
- Google Maps: tiles/mapa interna con Maps JavaScript API, clave frontend restringida por HTTP referrer, Google Cloud y billing; sin clave, mapa OSM y deep-link a Google Maps; no infringir términos de proveedores.

## 5. Ejemplo API piloto

- `GET /api/health` — `ok`, modo de operación.
- `GET /api/config` — clave pública-restringida de Google Maps (no credencial de servidor), estado.
- `POST /api/auth/register`, `/api/auth/login` — contraseña >=10, sesión expira 7 días.
- `GET /api/posts`, `POST /api/posts` — búsqueda + publicación.
- `POST /api/posts/resolve`, `POST /api/reports` — cierre por dueño / reportes.
- `GET /api/chat?zone=8.9,-79.5`, `POST /api/chat` — sala comunitaria.
- `GET /api/earthquakes` — proxy cacheado a fuente USGS por 100 s, no EEW.

## 6. Resiliencia offline futura

Shell instalable offline ya implementado con Service Worker; los datos dinámicos no se cachean (para no mostrar «alerta vigente» desactualizada). Objetivo: fichas estáticas de preparación, mapas vectoriales descargados por zona bajo licencia válida, cola local **no entregada** con etiqueta inequívoca, P2P restringido Bluetooth/Wi-Fi solo con consentimiento, opciones SMS de respaldo autorizadas. **Nunca marcar un SOS como entregado sin confirmación del servidor/canal oficial**.
