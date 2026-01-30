package com.example.blueledger.di

import android.app.Application
import com.example.blueledger.data.local.DataStoreManager
import com.example.blueledger.data.repo.AuthRepository
import com.example.blueledger.data.repo.ProjectsRepository
import com.google.gson.Gson
import kotlinx.coroutines.Dispatchers

/**
 * Simple manual DI container for repositories and singletons.
 */
class AppContainer(application: Application) {
    private val gson = Gson()
    private val io = Dispatchers.IO
    private val store = DataStoreManager(application, io)

    val authRepository = AuthRepository(store, io, gson)
    val projectsRepository = ProjectsRepository(store, io, gson)
}


