package org.alertasolidaria.mobile

import android.Manifest
import android.app.Activity
import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Bundle
import android.webkit.GeolocationPermissions
import android.webkit.WebSettings
import android.webkit.WebChromeClient
import android.webkit.WebView
import android.webkit.WebViewClient
import android.webkit.WebResourceRequest
import android.widget.TextView

/** Native Galaxy integration shell. NOT an OEM Cell Broadcast client or EEW system. */
class MainActivity: Activity() {
    private var geolocationOrigin: String? = null
    private var geoCallback: GeolocationPermissions.Callback? = null
    private lateinit var web: WebView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val url = BuildConfig.SERVICE_URL
        if (!url.startsWith("https://") || url.contains("change-me.invalid")) {
            setContentView(TextView(this).apply {
                text = "Alerta Solidaria · configuración pendiente\n\n" +
                       "El equipo debe configurar la URL HTTPS verificada del servidor antes de usar la app. " +
                       "No reemplaza a los servicios de emergencia."
                textSize = 18f
                setPadding(32, 60, 32, 24)
            })
            return
        }
        web = WebView(this)
        setContentView(web)
        val approved = Uri.parse(url).host
        web.settings.allowFileAccess = false
        web.settings.allowContentAccess = false
        web.settings.mixedContentMode = WebSettings.MIXED_CONTENT_NEVER_ALLOW
        web.settings.javaScriptEnabled = true
        web.settings.domStorageEnabled = true
        web.settings.setGeolocationEnabled(true)
        web.webViewClient = object: WebViewClient() {
            override fun shouldOverrideUrlLoading(view: WebView?, request: WebResourceRequest): Boolean {
                val uri = request.url
                if (uri.scheme == "https" && uri.host == approved) return false
                if (uri.scheme !in listOf("https", "tel")) return true
                return try { startActivity(Intent(Intent.ACTION_VIEW, uri)); true }
                       catch (_: Exception) { true }
            }
        }
        web.webChromeClient = object: WebChromeClient() {
            override fun onGeolocationPermissionsShowPrompt(origin: String?, callback: GeolocationPermissions.Callback?) {
                if (origin == null || Uri.parse(origin).host != approved) {
                    callback?.invoke(origin, false, false); return
                }
                if (checkSelfPermission(Manifest.permission.ACCESS_COARSE_LOCATION) == PackageManager.PERMISSION_GRANTED) {
                    callback?.invoke(origin, true, false)
                } else {
                    geolocationOrigin = origin
                    geoCallback = callback
                    requestPermissions(arrayOf(Manifest.permission.ACCESS_COARSE_LOCATION), 17)
                }
            }
        }
        web.loadUrl(url)
    }

    override fun onRequestPermissionsResult(requestCode: Int, permissions: Array<out String>, grantResults: IntArray) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode == 17) {
            val granted = grantResults.firstOrNull() == PackageManager.PERMISSION_GRANTED
            geoCallback?.invoke(geolocationOrigin, granted, false)
            geoCallback = null; geolocationOrigin = null
        }
    }

    @Deprecated("Handled for compatibility with system back navigation")
    override fun onBackPressed() {
        if (::web.isInitialized && web.canGoBack()) web.goBack() else super.onBackPressed()
    }
}
