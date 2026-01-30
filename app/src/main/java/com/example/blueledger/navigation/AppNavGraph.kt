package com.example.blueledger.navigation

import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.compose.runtime.collectAsState
import androidx.compose.ui.platform.LocalContext
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.blueledger.BlueLedgerApp
import com.example.blueledger.ui.screens.auth.LoginScreen
import com.example.blueledger.ui.screens.auth.SignupScreen
import com.example.blueledger.ui.screens.home.HomeRoot
import com.example.blueledger.ui.screens.onboarding.OnboardingScreen
import com.example.blueledger.ui.screens.splash.SplashScreen
import com.example.blueledger.ui.viewmodel.AppViewModelFactory
import com.example.blueledger.ui.viewmodel.AuthViewModel
import com.example.blueledger.ui.viewmodel.ProjectsViewModel

/**
 * AppNavGraph wires all top-level destinations together using Navigation-Compose.
 * This separates navigation wiring from UI code for readability and testability.
 */
@Composable
fun AppNavGraph(
    navController: NavHostController,
    modifier: Modifier = Modifier,
) {
    NavHost(
        navController = navController,
        startDestination = NavRoute.Splash.route,
        modifier = modifier
    ) {
        composable(NavRoute.Splash.route) {
            SplashScreen(
                onContinue = { navController.navigate(NavRoute.Onboarding.route) { popUpTo(NavRoute.Splash.route) { inclusive = true } } }
            )
        }
        composable(NavRoute.Onboarding.route) {
            val app = (LocalContext.current.applicationContext as BlueLedgerApp)
            val factory = AppViewModelFactory(app.container.authRepository, app.container.projectsRepository)
            val authVm: AuthViewModel = viewModel(factory = factory)
            OnboardingScreen(
                onLogin = { navController.navigate(NavRoute.Login.route) },
                onSignup = { navController.navigate(NavRoute.Signup.route) },
                onLanguageChanged = { authVm.setLanguage(it) }
            )
        }
        composable(NavRoute.Login.route) {
            val app = (LocalContext.current.applicationContext as BlueLedgerApp)
            val factory = AppViewModelFactory(app.container.authRepository, app.container.projectsRepository)
            val authVm: AuthViewModel = viewModel(factory = factory)
            LoginScreen(
                onLogin = { email, password, remember ->
                    authVm.setRememberMe(remember)
                    authVm.login(email, password) {
                        navController.navigate(NavRoute.Home.route) { popUpTo(NavRoute.Onboarding.route) { inclusive = true } }
                    }
                },
                onNavigateToSignup = { navController.navigate(NavRoute.Signup.route) }
            )
        }
        composable(NavRoute.Signup.route) {
            val app = (LocalContext.current.applicationContext as BlueLedgerApp)
            val factory = AppViewModelFactory(app.container.authRepository, app.container.projectsRepository)
            val authVm: AuthViewModel = viewModel(factory = factory)
            SignupScreen(
                onSignup = { email, phone, password ->
                    authVm.signup(email, phone, password) {
                        navController.navigate(NavRoute.Home.route) { popUpTo(NavRoute.Onboarding.route) { inclusive = true } }
                    }
                },
                onNavigateToLogin = { navController.navigate(NavRoute.Login.route) }
            )
        }
        composable(NavRoute.Home.route) {
            val app = (LocalContext.current.applicationContext as BlueLedgerApp)
            val factory = AppViewModelFactory(app.container.authRepository, app.container.projectsRepository)
            val authVm: AuthViewModel = viewModel(factory = factory)
            val projectsVm: ProjectsViewModel = viewModel(factory = factory)
            val (hectares, credits) = projectsVm.totals.collectAsState().value
            val uploads = projectsVm.uploads.collectAsState().value
            val user = authVm.currentUser.collectAsState().value
            HomeRoot(
                hectaresTotal = hectares,
                creditsTotal = credits,
                uploads = uploads,
                onSubmitUpload = { plotId, species, hectaresValue, lat, lng, imageUri ->
                    projectsVm.addUpload(plotId, species, hectaresValue, lat = lat, lng = lng, imageUri = imageUri) {}
                },
                currentEmail = user?.email,
                currentPhone = user?.phone,
                currentUsername = user?.username,
                onSaveProfile = { email, phone, username -> authVm.updateUser(email, phone, username) },
                onLogout = { authVm.logout { navController.navigate(NavRoute.Onboarding.route) { popUpTo(0) } } }
            )
        }
    }
}


