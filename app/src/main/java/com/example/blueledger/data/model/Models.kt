package com.example.blueledger.data.model

/**
 * Core data models used by the app.
 */
data class User(
    val email: String,
    val phone: String = "",
    val username: String = "",
)

data class UploadProject(
    val id: String,
    val plotId: String,
    val species: String,
    val hectares: Double,
    val gpsLat: Double,
    val gpsLng: Double,
    val imageUri: String? = null,
    val mintedCredits: Int = 0,
    val timestamp: Long = System.currentTimeMillis()
)

data class WalletSummary(
    val totalCredits: Int,
    val totalHectares: Double,
)


