package com.example.blueledger.data.remote

import com.example.blueledger.data.model.User
import com.google.gson.annotations.SerializedName

/**
 * Request/response DTOs for the BlueLedger demo backend (see server/main.py).
 * JSON uses snake_case to match the Python/Pydantic models.
 */
data class SignupRequest(
    val email: String,
    val phone: String,
    val username: String,
    val password: String,
)

data class LoginRequest(
    val email: String,
    val password: String,
)

data class UserDto(
    val id: Long,
    val email: String,
    val phone: String?,
    val username: String?,
)

fun UserDto.toUser(): User = User(id = id, email = email, phone = phone.orEmpty(), username = username.orEmpty())

data class SpeciesDto(
    val id: Long,
    val name: String,
    @SerializedName("credits_per_hectare") val creditsPerHectare: Double,
)

data class CommunityDto(
    val id: Long,
    val name: String,
)

data class ProjectRequest(
    @SerializedName("user_id") val userId: Long,
    @SerializedName("plot_id") val plotId: String,
    val species: String,
    val hectares: Double,
    @SerializedName("gps_lat") val gpsLat: Double,
    @SerializedName("gps_lng") val gpsLng: Double,
    @SerializedName("image_uri") val imageUri: String?,
)

data class ProjectDto(
    val id: Long,
    @SerializedName("plot_id") val plotId: String,
    val species: String,
    val hectares: Double,
    @SerializedName("gps_lat") val gpsLat: Double,
    @SerializedName("gps_lng") val gpsLng: Double,
    @SerializedName("image_uri") val imageUri: String?,
    @SerializedName("minted_credits") val mintedCredits: Int,
    val status: String,
    @SerializedName("created_at") val createdAt: String,
)

data class WalletDto(
    @SerializedName("total_credits") val totalCredits: Int,
    @SerializedName("total_hectares") val totalHectares: Double,
)
