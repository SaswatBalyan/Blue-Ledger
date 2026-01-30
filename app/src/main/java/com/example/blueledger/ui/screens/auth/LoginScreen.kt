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
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Lock
import androidx.compose.material.icons.filled.MailOutline
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Checkbox
import androidx.compose.material3.CheckboxDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.material3.TextField
import androidx.compose.material3.TextFieldDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clipToBounds
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.Font
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.blueledger.R

// Define Rubik font family
val Rubik = FontFamily(
    Font(R.font.rubikmedium)
)

@Composable
fun LoginScreen(
    onLogin: (email: String, password: String, rememberMe: Boolean) -> Unit,
    onNavigateToSignup: () -> Unit,
    modifier: Modifier = Modifier
) {
    val (email, setEmail) = remember { mutableStateOf("") }
    val (password, setPassword) = remember { mutableStateOf("") }
    val (rememberMe, setRememberMe) = remember { mutableStateOf(false) }

    Box(
        modifier = modifier
            .fillMaxSize()
            .background(Color.White)
            .clipToBounds()
    ) {
        Image(
            painter = painterResource(id = R.drawable.vector2),
            contentDescription = null, // Decorative
            modifier = Modifier
                .fillMaxWidth()
                .height(630.dp) 
                .offset(y = (-265).dp) 
            ,
            contentScale = ContentScale.FillWidth
        )

        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(horizontal = 30.dp) 
        ) {
            Spacer(modifier = Modifier.height(350.dp))

            Text(
                text = "Log in",
                style = TextStyle(
                    fontSize = 40.sp, 
                    fontFamily = Rubik, 
                    // fontWeight = FontWeight.Medium, // Removed, Rubik is rubikmedium
                    color = Color(0xFF0B3042)
                )
            )
            Image(
                painter = painterResource(id = R.drawable.line_9),
                contentDescription = null, // Decorative
                modifier = Modifier
                    .width(100.dp) 
                    .offset(x = (-3).dp) // Adjust this value to position the line
                    .height(3.dp)
            )

            Spacer(modifier = Modifier.height(60.dp))

            Text(
                text = "Email",
                style = TextStyle(
                    fontSize = 17.sp, 
                    fontFamily = Rubik,
                    color = Color(0xFF0B3042),
                    letterSpacing = 0.01.sp
                ),
                modifier = Modifier.padding(bottom = 8.dp)
            )
            TextField(
                value = email,
                onValueChange = setEmail,
                placeholder = { Text("Enter your email", style = TextStyle(fontFamily = Rubik, fontSize = 16.sp)) },
                leadingIcon = {
                    Icon(
                        imageVector = Icons.Filled.MailOutline,
                        contentDescription = "Email Icon",
                        tint = Color(0xFF0B3042) 
                    )
                },
                colors = TextFieldDefaults.colors(
                    focusedContainerColor = Color.Transparent,
                    unfocusedContainerColor = Color.Transparent,
                    disabledContainerColor = Color.Transparent,
                    cursorColor = Color(0xFF0B3042),
                    focusedIndicatorColor = Color.Transparent, 
                    unfocusedIndicatorColor = Color.Transparent, 
                ),
                textStyle = TextStyle(fontSize = 16.sp, color = Color.Black, fontFamily = Rubik),
                singleLine = true,
                modifier = Modifier.fillMaxWidth()
            )
            Image(
                painter = painterResource(id = R.drawable.line_2),
                contentDescription = "Email underline",
                modifier = Modifier
                    .fillMaxWidth()
                    .offset(x = 0.dp) // Adjust this value to align with "E"
                    .height(1.dp)
            )

            Spacer(modifier = Modifier.height(25.dp))

            Text(
                text = "Password",
                style = TextStyle(
                    fontSize = 17.sp, 
                    fontFamily = Rubik,
                    color = Color(0xFF0B3042),
                    letterSpacing = 0.01.sp
                ),
                modifier = Modifier.padding(bottom = 8.dp)
            )
            TextField(
                value = password,
                onValueChange = setPassword,
                placeholder = { Text("Enter your password", style = TextStyle(fontFamily = Rubik, fontSize = 16.sp)) },
                leadingIcon = {
                    Icon(
                        imageVector = Icons.Filled.Lock,
                        contentDescription = "Password Icon",
                        tint = Color(0xFF0B3042) 
                    )
                },
                visualTransformation = PasswordVisualTransformation(),
                colors = TextFieldDefaults.colors(
                    focusedContainerColor = Color.Transparent,
                    unfocusedContainerColor = Color.Transparent,
                    disabledContainerColor = Color.Transparent,
                    cursorColor = Color(0xFF0B3042),
                    focusedIndicatorColor = Color.Transparent, 
                    unfocusedIndicatorColor = Color.Transparent, 
                ),
                textStyle = TextStyle(fontSize = 16.sp, color = Color.Black, fontFamily = Rubik),
                singleLine = true,
                modifier = Modifier.fillMaxWidth()
            )
            Image(
                painter = painterResource(id = R.drawable.line_2_password), 
                contentDescription = "Password underline",
                modifier = Modifier
                    .fillMaxWidth()
                    .offset(x = 0.dp) // Adjust this value to align with "E"
                    .height(1.dp)
            )

            Spacer(modifier = Modifier.height(20.dp))

            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Checkbox(
                        checked = rememberMe,
                        onCheckedChange = setRememberMe,
                        colors = CheckboxDefaults.colors(
                            checkedColor = Color(0xFF0B3042),
                            uncheckedColor = Color(0xFF0B3042),
                            checkmarkColor = Color.White
                        ),
                        modifier = Modifier.size(20.dp) 
                    )
                    Spacer(modifier = Modifier.width(6.dp))
                    Text(
                        text = "Remember Me",
                        style = TextStyle(
                            fontSize = 13.sp, 
                            fontFamily = Rubik,
                            color = Color(0xFF0B3042),
                            letterSpacing = 0.02.sp
                        )
                    )
                }
                Text(
                    text = "Forgot Password?",
                    style = TextStyle(
                        fontSize = 13.sp, 
                        fontFamily = Rubik,
                        color = Color(0xFF2C5262),
                        letterSpacing = 0.02.sp
                    ),
                    modifier = Modifier.clickable { /* TODO: Implement Forgot Password */ }
                )
            }

            Spacer(modifier = Modifier.weight(1f)) 

            Button(
                onClick = { onLogin(email, password, rememberMe) },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(55.dp) 
                    .padding(bottom = 10.dp), 
                colors = ButtonDefaults.buttonColors(
                    containerColor = Color(0xFF2C5262) 
                ),
                shape = androidx.compose.foundation.shape.RoundedCornerShape(13.dp) 
            ) {
                Text(
                    text = "Login",
                    style = TextStyle(
                        fontSize = 20.sp, 
                        fontFamily = Rubik,
                        color = Color(0xFFF8F8FF),
                        letterSpacing = 0.01.sp,
                        textAlign = TextAlign.Center
                    )
                )
            }

            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(bottom = 30.dp), 
                horizontalArrangement = Arrangement.Center,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = "Don’t have an Account ? ",
                    style = TextStyle(
                        fontSize = 15.sp, 
                        fontFamily = Rubik,
                        color = Color(0xFF9E9E9E),
                        letterSpacing = 0.01.sp
                    )
                )
                Text(
                    text = "Sign up",
                    style = TextStyle(
                        fontSize = 15.sp, 
                        fontFamily = Rubik,
                        // fontWeight = FontWeight.Bold, // Removed
                        color = Color(0xFF0B3042),
                        letterSpacing = 0.01.sp
                    ),
                    modifier = Modifier.clickable { onNavigateToSignup() }
                )
            }
        }
    }
}
