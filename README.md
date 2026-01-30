# BlueLedger

[![Android](https://img.shields.io/badge/Android-35%2B-green)](#)
[![Kotlin](https://img.shields.io/badge/Kotlin-2.0-purple)](#)
[![Jetpack Compose](https://img.shields.io/badge/Jetpack%20Compose-2024.09-blue)](#)

BlueLedger is a mobile application for tracking and managing mangrove reforestation projects. It enables users to upload project data, track planting efforts, and mint carbon credits based on verified reforestation activities.

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Building](#building)
- [Project Structure](#project-structure)
- [Architecture](#architecture)
- [Core Concepts](#core-concepts)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## Features

- **User Authentication**: Local authentication with email-based signup and login
- **Project Management**: Create and manage reforestation projects with species tracking
- **GPS Integration**: Capture precise location data for planted areas
- **Carbon Credit System**: Automatically calculate and mint carbon credits based on mangrove species and hectares planted
  - Different species have different credit weights (Rhizophora: 14, Avicennia: 12, Bruguiera: 10 credits/hectare)
  - Bonus multipliers applied for larger planting areas (≥10 hectares: 1.2x, ≥5 hectares: 1.1x)
- **Wallet Summary**: View total credits minted and total hectares planted across all projects
- **Responsive Design**: Adaptive UI that works seamlessly across different screen sizes
- **Offline-First**: Local data persistence with DataStore
- **Multi-Language Support**: Ready for internationalization

## Getting Started

### Prerequisites

- **Android Studio**: Latest version with Android SDK 36
- **Java**: JDK 11 or higher
- **Gradle**: 8.13.0 (included via Gradle Wrapper)
- **Android Minimum SDK**: Level 24 (Android 7.0)
- **Android Target SDK**: Level 36 (Android 15)

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd BlueLedger
   ```

2. **Open in Android Studio**:
   - Launch Android Studio
   - Select "Open an Existing Project"
   - Navigate to the BlueLedger directory
   - Let Gradle sync automatically (or use File > Sync Now)

3. **Connect a device or emulator**:
   - Connect an Android device (API 24+) via USB with developer mode enabled, or
   - Create and launch an Android Virtual Device (AVD) from Android Studio

### Building

**Build the debug APK**:
```bash
./gradlew build
```

**Build and run on a connected device/emulator**:
```bash
./gradlew installDebug
```

**Or from Android Studio**:
- Click the "Run" button (green play icon) or press `Shift + F10`

**Create a release build**:
```bash
./gradlew assembleRelease
```

## Project Structure

```
BlueLedger/
├── app/
│   ├── src/
│   │   ├── main/
│   │   │   ├── java/com/example/blueledger/
│   │   │   │   ├── MainActivity.kt                 # Entry point
│   │   │   │   ├── BlueLedgerApp.kt               # Application class with DI container
│   │   │   │   ├── data/
│   │   │   │   │   ├── local/                      # DataStore persistence
│   │   │   │   │   ├── model/                      # Data models (User, UploadProject, etc.)
│   │   │   │   │   └── repo/                       # Repository layer (Auth, Projects)
│   │   │   │   ├── di/                             # Dependency injection setup
│   │   │   │   ├── navigation/                     # Navigation routes and graph
│   │   │   │   ├── ui/
│   │   │   │   │   ├── screens/
│   │   │   │   │   │   ├── splash/                 # Splash screen
│   │   │   │   │   │   ├── auth/                   # Login/Signup screens
│   │   │   │   │   │   ├── onboarding/             # Onboarding flow
│   │   │   │   │   │   └── home/                   # Main app screens
│   │   │   │   │   ├── theme/                      # Material 3 theming
│   │   │   │   │   └── viewmodel/                  # ViewModels for UI state
│   │   │   │   └── util/                           # Utilities (LocationHelper, etc.)
│   │   │   ├── res/
│   │   │   │   ├── drawable/                       # Vector drawables and images
│   │   │   │   ├── layout/                         # XML layouts
│   │   │   │   ├── values/                         # Strings, colors, dimens
│   │   │   │   └── font/                           # Custom fonts
│   │   │   └── AndroidManifest.xml
│   │   ├── androidTest/                            # Instrumented tests
│   │   └── test/                                   # Unit tests
│   ├── build.gradle.kts                            # App-level Gradle configuration
│   └── proguard-rules.pro
├── gradle/
│   ├── libs.versions.toml                          # Version catalog
│   └── wrapper/
├── build.gradle.kts                                # Project-level Gradle configuration
├── settings.gradle.kts                             # Gradle settings
└── README.md

```

## Architecture

BlueLedger follows **Clean Architecture** principles with clear separation of concerns:

### Layers

1. **UI Layer** (`ui/`)
   - Jetpack Compose-based screens
   - ViewModels for state management
   - Material 3 design system

2. **Domain Layer** (Implicit)
   - Use cases and business logic
   - Currently embedded in repositories

3. **Data Layer** (`data/`)
   - **Repositories**: Handle authentication and project operations
   - **Local Storage**: DataStore for preferences and encrypted user data
   - **Models**: Core data classes

4. **Dependency Injection** (`di/`)
   - Centralized container in `AppContainer`
   - Manual DI (ready for Hilt migration)

### Key Components

- **MainActivity**: Hosts Compose UI and navigation
- **BlueLedgerApp**: Application class with DI container
- **AppNavGraph**: Navigation definitions using Jetpack Navigation
- **DataStoreManager**: Centralized preference and data persistence
- **LocationHelper**: GPS location retrieval for project coordinates

## Core Concepts

### User Model
```kotlin
data class User(
    val email: String,
    val phone: String = "",
    val username: String = "",
)
```

### Upload Project
Represents a reforestation project with location and species data:
```kotlin
data class UploadProject(
    val id: String,
    val plotId: String,
    val species: String,           // e.g., "Rhizophora", "Avicennia"
    val hectares: Double,
    val gpsLat: Double,
    val gpsLng: Double,
    val imageUri: String? = null,
    val mintedCredits: Int = 0,   // Auto-calculated
    val timestamp: Long = System.currentTimeMillis()
)
```

### Carbon Credit Calculation
Credits are calculated based on:
1. **Species**: Different mangrove species have different carbon sequestration rates
   - Rhizophora: 14 credits/hectare
   - Avicennia: 12 credits/hectare
   - Bruguiera: 10 credits/hectare

2. **Area Multiplier**:
   - ≥10 hectares: 1.2x bonus
   - ≥5 hectares: 1.1x bonus
   - <5 hectares: 1.0x baseline

### Authentication Flow
- **Local-first**: Users are stored locally via DataStore (no backend yet)
- **Remember Me**: Optional persistent login
- **TODO**: Backend integration with token-based auth

## Development

### Technology Stack

| Component | Version | Purpose |
|-----------|---------|---------|
| Kotlin | 2.0.21 | Primary language |
| Jetpack Compose | 2024.09 | UI framework |
| Jetpack Navigation | 2.8.3 | Screen navigation |
| Room Database | 2.6.1 | (Prepared for future use) |
| DataStore | 1.1.1 | Local preferences & data |
| Lifecycle/ViewModel | 2.8.6 | State management |
| Gson | 2.11.0 | JSON serialization |
| Play Services Location | 21.3.0 | GPS integration |
| Material Icons Extended | 2024.09 | UI icons |

### Key Dependencies
See `gradle/libs.versions.toml` for full version catalog.

### Running Tests

**Unit tests**:
```bash
./gradlew test
```

**Instrumented tests**:
```bash
./gradlew connectedAndroidTest
```

### Debug Build

Debug builds include:
- Tooling previews for Compose
- Test manifests for UI testing
- Unminified code for easier debugging

### Release Build

Release builds include:
- ProGuard optimization and obfuscation
- Signing configuration (configure in `local.properties`)
- Size optimization

## Contributing

We welcome contributions! To get started:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes**: Follow the existing code style and architecture
4. **Test your changes**: Ensure existing tests pass
5. **Commit with clear messages**: `git commit -m "Add feature description"`
6. **Push to your fork**: `git push origin feature/your-feature-name`
7. **Open a Pull Request**: Provide a clear description of changes

### Code Style

- **Kotlin**: Follow [Kotlin official style guide](https://kotlinlang.org/docs/coding-conventions.html)
- **Naming**: Use clear, descriptive names; prefer explicit over implicit
- **Comments**: Document complex logic; use TODO comments for future work
- **Architecture**: Maintain clean separation between layers

### Common Development Tasks

**Add a new screen**:
1. Create a composable in `ui/screens/<feature>/`
2. Add ViewModel in `ui/viewmodel/` if needed
3. Add navigation route in `navigation/NavRoutes.kt`
4. Add route to `navigation/AppNavGraph.kt`

**Add a new data model**:
1. Define in `data/model/Models.kt`
2. Create repository methods in `data/repo/Repositories.kt`
3. Expose via appropriate data layer interfaces

**Local data persistence**:
- Use `DataStoreManager` in `data/local/DataStoreManager.kt`
- All user data is JSON-serialized via Gson for simplicity

## Known Limitations & TODOs

- **Backend Integration**: Auth and project verification currently use mock implementations
- **Database**: Room database is prepared but not yet used; consider migration for complex queries
- **API**: No real backend for credential minting; implement blockchain or backend verification
- **Payment**: Wallet/credit redemption flow not implemented
- **Testing**: Limited test coverage; more unit and integration tests needed
- **Internationalization**: Language support prepared but not fully implemented

## Support & Documentation

- **Issues**: Report bugs via GitHub Issues
- **Splash Screen**: See [SPLASH_IMPLEMENTATION.md](SPLASH_IMPLEMENTATION.md) for responsive design details
- **Android Documentation**: [Android Developers](https://developer.android.com)
- **Jetpack Compose**: [Compose Documentation](https://developer.android.com/jetpack/compose)

