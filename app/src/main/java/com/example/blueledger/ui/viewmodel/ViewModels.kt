package com.example.blueledger.ui.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import com.example.blueledger.data.repo.AuthRepository
import com.example.blueledger.data.repo.ProjectsRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.launch

/**
 * AuthViewModel exposes login/signup and remember-me state.
 */
class AuthViewModel(private val repo: AuthRepository) : ViewModel() {
    val rememberMe = repo.rememberMe.stateIn(viewModelScope, SharingStarted.Lazily, true)
    val currentUser = repo.currentUser.stateIn(viewModelScope, SharingStarted.Lazily, null)
    val language = repo.language.stateIn(viewModelScope, SharingStarted.Lazily, "English")
    val serverBaseUrl = repo.serverBaseUrl.stateIn(viewModelScope, SharingStarted.Lazily, "")

    private val _authError = MutableStateFlow<String?>(null)
    val authError: StateFlow<String?> = _authError.asStateFlow()

    private val _communityCount = MutableStateFlow(0)
    val communityCount: StateFlow<Int> = _communityCount.asStateFlow()

    fun setRememberMe(enabled: Boolean) {
        viewModelScope.launch { repo.setRememberMe(enabled) }
    }

    fun setServerBaseUrl(url: String) {
        viewModelScope.launch { repo.setServerBaseUrl(url) }
    }

    fun login(email: String, password: String, onSuccess: () -> Unit) {
        viewModelScope.launch {
            try {
                repo.login(email, password)
                _authError.value = null
                runCatching { _communityCount.value = repo.fetchCommunityCount() }
                onSuccess()
            } catch (e: Exception) {
                _authError.value = e.message ?: "Could not reach server. Check the Server IP and that it's running."
            }
        }
    }

    fun signup(email: String, phone: String, password: String, onSuccess: () -> Unit) {
        viewModelScope.launch {
            try {
                repo.signup(email, phone, password)
                _authError.value = null
                runCatching { _communityCount.value = repo.fetchCommunityCount() }
                onSuccess()
            } catch (e: Exception) {
                _authError.value = e.message ?: "Could not reach server. Check the Server IP and that it's running."
            }
        }
    }

    fun logout(onDone: () -> Unit) {
        viewModelScope.launch { repo.logout(); onDone() }
    }

    fun setLanguage(lang: String) {
        viewModelScope.launch { repo.setLanguage(lang) }
    }

    fun updateUser(email: String, phone: String, username: String) {
        val current = currentUser.value ?: return
        viewModelScope.launch { repo.updateUser(current.copy(email = email, phone = phone, username = username)) }
    }
}

/**
 * ProjectsViewModel exposes the signed-in user's uploads/totals, fetched from the backend,
 * and submits new uploads for it to mint credits for.
 */
class ProjectsViewModel(private val repo: ProjectsRepository) : ViewModel() {
    private val _uploads = MutableStateFlow<List<com.example.blueledger.data.model.UploadProject>>(emptyList())
    val uploads: StateFlow<List<com.example.blueledger.data.model.UploadProject>> = _uploads.asStateFlow()

    private val _totals = MutableStateFlow(0.0 to 0)
    val totals: StateFlow<Pair<Double, Int>> = _totals.asStateFlow()

    private val _message = MutableStateFlow<String?>(null)
    val message: StateFlow<String?> = _message.asStateFlow()

    fun refresh(userId: Long) {
        if (userId <= 0) return
        viewModelScope.launch {
            try {
                _uploads.value = repo.fetchUploads(userId)
                val wallet = repo.fetchWallet(userId)
                _totals.value = wallet.totalHectares to wallet.totalCredits
            } catch (e: Exception) {
                _message.value = "Could not load projects: ${e.message ?: "network error"}"
            }
        }
    }

    fun addUpload(
        userId: Long,
        plotId: String,
        species: String,
        hectares: Double,
        lat: Double,
        lng: Double,
        imageUri: String?,
        onDone: () -> Unit,
    ) {
        if (userId <= 0) {
            _message.value = "You're not logged in to the server yet."
            return
        }
        viewModelScope.launch {
            try {
                val created = repo.addUpload(userId, plotId, species, hectares, lat, lng, imageUri)
                refresh(userId)
                _message.value = "Project submitted — ${created.mintedCredits} credits minted"
                onDone()
            } catch (e: Exception) {
                _message.value = "Submit failed: ${e.message ?: "network error"}"
            }
        }
    }

    fun consumeMessage() {
        _message.value = null
    }
}

/**
 * Factory to construct ViewModels with repositories from our DI container.
 */
class AppViewModelFactory(
    private val authRepository: AuthRepository,
    private val projectsRepository: ProjectsRepository
) : ViewModelProvider.Factory {
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        @Suppress("UNCHECKED_CAST")
        return when {
            modelClass.isAssignableFrom(AuthViewModel::class.java) -> AuthViewModel(authRepository) as T
            modelClass.isAssignableFrom(ProjectsViewModel::class.java) -> ProjectsViewModel(projectsRepository) as T
            else -> throw IllegalArgumentException("Unknown ViewModel class: ${modelClass.name}")
        }
    }
}
