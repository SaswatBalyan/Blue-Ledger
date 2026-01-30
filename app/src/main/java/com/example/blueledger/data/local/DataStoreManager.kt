package com.example.blueledger.data.local

import android.content.Context
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.emptyPreferences
import androidx.datastore.preferences.core.booleanPreferencesKey
import androidx.datastore.preferences.core.stringPreferencesKey
import androidx.datastore.preferences.preferencesDataStore
import kotlinx.coroutines.CoroutineDispatcher
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.catch
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.withContext
import java.io.IOException

private const val PREFS_NAME = "blueledger_prefs"

private val Context.dataStore by preferencesDataStore(name = PREFS_NAME)

/**
 * DataStoreManager provides typed access to app preferences and simple persistence
 * for mock backend-less operation (e.g., remember me, user JSON, uploads JSON).
 */
class DataStoreManager(
    private val context: Context,
    private val ioDispatcher: CoroutineDispatcher,
) {
    private object Keys {
        val rememberMe: Preferences.Key<Boolean> = booleanPreferencesKey("remember_me")
        val userJson: Preferences.Key<String> = stringPreferencesKey("user_json")
        val uploadsJson: Preferences.Key<String> = stringPreferencesKey("uploads_json")
        val language: Preferences.Key<String> = stringPreferencesKey("language")
    }

    fun rememberMeFlow(): Flow<Boolean> = context.dataStore.data
        .catch { e -> if (e is IOException) emit(emptyPreferences()) else throw e }
        .map { it[Keys.rememberMe] ?: true }

    suspend fun setRememberMe(enabled: Boolean) = withContext(ioDispatcher) {
        context.dataStore.edit { it[Keys.rememberMe] = enabled }
    }

    fun userJsonFlow(): Flow<String?> = context.dataStore.data
        .catch { e -> if (e is IOException) emit(emptyPreferences()) else throw e }
        .map { it[Keys.userJson] }

    suspend fun setUserJson(json: String?) = withContext(ioDispatcher) {
        context.dataStore.edit { prefs ->
            if (json == null) prefs.remove(Keys.userJson) else prefs[Keys.userJson] = json
        }
    }

    fun uploadsJsonFlow(): Flow<String?> = context.dataStore.data
        .catch { e -> if (e is IOException) emit(emptyPreferences()) else throw e }
        .map { it[Keys.uploadsJson] }

    suspend fun setUploadsJson(json: String) = withContext(ioDispatcher) {
        context.dataStore.edit { it[Keys.uploadsJson] = json }
    }

    fun languageFlow(): Flow<String> = context.dataStore.data
        .catch { e -> if (e is IOException) emit(emptyPreferences()) else throw e }
        .map { it[Keys.language] ?: "English" }

    suspend fun setLanguage(lang: String) = withContext(ioDispatcher) {
        context.dataStore.edit { it[Keys.language] = lang }
    }
}


