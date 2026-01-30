package com.example.blueledger.data.repo

import com.example.blueledger.data.local.DataStoreManager
import com.example.blueledger.data.model.UploadProject
import com.example.blueledger.data.model.User
import com.google.gson.Gson
import com.google.gson.reflect.TypeToken
import kotlinx.coroutines.CoroutineDispatcher
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.withContext
import java.util.UUID
import kotlinx.coroutines.flow.first

/**
 * AuthRepository handles user login/signup locally using DataStore.
 * TODO: Replace with real backend API and token storage.
 */
class AuthRepository(
    private val store: DataStoreManager,
    private val ioDispatcher: CoroutineDispatcher,
    private val gson: Gson,
) {
    val rememberMe: Flow<Boolean> = store.rememberMeFlow()
    val currentUser: Flow<User?> = store.userJsonFlow().map { it?.let { json -> gson.fromJson(json, User::class.java) } }
    val language: Flow<String> = store.languageFlow()

    suspend fun setRememberMe(enabled: Boolean) = store.setRememberMe(enabled)

    suspend fun login(email: String, password: String): User = withContext(ioDispatcher) {
        // TODO: Replace with backend auth. This mock treats any non-empty credentials as valid.
        val user = User(email = email, username = email.substringBefore('@'))
        store.setUserJson(gson.toJson(user))
        user
    }

    suspend fun signup(email: String, phone: String, password: String): User = withContext(ioDispatcher) {
        // TODO: Replace with backend signup. This mock simply persists the user locally.
        val user = User(email = email, phone = phone, username = email.substringBefore('@'))
        store.setUserJson(gson.toJson(user))
        user
    }

    suspend fun logout() = withContext(ioDispatcher) { store.setUserJson(null) }

    suspend fun setLanguage(lang: String) = store.setLanguage(lang)
    
    suspend fun updateUser(user: User) = store.setUserJson(gson.toJson(user))
}

/**
 * ProjectsRepository persists uploads locally, and computes wallet summaries.
 * TODO: Replace with verification & minting logic once backend is ready.
 */
class ProjectsRepository(
    private val store: DataStoreManager,
    private val ioDispatcher: CoroutineDispatcher,
    private val gson: Gson,
) {
    private fun parseUploads(json: String?): List<UploadProject> {
        if (json.isNullOrEmpty()) return emptyList()
        val type = object : TypeToken<List<UploadProject>>() {}.type
        return gson.fromJson(json, type)
    }

    val uploads: Flow<List<UploadProject>> = store.uploadsJsonFlow().map { parseUploads(it) }

    val totals = uploads.map { list ->
        val hectares = list.sumOf { it.hectares }
        val credits = list.sumOf { it.mintedCredits }
        hectares to credits
    }

    suspend fun addUpload(
        plotId: String,
        species: String,
        hectares: Double,
        lat: Double,
        lng: Double,
        imageUri: String?
    ) = withContext(ioDispatcher) {
        val currentJson = store.uploadsJsonFlow().first()
        val current = parseUploads(currentJson)
        val minted = mockMintCreditsForSpecies(hectares, species)
        val newItem = UploadProject(
            id = UUID.randomUUID().toString(),
            plotId = plotId,
            species = species,
            hectares = hectares,
            gpsLat = lat,
            gpsLng = lng,
            imageUri = imageUri,
            mintedCredits = minted
        )
        val updated = current + newItem
        store.setUploadsJson(gson.toJson(updated))
    }

    fun mockMintCreditsForSpecies(hectares: Double, species: String): Int {
        // Simple species weighting for demo
        val basePerHectare = when (species.lowercase()) {
            "rhizophora" -> 14  // high carbon
            "avicennia" -> 12  // medium
            "bruguiera" -> 10  // baseline
            else -> 10
        }
        val bonus = if (hectares >= 10.0) 1.2 else if (hectares >= 5.0) 1.1 else 1.0
        val minted = (hectares * basePerHectare * bonus).toInt()
        return minted.coerceAtLeast(1)
    }
}


