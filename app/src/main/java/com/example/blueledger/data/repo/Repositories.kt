package com.example.blueledger.data.repo

import com.example.blueledger.data.local.DataStoreManager
import com.example.blueledger.data.model.UploadProject
import com.example.blueledger.data.model.User
import com.example.blueledger.data.model.WalletSummary
import com.example.blueledger.data.remote.ApiClientProvider
import com.example.blueledger.data.remote.LoginRequest
import com.example.blueledger.data.remote.ProjectRequest
import com.example.blueledger.data.remote.SignupRequest
import com.example.blueledger.data.remote.toUser
import com.google.gson.Gson
import kotlinx.coroutines.CoroutineDispatcher
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.withContext
import java.text.SimpleDateFormat
import java.util.Locale
import java.util.TimeZone

/**
 * AuthRepository talks to the BlueLedger demo backend (server/) for signup/login, and
 * caches the resulting User + lightweight preferences (remember-me, server URL) locally
 * via DataStore so the session survives app restarts.
 */
class AuthRepository(
    private val store: DataStoreManager,
    private val ioDispatcher: CoroutineDispatcher,
    private val gson: Gson,
    private val apiClientProvider: ApiClientProvider,
) {
    val rememberMe: Flow<Boolean> = store.rememberMeFlow()
    val currentUser: Flow<User?> = store.userJsonFlow().map { it?.let { json -> gson.fromJson(json, User::class.java) } }
    val language: Flow<String> = store.languageFlow()
    val serverBaseUrl: Flow<String> = store.serverBaseUrlFlow()

    suspend fun setRememberMe(enabled: Boolean) = store.setRememberMe(enabled)

    suspend fun setServerBaseUrl(url: String) = store.setServerBaseUrl(url)

    suspend fun login(email: String, password: String): User = withContext(ioDispatcher) {
        val dto = apiClientProvider.get().login(LoginRequest(email, password))
        val user = dto.toUser()
        store.setUserJson(gson.toJson(user))
        user
    }

    suspend fun signup(email: String, phone: String, password: String): User = withContext(ioDispatcher) {
        val username = email.substringBefore('@')
        val dto = apiClientProvider.get().signup(SignupRequest(email, phone, username, password))
        val user = dto.toUser()
        store.setUserJson(gson.toJson(user))
        user
    }

    suspend fun logout() = withContext(ioDispatcher) { store.setUserJson(null) }

    suspend fun setLanguage(lang: String) = store.setLanguage(lang)

    suspend fun updateUser(user: User) = store.setUserJson(gson.toJson(user))

    suspend fun fetchCommunityCount(): Int = withContext(ioDispatcher) {
        apiClientProvider.get().getCommunities().size
    }
}

private val serverTimestampFormat = SimpleDateFormat("yyyy-MM-dd HH:mm:ss", Locale.US).apply {
    timeZone = TimeZone.getTimeZone("UTC")
}

/**
 * ProjectsRepository reads/writes projects through the backend's REST API; the server is
 * the source of truth (and does the credit minting), so nothing is cached in DataStore here.
 */
class ProjectsRepository(
    private val ioDispatcher: CoroutineDispatcher,
    private val apiClientProvider: ApiClientProvider,
) {
    suspend fun fetchUploads(userId: Long): List<UploadProject> = withContext(ioDispatcher) {
        apiClientProvider.get().getProjects(userId).map { it.toUploadProject() }
    }

    suspend fun addUpload(
        userId: Long,
        plotId: String,
        species: String,
        hectares: Double,
        lat: Double,
        lng: Double,
        imageUri: String?,
    ): UploadProject = withContext(ioDispatcher) {
        val dto = apiClientProvider.get().addProject(
            ProjectRequest(
                userId = userId,
                plotId = plotId,
                species = species,
                hectares = hectares,
                gpsLat = lat,
                gpsLng = lng,
                imageUri = imageUri,
            )
        )
        dto.toUploadProject()
    }

    suspend fun fetchWallet(userId: Long): WalletSummary = withContext(ioDispatcher) {
        val dto = apiClientProvider.get().getWallet(userId)
        WalletSummary(totalCredits = dto.totalCredits, totalHectares = dto.totalHectares)
    }

    private fun com.example.blueledger.data.remote.ProjectDto.toUploadProject(): UploadProject = UploadProject(
        id = id.toString(),
        plotId = plotId,
        species = species,
        hectares = hectares,
        gpsLat = gpsLat,
        gpsLng = gpsLng,
        imageUri = imageUri,
        mintedCredits = mintedCredits,
        timestamp = runCatching { serverTimestampFormat.parse(createdAt)?.time }.getOrNull() ?: System.currentTimeMillis(),
    )
}
