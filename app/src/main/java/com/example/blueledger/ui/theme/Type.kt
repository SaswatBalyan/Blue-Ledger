package com.example.blueledger.ui.theme

import androidx.compose.material3.Typography
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp
import androidx.compose.ui.text.googlefonts.Font
import androidx.compose.ui.text.googlefonts.GoogleFont

private val provider = GoogleFont.Provider(
    providerAuthority = "com.google.android.gms.fonts",
    providerPackage = "com.google.android.gms",
    certificates = com.example.blueledger.R.array.com_google_android_gms_fonts_certs
)

private val Koulen = FontFamily(
    Font(googleFont = GoogleFont("Koulen"), fontProvider = provider, weight = FontWeight.Normal)
)

private val LaBelleAurore = FontFamily(
    Font(googleFont = GoogleFont("La Belle Aurore"), fontProvider = provider, weight = FontWeight.Normal)
)

private val Rubik = FontFamily(
    Font(googleFont = GoogleFont("Rubik"), fontProvider = provider, weight = FontWeight.Medium)
)

val AppTypography = Typography(
    // Default body style as per instruction unless overridden
    bodyLarge = TextStyle(
        fontFamily = Rubik,
        fontWeight = FontWeight.Medium,
        fontSize = 16.sp,
        lineHeight = 22.sp,
        letterSpacing = 0.sp
    )
)

// Exposed custom roles for splash
val KoulenDisplay = TextStyle(
    fontFamily = Koulen,
    fontWeight = FontWeight.Normal,
    fontSize = 94.25.sp,
    lineHeight = 94.25.sp,
    letterSpacing = 0.sp
)

val TaglineScript = TextStyle(
    fontFamily = LaBelleAurore,
    fontWeight = FontWeight.Normal,
    fontSize = 45.07.sp,
    lineHeight = 45.07.sp,
    letterSpacing = 0.sp
)

val ContinueLabel = TextStyle(
    fontFamily = Rubik,
    fontWeight = FontWeight.Medium,
    fontSize = 27.01.sp,
    lineHeight = 37.8.sp,
    letterSpacing = 0.35.sp
)