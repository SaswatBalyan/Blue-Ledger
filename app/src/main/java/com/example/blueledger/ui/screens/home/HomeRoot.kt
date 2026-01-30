package com.example.blueledger.ui.screens.home

import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.AccountCircle
import androidx.compose.material.icons.filled.AddCircle
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.Wallet
import androidx.compose.material3.Icon
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier

/**
 * HomeRoot hosts the bottom tab navigation and shows the selected tab content.
 */
@Composable
fun HomeRoot(
    hectaresTotal: Double,
    creditsTotal: Int,
    uploads: List<com.example.blueledger.data.model.UploadProject>,
    onSubmitUpload: (plotId: String, species: String, hectares: Double, lat: Double, lng: Double, imageUri: String?) -> Unit,
    currentEmail: String?,
    currentPhone: String?,
    currentUsername: String?,
    onSaveProfile: (email: String, phone: String, username: String) -> Unit,
    onLogout: () -> Unit,
    modifier: Modifier = Modifier
) {
    val tabs = listOf(HomeTab.Dashboard, HomeTab.Upload, HomeTab.Wallet, HomeTab.Profile)
    val (selected, setSelected) = remember { mutableStateOf(HomeTab.Dashboard) }

    Scaffold(
        modifier = modifier,
        bottomBar = {
            NavigationBar {
                tabs.forEach { tab ->
                    NavigationBarItem(
                        selected = tab == selected,
                        onClick = { setSelected(tab) },
                        icon = { Icon(imageVector = tab.icon, contentDescription = tab.label) },
                        label = { Text(tab.label) }
                    )
                }
            }
        }
    ) { padding ->
        when (selected) {
            HomeTab.Dashboard -> DashboardTab(hectaresTotal, creditsTotal, uploads.size, modifier = Modifier)
            HomeTab.Upload -> UploadTab(onSubmitMock = { /* deprecated */ }, onSubmit = onSubmitUpload, modifier = Modifier)
            HomeTab.Wallet -> WalletTab(creditsTotal, hectaresTotal, uploads, modifier = Modifier)
            HomeTab.Profile -> ProfileTab(
                initialEmail = currentEmail.orEmpty(),
                initialPhone = currentPhone.orEmpty(),
                initialUsername = currentUsername.orEmpty(),
                onSave = onSaveProfile,
                onLogout = onLogout,
                modifier = Modifier
            )
        }
    }
}

enum class HomeTab(val label: String, val icon: androidx.compose.ui.graphics.vector.ImageVector) {
    Dashboard("Home", Icons.Filled.Home),
    Upload("Upload", Icons.Filled.AddCircle),
    Wallet("Wallet", Icons.Filled.Wallet),
    Profile("Profile", Icons.Filled.AccountCircle)
}


