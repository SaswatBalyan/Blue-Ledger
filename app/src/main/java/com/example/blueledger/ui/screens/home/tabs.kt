package com.example.blueledger.ui.screens.home

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import android.net.Uri
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.PickVisualMediaRequest
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Row
import androidx.compose.ui.platform.LocalUriHandler
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.ExposedDropdownMenuBox
import androidx.compose.material3.ExposedDropdownMenuDefaults
import android.Manifest
import androidx.activity.result.contract.ActivityResultContracts.RequestMultiplePermissions
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.SnackbarHost
import androidx.compose.material3.SnackbarHostState
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.setValue
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.ui.platform.LocalContext
import kotlinx.coroutines.launch

/**
 * Dashboard tab shows high-level metrics.
 * TODO: Bind to real data from repository.
 */
@Composable
fun DashboardTab(totalHectares: Double, totalCredits: Int, totalCommunities: Int, modifier: Modifier = Modifier) {
    Column(
        modifier = modifier.fillMaxSize().padding(16.dp),
        verticalArrangement = Arrangement.Top
    ) {
        Text("Dashboard", style = MaterialTheme.typography.headlineSmall)
        Spacer(Modifier.height(12.dp))
        Text("Total hectares uploaded: $totalHectares")
        Text("Total credits minted: $totalCredits")
        Text("Total communities enrolled: $totalCommunities")
    }
}

/**
 * Upload tab collects project data and mocks credit minting.
 * TODO: Add image picker and GPS.
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun UploadTab(onSubmitMock: () -> Unit = {}, onSubmit: (plotId: String, species: String, hectares: Double, lat: Double, lng: Double, imageUri: String?) -> Unit, modifier: Modifier = Modifier) {
    val (plotId, setPlotId) = remember { mutableStateOf("") }
    val speciesList = listOf("Rhizophora", "Avicennia", "Bruguiera")
    val (expanded, setExpanded) = remember { mutableStateOf(false) }
    val (species, setSpecies) = remember { mutableStateOf(speciesList.first()) }
    val (hectares, setHectares) = remember { mutableStateOf("") }
    val (imageUri, setImageUri) = remember { mutableStateOf<Uri?>(null) }

    val picker = rememberLauncherForActivityResult(ActivityResultContracts.PickVisualMedia()) { uri ->
        setImageUri(uri)
    }
    val snack = remember { SnackbarHostState() }
    val permissionLauncher = rememberLauncherForActivityResult(RequestMultiplePermissions()) { _ ->
        // After user responds, user can press Submit again.
    }
    var lat by remember { mutableStateOf(0.0) }
    var lng by remember { mutableStateOf(0.0) }
    val scope = rememberCoroutineScope()
    val ctx = LocalContext.current

    Column(
        modifier = modifier.fillMaxSize().padding(16.dp),
        verticalArrangement = Arrangement.Top
    ) {
        Text("Upload Project", style = MaterialTheme.typography.headlineSmall)
        Spacer(Modifier.height(12.dp))
        Row(verticalAlignment = Alignment.CenterVertically) {
            Text("Image: ")
            TextButton(onClick = {
                picker.launch(PickVisualMediaRequest(ActivityResultContracts.PickVisualMedia.ImageOnly))
            }) { Text(if (imageUri == null) "Pick Image" else "Change Image") }
        }
        OutlinedTextField(value = plotId, onValueChange = setPlotId, label = { Text("Plot ID") })
        Spacer(Modifier.height(8.dp))
        ExposedDropdownMenuBox(expanded = expanded, onExpandedChange = { setExpanded(!expanded) }) {
            OutlinedTextField(
                value = species,
                onValueChange = {},
                readOnly = true,
                label = { Text("Species of tree") },
                trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = expanded) },
                modifier = Modifier
            )
            ExposedDropdownMenu(expanded = expanded, onDismissRequest = { setExpanded(false) }) {
                speciesList.forEach { sp ->
                    DropdownMenuItem(text = { Text(sp) }, onClick = { setSpecies(sp); setExpanded(false) })
                }
            }
        }
        Spacer(Modifier.height(8.dp))
        OutlinedTextField(value = hectares, onValueChange = setHectares, label = { Text("Hectares of land") })
        Spacer(Modifier.height(8.dp))
        Text("GPS: auto-detected (mock)")
        Spacer(Modifier.height(16.dp))
        Button(onClick = {
            val h = hectares.toDoubleOrNull() ?: return@Button
            val helper = com.example.blueledger.util.LocationHelper(ctx)
            if (!helper.hasLocationPermission(ctx)) {
                permissionLauncher.launch(arrayOf(Manifest.permission.ACCESS_FINE_LOCATION, Manifest.permission.ACCESS_COARSE_LOCATION))
                // Proceed with default coords for demo
                onSubmit(plotId, species, h, lat, lng, imageUri?.toString())
                return@Button
            }
            scope.launch {
                val (la, ln) = helper.getLastLocationOrDefault()
                lat = la; lng = ln
                onSubmit(plotId, species, h, la, ln, imageUri?.toString())
            }
        }) { Text("Submit") }
        Spacer(Modifier.height(8.dp))
        Text("Current GPS: $lat, $lng")
    }
}

/**
 * Wallet tab shows totals and mock history.
 */
@Composable
fun WalletTab(totalCredits: Int, totalHectares: Double, items: List<com.example.blueledger.data.model.UploadProject>, modifier: Modifier = Modifier) {
    Column(
        modifier = modifier.fillMaxSize().padding(16.dp),
        verticalArrangement = Arrangement.Top
    ) {
        Text("Wallet", style = MaterialTheme.typography.headlineSmall)
        Spacer(Modifier.height(12.dp))
        Text("Total credits minted: $totalCredits")
        Text("Total hectares uploaded: $totalHectares")
        Spacer(Modifier.height(12.dp))
        Text("Previous uploads:")
        items.forEach { u ->
            Text("- ${u.plotId} • ${u.species} • ${u.hectares} ha • +${u.mintedCredits}")
        }
        Spacer(Modifier.height(16.dp))
        Button(onClick = { /* TODO: Implement sell credits */ }) { Text("Sell Credits") }
    }
}

/**
 * Profile tab shows editable user details and logout.
 */
@Composable
fun ProfileTab(
    initialEmail: String,
    initialPhone: String,
    initialUsername: String,
    onSave: (email: String, phone: String, username: String) -> Unit,
    onLogout: () -> Unit,
    modifier: Modifier = Modifier
) {
    val (username, setUsername) = remember { mutableStateOf(if (initialUsername.isBlank()) "User" else initialUsername) }
    val (email, setEmail) = remember { mutableStateOf(if (initialEmail.isBlank()) "user@example.com" else initialEmail) }
    val (phone, setPhone) = remember { mutableStateOf(if (initialPhone.isBlank()) "+" else initialPhone) }
    val uriHandler = LocalUriHandler.current

    Column(
        modifier = modifier.fillMaxSize().padding(16.dp),
        verticalArrangement = Arrangement.Top,
        horizontalAlignment = Alignment.Start
    ) {
        Text("Profile", style = MaterialTheme.typography.headlineSmall)
        Spacer(Modifier.height(12.dp))
        OutlinedTextField(value = username, onValueChange = setUsername, label = { Text("Username") })
        Spacer(Modifier.height(8.dp))
        OutlinedTextField(value = email, onValueChange = setEmail, label = { Text("Email") })
        Spacer(Modifier.height(8.dp))
        OutlinedTextField(value = phone, onValueChange = setPhone, label = { Text("Phone") })
        Spacer(Modifier.height(16.dp))
        Row {
            Button(onClick = { onSave(email, phone, username) }) { Text("Save") }
            Spacer(Modifier.height(0.dp))
            Button(onClick = onLogout, colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.error)) { Text("Logout") }
        }
        Spacer(Modifier.height(16.dp))
        Text(
            "Get to know us: https://example.org",
            color = MaterialTheme.colorScheme.primary,
            modifier = Modifier.clickable { uriHandler.openUri("https://example.org") }
        )
    }
}


