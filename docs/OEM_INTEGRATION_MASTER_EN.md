# Alerta Solidaria | OEM and Public Safety Integration Specification

Revision: 2026-10-10 · Open-source MIT · https://github.com/ruminui/Alerta-Solidaria

**Safety notice:** this is a LOCAL RESEARCH PILOT. It is NOT earthquake early warning, an emergency dispatch service, an Apple/Samsung system feature, or a government-authorized warning source. The USGS feed shows earthquakes AFTER they happen. User-generated posts must NEVER be promoted to official warnings.

## Executive request
Offer a no-cost, standards-oriented reference for product and public-safety teams to evaluate by explicit invitation. Independent, gated workstreams: (1) reveal emergency-alert availability and roaming limits in device Settings; (2) integrate authoritative alerts through government/OEM/operator channels; (3) optional privacy-preserving community map of needs, donations and offers. Do not send unsolicited archives to manufacturers.

## What is working in the repository
Python stdlib + SQLite API (users/posts/chat/reports); approximate-location map with Google Maps API optional and OSM fallback; geographically organized chat; opt-in WhatsApp sharing; post-event USGS feed; SwiftUI WebView and Android WebView starter sources. Pilot testing verifies software logic but is not device certification. Android APK, iOS IPA, critical alerts, Cell Broadcast access, emergency dispatch, WhatsApp group creation and money transfers are NOT included.

## Target reference architecture (FUTURE, NOT CODED)
Official authorized source -> verify digital signature, issuer identity, incident ID, timestamp and expiry -> enforce region polygon and severity -> independent human/automatic gates with fail-closed policy -> signed alert record with corrections/cancellations -> authorized Cell Broadcast by government/carrier/OEM AND supplementary APNs/FCM/SMS/voice, only where permitted -> telemetry of latency, receipt uncertainty and failures.
Separate trust boundary: unverified community needs -> user identity/abuse checks -> approximate map -> consent-based matching -> vetted NGO/operator approval -> audited supply delivery. No community SOS can trigger a privileged system alert.

## Cross-platform safety requirements
1. Official verified EEW/CAP data and regulator agreements; display unsupported/unknown where no coverage.
2. Duplicate/expired/untrusted CAP must NOT reach users as official alerts; validate time, polygons, authority, message type, language and cancellation.
3. Cell Broadcast is a privileged OEM/government/operator path, not a permission available to regular apps.
4. APNs/FCM are best effort, require connectivity and cannot guarantee seconds of anticipation.
5. Source separation (official, news, citizen reports), multilingual accessible wording and region-specific guidance.
6. Precise location opt-in only when necessary; public cells rounded; export/erase and expiring data including backups.
7. Prevention of scams/stalking and fake emergencies; volunteer verification, moderation 24/7, NGO accreditation and incident escalation.
8. Security review ASVS/MASVS, dependencies/SBOM, signed builds, penetration test, resilience and recovery drills.
9. Test locked devices, Focus/Doze, roaming, no signal, low battery, language, screen readers and end-to-end failover with actual agency supervisors.
10. Monitored, revocable phased rollout only after written approvals and independent validation.

## Reproduce local pilot
Python 3.11+ and Node 18+; run:
- python -m unittest discover -s tests -p test_*.py -v
- node --test tests/test_ui.cjs
- node --check app/app.js
- python backend/server.py
Browse http://127.0.0.1:8765 on the same computer. DO NOT expose this development server to the Internet. Map tiles require internet; Google Maps JavaScript API needs key/billing/restrictions.

## Approval gates
Local API/unit PASS does not imply mobile E2E PASS; mobile builds, official EEW, independent pentest, SRE, qualified moderators, government approval, privacy law, official distribution, emergency escalation and OEM acceptance remain BLOCKED. Release status: NO_GO.

## Manufacturer handoff
Apple: docs/APPLE_INTEGRATION_PLAYBOOK_EN.md
Samsung: docs/SAMSUNG_INTEGRATION_PLAYBOOK_EN.md
Operator manual: docs/MANUAL_TECNICO_DESPLIEGUE_Y_PRUEBAS_ES.md
Delivery process: docs/ENTREGA_INSTITUCIONAL_Y_CONTACTO_EN.md
Apple source policy: https://www.apple.com/legal/intellectual-property/policies/ideas.html
