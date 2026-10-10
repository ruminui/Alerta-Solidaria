import SwiftUI
import WebKit

/// Native iPhone integration shell. Critical Alerts permission NOT requested.
/// Does not provide background earthquake early warning or dispatch functionality.
struct CommunityWebView: UIViewRepresentable {
    // Replace only with a deployment owned and validated by the operator.
    static let serviceURL = "https://change-me.invalid/"

    func makeUIView(context: Context) -> WKWebView {
        let cfg = WKWebViewConfiguration()
        cfg.defaultWebpagePreferences.allowsContentJavaScript = true
        let view = WKWebView(frame: .zero, configuration: cfg)
        view.navigationDelegate = context.coordinator
        if let url = URL(string: Self.serviceURL), url.scheme == "https",
           url.host != "change-me.invalid" {
            view.load(URLRequest(url: url))
        } else {
            view.loadHTMLString("<html><meta name='viewport' content='width=device-width, initial-scale=1'><body style='font: 18px -apple-system; padding:24px'><h2>Alerta Solidaria</h2><p>Configuración HTTPS pendiente del operador.</p><p>Esta app no reemplaza emergencias oficiales.</p></body></html>", baseURL: nil)
        }
        return view
    }
    func updateUIView(_ uiView: WKWebView, context: Context) {}
    func makeCoordinator() -> Coordinator { Coordinator() }

    final class Coordinator: NSObject, WKNavigationDelegate {
        func webView(_ webView: WKWebView, decidePolicyFor action: WKNavigationAction,
                     decisionHandler: @escaping (WKNavigationActionPolicy) -> Void) {
            guard let destination = action.request.url else { decisionHandler(.cancel); return }
            if destination.host == URL(string: serviceURL)?.host && destination.scheme == "https" {
                decisionHandler(.allow)
            } else if ["https", "tel"].contains(destination.scheme ?? "") {
                UIApplication.shared.open(destination)
                decisionHandler(.cancel)
            } else {
                decisionHandler(.cancel)
            }
        }
    }
}
