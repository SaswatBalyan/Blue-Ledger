package com.example.blueledger.di

import android.app.Application
import com.example.blueledger.data.local.DataStoreManager
import com.example.blueledger.data.remote.ApiClientProvider
import com.example.blueledger.data.repo.AuthRepository
import com.example.blueledger.data.repo.ProjectsRepository
import com.google.gson.Gson
import kotlinx.coroutines.Dispatchers
import okhttp3.OkHttpClient
import java.util.concurrent.TimeUnit

/**
 * Simple manual DI container for repositories and singletons.
 */
class AppContainer(application: Application) {
    private val gson = Gson()
    private val io = Dispatchers.IO
    private val store = DataStoreManager(application, io)
    private val okHttpClient = OkHttpClient.Builder()
        .connectTimeout(10, TimeUnit.SECONDS)
        .readTimeout(10, TimeUnit.SECONDS)
        .build()
    private val apiClientProvider = ApiClientProvider(store, okHttpClient, gson)

    val authRepository = AuthRepository(store, io, gson, apiClientProvider)
    val projectsRepository = ProjectsRepository(io, apiClientProvider)
}
