package com.example.blueledger.data.remote

import com.example.blueledger.data.local.DataStoreManager
import com.google.gson.Gson
import kotlinx.coroutines.flow.first
import okhttp3.OkHttpClient
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

/**
 * The laptop's LAN IP is only known once the demo wifi is set up, so the base URL is
 * read fresh (from DataStore, user-editable at runtime) on every call rather than fixed
 * at build time. 10.0.2.2 is the Android emulator's alias for the host machine's localhost,
 * used as a fallback so the app still does something sensible before the user sets an IP.
 */
private const val DEFAULT_BASE_URL = "http://10.0.2.2:8000/"

internal fun normalizeBaseUrl(raw: String): String {
    var url = raw.trim()
    if (url.isEmpty()) return DEFAULT_BASE_URL
    if (!url.startsWith("http://") && !url.startsWith("https://")) url = "http://$url"
    if (!url.endsWith("/")) url = "$url/"
    return url
}

class ApiClientProvider(
    private val store: DataStoreManager,
    private val okHttpClient: OkHttpClient,
    private val gson: Gson,
) {
    suspend fun get(): ApiService {
        val baseUrl = normalizeBaseUrl(store.serverBaseUrlFlow().first())
        return Retrofit.Builder()
            .baseUrl(baseUrl)
            .client(okHttpClient)
            .addConverterFactory(GsonConverterFactory.create(gson))
            .build()
            .create(ApiService::class.java)
    }
}
