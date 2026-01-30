package com.example.blueledger.util

import android.Manifest
import android.annotation.SuppressLint
import android.content.Context
import android.content.pm.PackageManager
import androidx.core.content.ContextCompat
import com.google.android.gms.location.FusedLocationProviderClient
import com.google.android.gms.location.LocationServices
import kotlinx.coroutines.suspendCancellableCoroutine
import kotlin.coroutines.resume

/**
 * Minimal helper to fetch last known location using FusedLocationProvider.
 * Falls back to (0.0, 0.0) when not available.
 */
class LocationHelper(context: Context) {
    private val fused: FusedLocationProviderClient = LocationServices.getFusedLocationProviderClient(context)

    fun hasLocationPermission(context: Context): Boolean {
        val fine = ContextCompat.checkSelfPermission(context, Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED
        val coarse = ContextCompat.checkSelfPermission(context, Manifest.permission.ACCESS_COARSE_LOCATION) == PackageManager.PERMISSION_GRANTED
        return fine || coarse
    }

    @SuppressLint("MissingPermission")
    suspend fun getLastLocationOrDefault(): Pair<Double, Double> = suspendCancellableCoroutine { cont ->
        fused.lastLocation.addOnSuccessListener { loc ->
            if (loc != null) cont.resume(loc.latitude to loc.longitude) else cont.resume(0.0 to 0.0)
        }.addOnFailureListener {
            cont.resume(0.0 to 0.0)
        }
    }
}


