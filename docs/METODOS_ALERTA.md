# Métodos de alerta: cuáles sirven y para qué

| Canal o tecnología | ¿Puede anticipar? | Principal límite | Requisito de implementación |
|---|---|---|---|
| **Cell Broadcast / WEA / CMAS / EU-Alert** | Sí, según organismo y tipo de amenaza; no depende de aplicación | Solo autoridad/operador y cobertura habilitada | Convenio con gobiernos, operadoras, normas y firmware; no disponible para apps comunes |
| **Red sísmica EEW profesional** (ShakeAlert, J-Alert, etc.) | En lugares cubiertos, segundos de anticipación pueden ser posibles | Cobertura geográfica, detección y distancia; cerca epicentro puede no haber aviso | Acuerdo de datos verificados, señales sismológicas en tiempo real y autoridades |
| **APNs + alerta crítica de Apple** | Solo con fuentes EEW válidas; puede alertar durante/tras evento | Entitlement especial, red, latencia y permiso; no Cell Broadcast | Solicitar permiso Apple, APNs, pruebas, validación geográfica |
| **FCM + notificaciones Android** | Igual: depende de detección EEW externa | Doze, permisos, conectividad, latencia variable | Google/Firebase, permisos, proceso de priorización y observabilidad |
| **Push web** (PWA) | No garantizado, especialmente iOS | Instalación, permisos y restricciones de background | Service worker push, VAPID, navegadores compatibles, backend de distribución |
| **SMS / RCS** | Difusión rápida en algunos escenarios | Congestión, latencia, coste, operador | Gateway contratado, consentimiento, geofencing y deduplicación |
| **Llamadas automatizadas / voz, TTS** | Puede avisar riesgo confirmado | Redes y filtros antispam | Infraestructura telefónica, autorizaciones, verificación |
| **Satélite / SOS satelital** | Rutas de emergencia cuando no hay red terrestre | Hardware, región, convenios del fabricante y operador | Integración OEM/gubernamental, no acceso irrestricto por terceros |
| **Bluetooth / Wi-Fi Direct / mesh** | Transmisión vecinal local (no EEW confiable) | Alcance, batería, abusos, interoperabilidad | Protocolo criptográfico, consentimiento, evaluación y pruebas reales |
| **Sirenes públicas / radio FM / NOAA Weather Radio donde exista** | Canal redundante para alertas oficiales | Infraestructura y cobertura | Protección Civil y emisoras |
| **Reloj inteligente / vibración accesible** | Según datos oficiales disponibles | Plataforma, permisos, accesibilidad | Complicaciones/haptics, pruebas con discapacidad auditiva/visual |
| **USGS GeoJSON feeds** | **NO**: registro posterior | Publicación tras sismo, no sirve para anticipación | Implementado en piloto sólo como consulta informativa |
| **Ciudadanos y acelerómetros** | Potencial en red masiva, pero alto riesgo de falsos positivos | Escala, falsos positivos, sesgos, ruido, latencia | Investigación formal y calibración; no enviar órdenes públicas sin verificación |
| **Predicción por IA** | **No hay predicción exacta y confiable** | Científicamente no permite saber lugar/hora del próximo sismo | Prohibir afirmaciones de predicción no validadas |

## Prioridades para alertas ultra eficaces

1. Integración institucional con datos CAP verificados, firma, vigencia y área del evento. Se rechazan boletines sin validez comprobable o que llegan fuera de tiempo.
2. Multi-telemetría sísmica profesional en regiones con sistemas de alerta temprana; mantener transparencia de la zona cubierta.
3. Múltiples rutas de entrega independientes: primero canal gubernamental Cell Broadcast, paralelo APNs/FCM de aplicaciones aprobadas, SMS/voz y sirenas públicas.
4. Geotargeting con polígonos reales; evitar alarmar países enteros sin necesidad.
5. Alertas accesibles: tono/vibración, texto legible en varios idiomas, instrucciones accionables, prioridad a personas con discapacidades, escala de fuente grande.
6. Monitorización extremo a extremo: tiempo de detección, decisión, inicio de entrega, recepción, tasa de fallos, coherencia horaria, simulacros y pruebas con operadoras.
7. Mensajes cortos, fuente/fecha/hora, tipo de amenaza, localización, acción concreta y enlace oficial. Distinción muy visible entre «simulacro», «informativo», «advertencia» y «evacuación».
8. Auto-fail-closed ante fuentes no verificadas; canales de degradación que nunca sugieran falsas garantías; evaluación independiente.

### Lógica ética obligatoria

Más notificaciones **no** significa mejor seguridad. Una falsa alerta puede ocasionar estampidas, sobrecarga de ambulancias y pérdida de confianza. Nunca suplantar el sistema nacional ni fabricar riesgo; la red comunitaria es complemento.
