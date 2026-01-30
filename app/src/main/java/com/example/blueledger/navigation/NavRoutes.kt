package com.example.blueledger.navigation

/**
 * Defines all navigation routes in the app.
 * Keep route names centralized to avoid typos across the app.
 */
sealed class NavRoute(val route: String) {
    data object Splash : NavRoute("splash")
    data object Onboarding : NavRoute("onboarding")
    data object Login : NavRoute("login")
    data object Signup : NavRoute("signup")
    data object Home : NavRoute("home")
}


