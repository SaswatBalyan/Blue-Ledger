package com.example.blueledger.data.remote

import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST
import retrofit2.http.Path
import retrofit2.http.Query

/**
 * REST contract for the BlueLedger demo backend running on the laptop (see server/main.py).
 */
interface ApiService {
    @POST("api/signup")
    suspend fun signup(@Body req: SignupRequest): UserDto

    @POST("api/login")
    suspend fun login(@Body req: LoginRequest): UserDto

    @GET("api/species")
    suspend fun getSpecies(): List<SpeciesDto>

    @GET("api/communities")
    suspend fun getCommunities(): List<CommunityDto>

    @POST("api/projects")
    suspend fun addProject(@Body req: ProjectRequest): ProjectDto

    @GET("api/projects")
    suspend fun getProjects(@Query("user_id") userId: Long): List<ProjectDto>

    @GET("api/wallet/{userId}")
    suspend fun getWallet(@Path("userId") userId: Long): WalletDto
}
