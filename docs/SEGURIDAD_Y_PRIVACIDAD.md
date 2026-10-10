# Riesgos y gates de seguridad — **NO GO PRODUCCIÓN**

## Riesgos críticos que bloquean despliegue público

- **SOS falso / suplantación / emboscadas:** alguien puede publicar un falso rescate, atraer personas, difundir rumores o coordinar estafas. Necesita verificación multifactor por organización, reputación gobernada, revisión profesional, antifraude, denuncia y revocación.
- **Exposición de víctimas:** la ubicación exacta en tiempo real de personas vulnerables no debe publicarse. Ahora el mapa expone redondeo ~1 km, pero puede reidentificar; debe incorporarse consentimiento graduado, borrado, retención limitada, cifrado por campo en reposo, protección de menores, roles de acceso y mensajería de contacto seguro.
- **Dinero y donaciones:** no solicitar transferencias o billeteras personales. Futura plataforma de donación con organizaciones verificadas, identidad institucional, auditoría de inventario y comprobantes, sin checkout propio en la fase inicial.
- **Alertas falsas:** nunca publicar boletines sísmicos propios como alertas institucionales, ni pronósticos de terremoto por IA.
- **Disponibilidad:** un servidor de prueba no soporta emergencia regional. Exigir multicentro, DDoS, pruebas de carga, copias cifradas, redundancia de DNS, colas durables, SLA y personal de guardia.
- **Incitación al pánico, difusión de datos médicos y direcciones personales:** moderación con humanos y avisos multilingües antes de publicación.
- **Integración WhatsApp:** apertura opt-in de enlaces, jamás extracción de contactos ni grupos sin consentimiento.
- **Reglas geográficas y legales:** ley de datos del país, protección de menores, contratación de voluntarios, relación con servicios de rescate, autorizaciones de servicios públicos.

## Implementado solo para laboratorio

- Contraseña derivada con `hashlib.scrypt` y salt aleatoria; token aleatorio almacenado como SHA-256; expiración en 7 días.
- Permisos de escritura requieren sesión, consultas públicas omiten IDs internos y coordenadas exactas.
- En frontend, entradas ciudadanas se presentan mediante `textContent`, evitando construir HTML de usuario.
- Rate limit en memoria por IP, por proceso, 20 escrituras/minuto; sólo suficiente para pruebas.
- Reporte de abuso se persiste; **ningún moderador recibe aviso actualmente**, los reportes requieren consulta y gestión futura.
- Se usa mismo origen; no se habilita CORS público.
- El servidor arranca por defecto en 127.0.0.1; no publicar accidentalmente.

## Gates antes de publicar

- [ ] Acuerdo institucional/documentación de «no reemplaza emergencias» aprobado por experto legal/seguridad.
- [ ] Permisos ubicación precisos por finalidad, minimización, borrado/exportación RGPD/local, tiempo de retención, cifrado.
- [ ] MFA para operadores y ONG; RLS/ACL roles; verificación institucional presencial cuando corresponda.
- [ ] Moderación humana continua, denuncia, bloqueo, abuso, herramientas de crisis.
- [ ] Auditoría externa OWASP MASVS/ASVS, pentest, SAST, DAST, supply chain, SBOM y firma.
- [ ] API detrás de WAF, HTTPS/HSTS, gateway, rate limits centralizados y auditorías inmutables.
- [ ] Pruebas offline/latencia/pérdida de energía/restarts/DDOS.
- [ ] Push y fuentes oficiales verificadas; protocolo de retiro de falsos positivos.
- [ ] Operaciones humanitarias aprobadas, red de voluntarios, seguros y políticas de seguridad personal.
- [ ] Servicios de donaciones verificables sin transferencias directas a personas no verificadas.
- [ ] Pruebas de usuario en Android/iPhone físicos, accesibilidad WCAG 2.2 AA.

**Riesgo residual** de un sistema de emergencias incluso después del lanzamiento: siempre habrá lugares sin señal, fallos de baterías, retrasos y falta de personal. El producto no puede prometer un aviso universal ni una respuesta garantizada.
