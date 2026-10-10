plugins { id("com.android.application"); id("org.jetbrains.kotlin.android") }
android {
    namespace = "org.alertasolidaria.mobile"
    compileSdk = 35
    defaultConfig {
        applicationId = "org.alertasolidaria.mobile"
        minSdk = 26
        targetSdk = 35
        versionCode = 1
        versionName = "0.2.0"
        // Set the actual HTTPS address before building for testers.
        buildConfigField("String", "SERVICE_URL", "\"https://change-me.invalid/\"")
    }
    buildFeatures { buildConfig = true }
    compileOptions { sourceCompatibility = JavaVersion.VERSION_17; targetCompatibility = JavaVersion.VERSION_17 }
    kotlinOptions { jvmTarget = "17" }
}
