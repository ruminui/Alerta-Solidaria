# ALERTA SOLIDARIA · OPEN SOURCE

**Versión:** 0.2.1 (kit de publicación) · **Fecha:** 2026-10-10 · **Estado: PILOTO LOCAL VALIDABLE — NO APTO PARA EMERGENCIAS REALES**

Aplicación compartida con interfaz visual adaptada a iPhone y Samsung Galaxy. Mapa comunitario, solicitudes de ayuda y ofertas (donaciones e insumos), chat geográfico (mensajes visibles durante 24 h), plan offline de preparación, enlaces de WhatsApp y Google Maps, consulta del catálogo oficial de sismos de USGS. Independiente de Simworld: aprovecha sus patrones de mapa/social/tienda pero **no copia su repositorio, datos ni credenciales** y no modifica el proyecto original.

## Ejecutar en local (Python 3.11+)

```bash
python backend/server.py
# Abrir: http://127.0.0.1:8765
```

Para consultar el mapa de Google Maps desde la aplicación, configurar una clave válida, restringida al origen y con Maps JavaScript API habilitada; requiere proyecto Google Cloud y facturación:

```bash
export GOOGLE_MAPS_BROWSER_KEY='TU_CLAVE_RESTRINGIDA_A_DOMINIO' # Linux/macOS
python backend/server.py
```

En PowerShell: `$env:GOOGLE_MAPS_BROWSER_KEY='TU_CLAVE'; python backend/server.py`.
**Sin esa clave**, se dibuja un mapa interactivo OpenStreetMap/Leaflet y el botón **Abrir en Google Maps** funciona mediante enlace oficial. El proveedor se identifica siempre en la interfaz, y se mantiene el requisito de Google Maps para una instalación final.

### Tests automáticos sin acceso externo

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
node --test tests/test_ui.cjs
node --check app/app.js
```

Prueba visual opcional: `python tests/browser_smoke.py` (requiere Playwright, Chromium y acceso a localhost; en este entorno el navegador automatizado bloqueó 127.0.0.1 por política externa). No se declara aprobado el gate visual en dispositivo físico.

## Funciones implementadas y límites

| Función | Estado |
|--|--|
| Mapa interactivo, selección por toque, ubicación voluntaria | Implementada; requiere navegador que conceda permiso |
| Pedidos de ayuda / ofrecimientos / donaciones con marcadores | Implementada en servidor local y SQLite; se ocultan automáticamente tras 72 h |
| Regiones (aprox. 11 km), chat por zona y actualizaciones | Implementadas, **polling** de 2 min, no mensajería instantánea con WhatsApp |
| Compartir punto y descripción mediante enlace a WhatsApp | Implementado; el usuario elige destinatario / grupo existente |
| Google Maps (mapa interno) | Código implementado, bloqueado sin API key/facturación |
| OpenStreetMap de respaldo | Implementado, requiere Internet para tiles y librería |
| USGS terremotos de magnitud ≥4,5 en últimas 24 horas, zona <1500 km | Integrado como **registro posterior**, no alerta temprana |
| Dos estilos Galaxy/iPhone | Implementados en frontend compartido |
| Registro/login, scrypt, token sesiones, reporte abuso | Implementado para piloto; necesita auditoría para producción |
| Ubicación exacta oculta de vistas públicas | Implementado (redondeo ~1 km), almacenada en SQLite local (controlar acceso al servidor) |
| Push móvil, SMS / Cell Broadcast, sirena crítica, detección temprana | **NO implementado**. Requiere acuerdos/fuentes verificadas y capacidades del sistema |
| APK / IPA listos para tiendas | **NO**. Se incluyen guías / puentes nativos, requieren build, firma y pruebas |
| Grupo WhatsApp generado automáticamente | **NO**. Crear grupos arbitrarios no forma parte del enlace wa.me |
| Pagos / recaudación monetaria | **NO**; no pedir ni mover dinero por el piloto |
| Servicios reales de rescate / coordinación oficial | **NO**. Llamar al número oficial correspondiente |

## Seguridad y uso responsable

**Nunca desplegar públicamente tal cual.** El servidor rechaza por defecto enlazarse a una interfaz distinta de loopback; para pruebas exclusivamente en una red aislada exige `AS_REMOTE_PILOT_ACK=I_UNDERSTAND_NOT_FOR_EMERGENCIES`. Antes de un lanzamiento real: autenticación reforzada, antiabuso perimetral, moderación humana 24/7, verificación de voluntarios, RGPD/leyes locales, borrado/exportación de datos, fuentes oficiales y acuerdo con protección civil, HTTPS, respaldos, seguridad cloud, app store reviews, pruebas en redes lentas, push/APNs/FCM y auditoría accesibilidad. El registro de un pedido **no transmite un SOS al 911**. Jamás alertar que viene un sismo basándose en un registro USGS posterior.

Los mensajes y ubicaciones que aparecen en la app son creados por usuarios del servidor; **no están validados por rescatistas**. No ingresar teléfonos, domicilios privados, datos médicos o información financiera.

## Carpeta de documentos

- `docs/ARQUITECTURA.md`: solución de extremo a extremo, modos offline y canales de entrega.
- `docs/METODOS_ALERTA.md`: opciones técnicas, latencia, permisos y prioridades.
- `docs/SEGURIDAD_Y_PRIVACIDAD.md`: amenazas y gates de producción.
- `docs/CONTACTO_FABRICANTES.md`: canales oficiales, limitaciones legales y correos preparados.
- `docs/PITCH_APPLE_EN.md`, `docs/PITCH_SAMSUNG_EN.md`: propuestas concretas para integración nativa.
- `docs/HOJA_DE_RUTA.md`: ruta de producto, pruebas, plan de despliegue.
- `native/`: notas técnicas de plataformas para equipos internos.

**Licencia de esta implementación original:** MIT. Marcas Apple, Samsung, Google Maps y WhatsApp pertenecen a sus respectivos titulares. No afiliado ni aprobado por estas empresas. El código fuente de Simworld no se redistribuye en este paquete.

## Cambios 0.2.0 (2026-10-10)
- Mejor validación de coordenadas, incluidas entradas numéricas no finitas.
- Ocultación automática de pedidos con más de 72 horas y mensajes con más de 24 horas, para no presentar datos viejos como actuales. Esto es caducidad de VISIBILIDAD; los registros siguen guardados localmente para revisión, sujeto a futura política de retención.
- Guía de primeros pasos que se mantiene en caché después de la primera visita; no implica alertas ni datos sísmicos sin conexión.
- Cabeceras `X-Robots-Tag` y prevención de despliegue remoto accidental del servidor local.
- Suite de pruebas ampliada; componentes OEM y alertas previas siguen pendientes.

## Publicación independiente y feedback oficial

La preparación para publicar el código experimental y los enlaces oficiales de feedback están en [`docs/PUBLICAR_GITHUB_Y_CONTACTAR.md`](docs/PUBLICAR_GITHUB_Y_CONTACTAR.md). Este paquete no se ha enviado a Apple o Samsung, no tiene relación con ellos y no es apto para uso en emergencias reales. Consulte `SECURITY.md` antes de contribuir.
