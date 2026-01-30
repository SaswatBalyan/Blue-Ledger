package com.example.blueledger

import android.app.Application
import com.example.blueledger.di.AppContainer

/**
 * Application class to host the DI container.
 */
class BlueLedgerApp : Application() {
    // Expose container for ViewModels/Activities to obtain repositories
    lateinit var container: AppContainer
        private set

    override fun onCreate() {
        super.onCreate()
        container = AppContainer(this)
    }
}


