import SwiftUI

@main
struct AlertaSolidariaApp: App {
    var body: some Scene {
        WindowGroup { MainView() }
    }
}

struct MainView: View {
    var body: some View {
        NavigationStack {
            ZStack {
                Color(.systemGroupedBackground).ignoresSafeArea()
                CommunityWebView()
            }
            .navigationTitle("Alerta Solidaria")
            .navigationBarTitleDisplayMode(.inline)
        }
    }
}
