# iPhone/iOS: implementation and feature feedback playbook

Owner: authorized Apple engineering/product organization and official public-warning authorities. **This is a proposed integration, not a shipped iOS feature. No iPhone build or Critical Alerts authorization exists.**

## Starting source and procedure
- Review the MIT repository, safety notice, tests and separate OEM specification.
- On a Mac create a valid Xcode SwiftUI iOS project using native/ios/AlertaSolidaria/AlertaSolidariaApp.swift and CommunityWebView.swift as research starting points. Configure signing team, bundle identifier, HTTPS deployment and privacy disclosures. There is no ready-to-sign Xcode archive here.
- WKWebView requires app-site security audit, accessibility and restricted destinations. Reject arbitrary navigation and any non-HTTPS service endpoint.
- For optional normal mobile notifications, implement explicit permission, APNs token registration/rotation and authorized provider using TLS/HTTP2; specify short expiry, idempotency and revocation. APNs is best effort and may be delayed.
- Critical Alerts require Apple's special entitlement com.apple.developer.usernotifications.critical-alerts, requested and granted by Apple. The entitlement is NOT included or available by adding source code.
- Government emergency notifications, regional coverage and roaming belong to authorized Apple/operator/government paths, not this WebView. Do not represent post-event USGS data as early warning.
- Test on physical iPhone: real OS versions, screen locked/unlocked, Focus, quiet mode, no data, roaming, GPS denial, VoiceOver, Dynamic Type, delayed and stale notifications, duplicate events and official cancellations.
- App Store/TestFlight publishing of an independent app is distinct from inclusion in an iOS update. OS inclusion requires Apple authorization and independent implementation.

## One specific actionable iOS improvement to file
**Title:** Display real government-emergency-alert availability by country, carrier and roaming status in iPhone Settings.
**User problem:** travelers may not know whether earthquake/government warnings operate in a visited country.
**Expected:** accessible localized status supported/unsupported/unknown, clear limitations and a safe test where authorized.
**Submission:** https://developer.apple.com/feedback-assistant/ (iOS category, one issue per report) or https://www.apple.com/feedback/iphone/. Requires an account or manual web submission; retain a Feedback Assistant ID.
**Do NOT attach the full ZIP unsolicited:** https://www.apple.com/legal/intellectual-property/policies/ideas.html

Docs: https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.usernotifications.critical-alerts and https://developer.apple.com/documentation/usernotifications/sending-notification-requests-to-apns
