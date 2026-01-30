package com.example.blueledger.ui.screens.auth

import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.size // Added import
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Icon // Added import
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalConfiguration
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.Font
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.em
import androidx.compose.ui.unit.sp
import com.example.blueledger.R // Make sure this import is correct for your R class

// TODO: Ensure you have rubikmedium.ttf in res/font folder
val rubikFontFamily = FontFamily(Font(R.font.rubikmedium))

val textPrimaryColor = Color(0xFF0B3042)
val textHintColor = Color(0xFF9E9E9E)
val accentColor = Color(0xFF2C5262)
val buttonTextColor = Color(0xFFF8F8FF)
val screenBackgroundColor = Color.White

@Composable
fun CustomStyledTextField(
    value: String,
    onValueChange: (String) -> Unit,
    label: String,
    modifier: Modifier = Modifier,
    lineDrawableRes: Int,
    scaleFactor: Float,
    leadingIconRes: Int? = null,
    leadingIconContentDescription: String? = null,
    visualTransformation: VisualTransformation = VisualTransformation.None,
    keyboardType: KeyboardType = KeyboardType.Text,
    keyboardActions: KeyboardActions = KeyboardActions.Default
) {
    Column(modifier = modifier) {
        Text(
            text = label,
            style = TextStyle(
                fontSize = (27.44f * scaleFactor).sp,
                fontFamily = rubikFontFamily,
                color = textPrimaryColor,
                letterSpacing = 0.01.em
            ),
            modifier = Modifier.offset(y = ((-2.95f) * scaleFactor).dp)
        )
        Row(
            verticalAlignment = Alignment.CenterVertically,
            modifier = Modifier.padding(top = (4f * scaleFactor).dp) // Adjust spacing between label and input area
        ) {
            if (leadingIconRes != null) {
                Icon(
                    painter = painterResource(id = leadingIconRes),
                    contentDescription = leadingIconContentDescription,
                    modifier = Modifier.size((24f * scaleFactor).dp), // Scaled icon size
                    tint = textHintColor // Optional: Apply a tint to the icon
                )
                Spacer(Modifier.width((8f * scaleFactor).dp))
            }
            Column(modifier = Modifier.weight(1f)) {
                BasicTextField(
                    value = value,
                    onValueChange = onValueChange,
                    textStyle = TextStyle(
                        fontSize = (27.44f * scaleFactor).sp,
                        fontFamily = rubikFontFamily,
                        color = textPrimaryColor
                    ),
                    visualTransformation = visualTransformation,
                    keyboardOptions = KeyboardOptions(keyboardType = keyboardType),
                    keyboardActions = keyboardActions,
                    singleLine = true,
                    decorationBox = { innerTextField ->
                        Column {
                            innerTextField() // The actual text input area
                            Spacer(Modifier.height((10f * scaleFactor).dp)) // Space between text and line
                            Image(
                                painter = painterResource(id = lineDrawableRes),
                                contentDescription = "Text field underline",
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .height((2.72f * scaleFactor).dp),
                                contentScale = ContentScale.FillBounds
                            )
                        }
                    }
                )
            }
        }
    }
}


/**
 * SignupScreen captures new user information and navigates to Home on success.
 * TODO: Replace with real signup API + validation.
 */
@Composable
fun SignupScreen(
    onSignup: (email: String, phone: String, password: String) -> Unit,
    onNavigateToLogin: () -> Unit,
    modifier: Modifier = Modifier
) {
    val (email, setEmail) = remember { mutableStateOf("") }
    val (phone, setPhone) = remember { mutableStateOf("") }
    val (password, setPassword) = remember { mutableStateOf("") }
    val (confirm, setConfirm) = remember { mutableStateOf("") }

    val scaleFactor = 0.6f // Applied scale factor from previous step, ensure this is desired

    val figmaContentWidthDp = 588.dp * scaleFactor

    val configuration = LocalConfiguration.current
    val screenWidthDp = configuration.screenWidthDp.dp
    val horizontalPadding = ((screenWidthDp - figmaContentWidthDp) / 2).coerceAtLeast(0.dp)

    Box(
        modifier = modifier
            .fillMaxSize()
            .background(screenBackgroundColor)
    ) {
        Image(
            painter = painterResource(id = R.drawable.vector_3),
            contentDescription = null, // Decorative
            modifier = Modifier
                .fillMaxWidth()
                .height((1007.63f * scaleFactor).dp)
                .offset(y = ((-527f) * scaleFactor).dp),
            contentScale = ContentScale.FillWidth
        )

        Column(
            modifier = Modifier
                .fillMaxSize()
                .verticalScroll(rememberScrollState())
                .padding(horizontal = horizontalPadding)
                .padding(top = (350.dp - (70f * scaleFactor).dp)),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text(
                text = "Sign up",
                style = TextStyle(
                    fontSize = (65.17f * scaleFactor).sp,
                    color = textPrimaryColor,
                    fontFamily = rubikFontFamily,
                    lineHeight = (72f * scaleFactor).sp
                ),
                modifier = Modifier.align(Alignment.Start)
            )

            Spacer(Modifier.height((16f * scaleFactor).dp))

            Image(
                painter = painterResource(id = R.drawable.line_8),
                contentDescription = null,
                modifier = Modifier
                    .width((126.92f * scaleFactor).dp)
                    .height((5.43f * scaleFactor).dp)
                    .align(Alignment.Start)
            )

            Spacer(Modifier.height((60f * scaleFactor).dp))

            CustomStyledTextField(
                value = email,
                onValueChange = setEmail,
                label = "Email",
                lineDrawableRes = R.drawable.line_2,
                scaleFactor = scaleFactor,
                leadingIconRes = R.drawable.ic_email_custom,
                leadingIconContentDescription = "Email Icon",
                modifier = Modifier.fillMaxWidth()
            )
            Spacer(Modifier.height((35f * scaleFactor).dp))

            CustomStyledTextField(
                value = phone,
                onValueChange = setPhone,
                label = "Phone no",
                lineDrawableRes = R.drawable.line_2,
                scaleFactor = scaleFactor,
                leadingIconRes = R.drawable.ic_mobile_custom,
                leadingIconContentDescription = "Mobile Icon",
                keyboardType = KeyboardType.Phone,
                modifier = Modifier.fillMaxWidth()
            )
            Spacer(Modifier.height((35f * scaleFactor).dp))

            CustomStyledTextField(
                value = password,
                onValueChange = setPassword,
                label = "Password",
                lineDrawableRes = R.drawable.line_password_inactive,
                scaleFactor = scaleFactor,
                leadingIconRes = R.drawable.ic_lock_custom,
                leadingIconContentDescription = "Lock Icon",
                visualTransformation = PasswordVisualTransformation(),
                keyboardType = KeyboardType.Password,
                modifier = Modifier.fillMaxWidth()
            )
            Spacer(Modifier.height((35f * scaleFactor).dp))

            CustomStyledTextField(
                value = confirm,
                onValueChange = setConfirm,
                label = "Confirm Password",
                lineDrawableRes = R.drawable.line_password_inactive,
                scaleFactor = scaleFactor,
                leadingIconRes = R.drawable.ic_lock_custom,
                leadingIconContentDescription = "Lock Icon",
                visualTransformation = PasswordVisualTransformation(),
                keyboardType = KeyboardType.Password,
                modifier = Modifier.fillMaxWidth()
            )

            Spacer(Modifier.height((70f * scaleFactor).dp))

            Button(
                onClick = { onSignup(email, phone, password) },
                modifier = Modifier
                    .fillMaxWidth()
                    .height((84.16f * scaleFactor).dp),
                shape = RoundedCornerShape((21.72f * scaleFactor).dp),
                colors = ButtonDefaults.buttonColors(containerColor = accentColor)
            ) {
                Text(
                    text = "Create Account",
                    style = TextStyle(
                        fontSize = (32.59f * scaleFactor).sp,
                        color = buttonTextColor,
                        fontFamily = rubikFontFamily,
                        letterSpacing = 0.01.em
                    )
                )
            }

            Spacer(Modifier.height((35f * scaleFactor).dp))

            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.Center
            ) {
                Text(
                    text = "Already have an Account!",
                    style = TextStyle(
                        fontSize = (25.35f * scaleFactor).sp,
                        color = textHintColor,
                        fontFamily = rubikFontFamily,
                        letterSpacing = 0.01.em
                    )
                )
                Spacer(Modifier.width((8f * scaleFactor).dp))
                Text(
                    text = "Login",
                    style = TextStyle(
                        fontSize = (25.35f * scaleFactor).sp,
                        color = accentColor,
                        fontFamily = rubikFontFamily,
                        letterSpacing = 0.01.em
                    ),
                    modifier = Modifier.clickable { onNavigateToLogin() }
                )
            }
            Spacer(Modifier.height((50f * scaleFactor).dp))
        }
    }
}
