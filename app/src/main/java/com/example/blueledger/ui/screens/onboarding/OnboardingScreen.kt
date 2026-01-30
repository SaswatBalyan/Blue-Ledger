package com.example.blueledger.ui.screens.onboarding

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.animateColorAsState // Corrected import
import androidx.compose.animation.core.animateDpAsState
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.tween
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.slideInVertically
import androidx.compose.animation.slideOutVertically
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
// import androidx.compose.foundation.layout.Arrangement // Unused import removed
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.scale
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalConfiguration
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.Font
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.IntOffset
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.blueledger.R // Make sure this import is correct for your project structure
import kotlinx.coroutines.delay

// Define Rubik Font Family - Ensure you have rubikmedium.ttf in res/font
val Rubik = FontFamily(
    Font(R.font.rubikmedium, FontWeight.Medium)
)

@Composable
fun OnboardingScreen(
    modifier: Modifier = Modifier, // Modifier is now the first optional parameter
    onLogin: () -> Unit,
    onSignup: () -> Unit,
    onLanguageChanged: (String) -> Unit = {}
) {
    val primaryTextColor = Color(0xFF0B3042)
    val buttonTextColor = Color(0xFFF8F8FF)
    val buttonBackgroundColor = Color(0xFF2C5262)
    val splashScreenBlue = Color(0xFFB5D8E7)
    val finalBackgroundColor = Color.White

    val currentConfiguration = LocalConfiguration.current
    val screenWidthDp = currentConfiguration.screenWidthDp.dp
    val screenHeightDp = currentConfiguration.screenHeightDp.dp
    val density = LocalDensity.current

    var contentVisible by remember { mutableStateOf(false) }

    val mainContentAnimationDuration = 600
    val logoSettleAnimationDuration = 500 // Slightly faster
    val initialDelayMillis = 100L // Short delay before starting animations

    LaunchedEffect(Unit) {
        delay(initialDelayMillis)
        contentVisible = true
    }

    val animatedBackgroundColor by animateColorAsState(
        targetValue = if (contentVisible) finalBackgroundColor else splashScreenBlue,
        animationSpec = tween(durationMillis = mainContentAnimationDuration),
        label = "BackgroundColorAnimation"
    )

    val logoAnimatedScale by animateFloatAsState(
        targetValue = if (contentVisible) 1.0f else 0.56f,
        animationSpec = tween(durationMillis = logoSettleAnimationDuration),
        label = "LogoScaleAnimation"
    )

    val logoAnimatedOffsetY: Dp by animateDpAsState(
        targetValue = if (contentVisible) 0.dp else (-20).dp, // Starts slightly up and settles
        animationSpec = tween(durationMillis = logoSettleAnimationDuration),
        label = "LogoOffsetYAnimation"
    )

    Box(
        modifier = modifier
            .fillMaxSize()
            .background(animatedBackgroundColor) // Animated background
    ) {
        // Top background vector image (vector3) - Static part of this screen's BG
        Image(
            painter = painterResource(id = R.drawable.vector3),
            contentDescription = null,
            modifier = Modifier
                .fillMaxWidth()
                .height(screenHeightDp * 0.15f)
                .align(Alignment.TopCenter),
            contentScale = ContentScale.FillWidth
        )

        val vector2Height = 1007.63.dp * (screenWidthDp / 720.dp)
        if (vector2Height < screenHeightDp * 0.6f) {
            Image(
                painter = painterResource(id = R.drawable.vector3),
                contentDescription = null,
                modifier = Modifier
                    .fillMaxWidth()
                    .height(screenHeightDp * 0.7f)
                    .align(Alignment.TopCenter),
                contentScale = ContentScale.FillWidth
            )
        }

        Image(
            painter = painterResource(id = R.drawable.vector2),
            contentDescription = null,
            modifier = Modifier
                .fillMaxWidth()
                .height(vector2Height)
                .align(Alignment.TopCenter)
                .offset(y = (50).dp * (screenWidthDp / 720.dp)),
            contentScale = ContentScale.FillWidth
        )

        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(horizontal = (80.dp * (screenWidthDp / 720.dp)))
        ) {
            Spacer(Modifier.height(72.dp))

            Image(
                painter = painterResource(id = R.drawable.blue_1),
                contentDescription = stringResource(R.string.logo_content_description),
                modifier = Modifier
                    .width(112.dp)
                    .height(100.dp)
                    .align(Alignment.CenterHorizontally)
                    .scale(logoAnimatedScale)
                    .offset { IntOffset(0, logoAnimatedOffsetY.roundToPx()) }
            )

            Spacer(Modifier.height(480.dp))

            AnimatedVisibility(
                visible = contentVisible,
                enter = slideInVertically(
                    initialOffsetY = { with(density) { 40.dp.roundToPx() } },
                    animationSpec = tween(durationMillis = mainContentAnimationDuration)
                ) + fadeIn(animationSpec = tween(durationMillis = mainContentAnimationDuration)),
                exit = slideOutVertically(animationSpec = tween(durationMillis = mainContentAnimationDuration))
                       + fadeOut(animationSpec = tween(durationMillis = mainContentAnimationDuration)),
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Text(
                        text = stringResource(id = R.string.welcome_),
                        fontFamily = Rubik,
                        fontWeight = FontWeight.Medium,
                        fontSize = 30.sp,
                        color = primaryTextColor,
                        textAlign = TextAlign.Start,
                        lineHeight = 36.sp,
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(bottom = 32.dp)
                    )

                    Button(
                        onClick = onSignup,
                        shape = RoundedCornerShape(19.59.dp),
                        colors = ButtonDefaults.buttonColors(
                            containerColor = buttonBackgroundColor,
                            contentColor = buttonTextColor
                        ),
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(80.18.dp)
                    ) {
                        Text(
                            text = stringResource(id = R.string.sign_up),
                            fontFamily = Rubik,
                            fontWeight = FontWeight.Medium,
                            fontSize = 29.39.sp,
                            letterSpacing = 0.01.sp
                        )
                    }

                    Spacer(Modifier.height(16.dp))

                    Button(
                        onClick = onLogin,
                        shape = RoundedCornerShape(19.59.dp),
                        colors = ButtonDefaults.buttonColors(
                            containerColor = buttonBackgroundColor,
                            contentColor = buttonTextColor
                        ),
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(80.18.dp)
                    ) {
                        Text(
                            text = stringResource(id = R.string.login),
                            fontFamily = Rubik,
                            fontWeight = FontWeight.Medium,
                            fontSize = 29.39.sp,
                            letterSpacing = 0.01.sp
                        )
                    }

                    Spacer(Modifier.height(24.dp))

                    TextButton(
                        onClick = { onLanguageChanged("next_language_code") }
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Icon(
                                painter = painterResource(id = R.drawable.globe),
                                contentDescription = stringResource(R.string.change_lang_icon_description),
                                tint = primaryTextColor,
                                modifier = Modifier.size(18.dp)
                            )
                            Spacer(Modifier.width(8.dp))
                            Text(
                                text = stringResource(id = R.string.change_lang),
                                fontFamily = Rubik,
                                fontWeight = FontWeight.Medium,
                                fontSize = 16.01.sp,
                                color = primaryTextColor,
                                letterSpacing = 0.01.sp,
                                lineHeight = 22.sp
                            )
                        }
                    }
                }
            }
            Spacer(Modifier.weight(1f))
        }
    }
}

@Preview(showBackground = true, widthDp = 360, heightDp = 720)
@Composable
fun OnboardingScreenPreviewLight() {
    OnboardingScreen(onLogin = {}, onSignup = {})
}

@Preview(showBackground = true, widthDp = 720, heightDp = 1080)
@Composable
fun OnboardingScreenPreviewLarge() {
    OnboardingScreen(onLogin = {}, onSignup = {})
}
