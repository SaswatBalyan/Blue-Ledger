package com.example.blueledger.ui.screens.splash

import androidx.compose.animation.core.animateDpAsState
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.draw.scale
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalConfiguration
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.Font
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Devices
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.IntOffset
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.blueledger.R
import com.example.blueledger.ui.theme.BlueLedgerTheme
import kotlinx.coroutines.delay

@Composable
fun SplashScreen(onContinue: () -> Unit) {
    val koulenFontFamily = FontFamily(Font(R.font.koulenregular))
    val laBelleAuroreFontFamily = FontFamily(Font(R.font.labelleaurore))

    val context = LocalContext.current
    val density = LocalDensity.current
    val configuration = LocalConfiguration.current
    val screenHeightDp = configuration.screenHeightDp.dp

    var startExitAnimation by remember { mutableStateOf(false) }

    val initialDisplayTime = 1500L
    val animationDurationMillis = 1000

    LaunchedEffect(Unit) {
        delay(initialDisplayTime)
        startExitAnimation = true
        delay(animationDurationMillis.toLong())
        onContinue()
    }

    // Adjusted target Y for logo to align with OnboardingScreen's logo position
    val targetLogoYFromTop = 72.dp + 50.dp // 72dp spacer + 100dp/2 logo height on Onboarding
    val initialLogoYFromTop = screenHeightDp / 2
    val animatedLogoOffsetY: Dp by animateDpAsState(
        targetValue = if (startExitAnimation) targetLogoYFromTop - initialLogoYFromTop else 0.dp,
        animationSpec = tween(durationMillis = animationDurationMillis)
    )

    val animatedLogoScale: Float by animateFloatAsState(
        targetValue = if (startExitAnimation) 0.56f else 1f, // 112dp / 200dp
        animationSpec = tween(durationMillis = animationDurationMillis)
    )

    val animatedTextOffsetY: Dp by animateDpAsState(
        targetValue = if (startExitAnimation) (-130).dp else 0.dp, // Keeps text moving up
        animationSpec = tween(durationMillis = animationDurationMillis)
    )
    val animatedTextAlpha: Float by animateFloatAsState(
        targetValue = if (startExitAnimation) 0f else 1f,
        animationSpec = tween(durationMillis = animationDurationMillis / 2, delayMillis = animationDurationMillis / 4)
    )

    Box(
        modifier = Modifier
            .fillMaxSize()
            // Background color that is revealed when vector_3 would have moved (now static)
            // If vector_2 is meant to be seen, OnboardingScreen should handle its display.
            .background(Color(0xFFB5D8E7)) 
    ) {
        // Background pattern (vector_3) - Now static
        Image(
            painter = painterResource(id = R.drawable.vector_3),
            contentDescription = "Background Pattern",
            modifier = Modifier.fillMaxSize()
            // Removed offset animation for vector_3
        )

        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(24.dp),
            verticalArrangement = Arrangement.Center,
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            val logoResId = remember {
                context.resources.getIdentifier("blue_1", "drawable", context.packageName)
            }
            Image(
                painter = if (logoResId != 0) painterResource(id = logoResId) else painterResource(id = R.drawable.ic_logo),
                contentDescription = "Blue Ledger Logo",
                modifier = Modifier
                    .size(200.dp) // Initial size
                    .scale(animatedLogoScale)
                    .offset { IntOffset(0, with(density) { animatedLogoOffsetY.roundToPx() }) }
            )
            
            Spacer(modifier = Modifier.height(8.dp))
            
            Text(
                text = "BLUE LEDGER",
                fontFamily = koulenFontFamily,
                fontSize = 60.sp,
                color = Color(0xFF0B3042),
                textAlign = TextAlign.Center,
                modifier = Modifier
                    .alpha(animatedTextAlpha)
                    .offset { IntOffset(0, with(density) { animatedTextOffsetY.roundToPx() }) }
            )
            
           Spacer(modifier = Modifier.height(0.dp))
            
            Text(
                text = "minting a better future",
                fontFamily = laBelleAuroreFontFamily,
                fontSize = 28.sp,
                fontWeight = FontWeight.Normal,
                color = Color(0xFF2494C3),
                textAlign = TextAlign.Center,
                modifier = Modifier
                    .alpha(animatedTextAlpha)
                    .offset { IntOffset(0, with(density) { animatedTextOffsetY.roundToPx() }) }
            )
        }
    }
}

@Preview(showBackground = true, device = Devices.PIXEL_4, backgroundColor = 0xFFFFFFFF)
@Composable
fun SplashScreenPreview() {
    BlueLedgerTheme {
        SplashScreen(onContinue = {}) 
    }
}
