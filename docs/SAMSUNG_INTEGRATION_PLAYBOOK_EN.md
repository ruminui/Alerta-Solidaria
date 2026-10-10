# Samsung Galaxy / One UI: integration and submission playbook

Owner: authorized Samsung One UI/Android systems engineers with national warning agencies/operators. **No Galaxy APK/AAB signed release, firmware integration, Cell Broadcast entitlement or certified early warning exists.**

## Engineering guide
1. Read source/QA/risk records. Android starter lives in native/android/ and contains a constrained WebView; it is not a privileged warning app.
2. Import with Android Studio, install supported JDK/SDK and Gradle, supply audited Gradle wrapper and app identity, replace placeholder SERVICE_URL with verified HTTPS pilot host only, configure privacy docs, target SDK and dependencies, sign test builds. A reproducible APK has NOT been built.
3. Restrict WebView local file/content access, mixed content and outbound URL schemes; request coarse location only after opt-in; default manual map mode without GPS.
4. Optional community notifications can use FCM with runtime permission and honest best-effort latency. Distinguish from government warnings. Doze, roaming, connectivity and power modes require physical tests.
5. Cell Broadcast/WEA-style emergency warnings require approved modem/framework/carrier/national-authority integration. No normal Google Play app can impersonate this by declaring an Android permission.
6. Official EEW requires verified region-specific low-latency source, authoritative policy and pre-broadcast fail-closed gate; the current USGS feed is post-event only.
7. Galaxy-specific QA: phones, OS releases, SIMs, roaming, network loss, accessibility TalkBack/large text, vibration/visual alternatives, data saver, throttling, false-alert prevention and factory rollback.
8. Phone app distribution requires Play Store review or controlled testing; inclusion in One UI firmware is an entirely separate, Samsung-authorized update process.

## Targeted product feedback (NOT code submission)
Title: Show government-emergency-alert service availability in Galaxy Settings by country, carrier and roaming.
Reason: travelers cannot easily know if emergency broadcasts/earthquake alerts are available.
Proposed UX: status supported/unsupported/unknown, regional limitations and verified local agencies, clear audible/accessibility options and permitted user test.
Submit from Samsung Members in the region with a signed-in Samsung account: https://www.samsung.com/ar/apps/samsung-members/ . Save receipt/post ID. Do not email an unsolicited ZIP to generic support.
