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

    fun setRememberMe(enabled: Boolean) {
        viewModelScope.launch { repo.setRememberMe(enabled) }
    }

    fun login(email: String, password: String, onSuccess: () -> Unit) {
        viewModelScope.launch { repo.login(email, password); onSuccess() }
    }

    fun signup(email: String, phone: String, password: String, onSuccess: () -> Unit) {
        viewModelScope.launch { repo.signup(email, phone, password); onSuccess() }
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
 * ProjectsViewModel exposes uploads and totals, and allows adding mock uploads.
 */
class ProjectsViewModel(private val repo: ProjectsRepository) : ViewModel() {
    val uploads = repo.uploads.stateIn(viewModelScope, SharingStarted.Lazily, emptyList())
    val totals = repo.totals.stateIn(viewModelScope, SharingStarted.Lazily, 0.0 to 0)

    fun addUpload(
        plotId: String,
        species: String,
        hectares: Double,
        lat: Double,
        lng: Double,
        imageUri: String?,
        onDone: () -> Unit
    ) {
        viewModelScope.launch {
            repo.addUpload(plotId, species, hectares, lat, lng, imageUri)
            onDone()
        }
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


