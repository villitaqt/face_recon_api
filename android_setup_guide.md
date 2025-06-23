# Android Client Setup Guide

## 🛠️ Project Creation Steps

### 1. Open Android Studio
- Launch Android Studio
- Click "New Project"

### 2. Choose Project Template
- Select "Empty Views Activity" (for traditional approach)
- OR "Empty Compose Activity" (for modern Jetpack Compose)

### 3. Configure Project
```
Name: FaceRecognitionApp
Package name: com.facerecon.app
Language: Kotlin
Minimum SDK: API 24 (Android 7.0)
Build configuration language: Kotlin DSL
```

### 4. Project Structure
```
FaceRecognitionApp/
├── app/
│   ├── src/main/
│   │   ├── java/com/facerecon/app/
│   │   │   ├── data/
│   │   │   │   ├── api/
│   │   │   │   ├── database/
│   │   │   │   ├── repository/
│   │   │   │   └── models/
│   │   │   ├── ui/
│   │   │   │   ├── screens/
│   │   │   │   ├── components/
│   │   │   │   └── theme/
│   │   │   ├── utils/
│   │   │   └── MainActivity.kt
│   │   └── res/
│   │       ├── values/
│   │       ├── drawable/
│   │       └── layout/
│   └── build.gradle.kts
└── build.gradle.kts
```

## 📱 Essential Dependencies

### Add to `app/build.gradle.kts`:

```kotlin
plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
    id("kotlin-kapt")
    id("dagger.hilt.android.plugin")
    id("kotlin-parcelize")
}

android {
    namespace = "com.facerecon.app"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.facerecon.app"
        minSdk = 24
        targetSdk = 34
        versionCode = 1
        versionName = "1.0"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }
    
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_1_8
        targetCompatibility = JavaVersion.VERSION_1_8
    }
    
    kotlinOptions {
        jvmTarget = "1.8"
    }
    
    buildFeatures {
        compose = true
    }
    
    composeOptions {
        kotlinCompilerExtensionVersion = "1.5.1"
    }
}

dependencies {
    // Core Android
    implementation("androidx.core:core-ktx:1.12.0")
    implementation("androidx.appcompat:appcompat:1.6.1")
    implementation("com.google.android.material:material:1.11.0")
    implementation("androidx.constraintlayout:constraintlayout:2.1.4")
    
    // Jetpack Compose
    implementation(platform("androidx.compose:compose-bom:2024.02.00"))
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-graphics")
    implementation("androidx.compose.ui:ui-tooling-preview")
    implementation("androidx.compose.material3:material3")
    implementation("androidx.activity:activity-compose:1.8.2")
    
    // CameraX
    implementation("androidx.camera:camera-core:1.3.1")
    implementation("androidx.camera:camera-camera2:1.3.1")
    implementation("androidx.camera:camera-lifecycle:1.3.1")
    implementation("androidx.camera:camera-view:1.3.1")
    
    // Networking
    implementation("com.squareup.retrofit2:retrofit:2.9.0")
    implementation("com.squareup.retrofit2:converter-gson:2.9.0")
    implementation("com.squareup.okhttp3:logging-interceptor:4.12.0")
    
    // Dependency Injection
    implementation("com.google.dagger:hilt-android:2.48")
    kapt("com.google.dagger:hilt-compiler:2.48")
    
    // Image Loading
    implementation("io.coil-kt:coil-compose:2.5.0")
    
    // Permissions
    implementation("com.google.accompanist:accompanist-permissions:0.32.0")
    
    // Lifecycle
    implementation("androidx.lifecycle:lifecycle-viewmodel-ktx:2.7.0")
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.7.0")
    
    // Navigation
    implementation("androidx.navigation:navigation-compose:2.7.7")
    
    // Testing
    testImplementation("junit:junit:4.13.2")
    androidTestImplementation("androidx.test.ext:junit:1.1.5")
    androidTestImplementation("androidx.test.espresso:espresso-core:3.5.1")
    androidTestImplementation(platform("androidx.compose:compose-bom:2024.02.00"))
    androidTestImplementation("androidx.compose.ui:ui-test-junit4")
    debugImplementation("androidx.compose.ui:ui-tooling")
    debugImplementation("androidx.compose.ui:ui-test-manifest")
}
```

## 🔧 Project Configuration

### 1. Add to `build.gradle.kts` (Project level):
```kotlin
plugins {
    id("com.android.application") version "8.2.2" apply false
    id("org.jetbrains.kotlin.android") version "1.9.0" apply false
    id("com.google.dagger.hilt.android") version "2.48" apply false
}
```

### 2. Add to `settings.gradle.kts`:
```kotlin
pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}

rootProject.name = "FaceRecognitionApp"
include(":app")
```

## 📋 Permissions Setup

### Add to `AndroidManifest.xml`:
```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools">

    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.CAMERA" />
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" 
        android:maxSdkVersion="32" />
    <uses-permission android:name="android.permission.READ_MEDIA_IMAGES" />
    <uses-permission android:name="android.permission.VIBRATE" />
    <uses-permission android:name="android.permission.POST_NOTIFICATIONS" />
    
    <uses-feature
        android:name="android.hardware.camera"
        android:required="true" />

    <application
        android:name=".FaceRecognitionApp"
        android:allowBackup="true"
        android:dataExtractionRules="@xml/data_extraction_rules"
        android:fullBackupContent="@xml/backup_rules"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.FaceRecognitionApp"
        tools:targetApi="31">
        
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:theme="@style/Theme.FaceRecognitionApp">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
```

## 🎯 Next Steps After Project Creation

1. **Sync Project**: Click "Sync Now" in Android Studio
2. **Create Package Structure**: Create the folders as shown above
3. **Copy API Models**: Use the models provided in the next files
4. **Test Basic Setup**: Run the app to ensure it builds successfully

## 🔍 Common Issues & Solutions

### Issue: Gradle Sync Fails
- **Solution**: Update Android Studio to latest version
- **Solution**: Check internet connection for dependencies

### Issue: Compose Preview Not Working
- **Solution**: Invalidate caches and restart (File > Invalidate Caches)

### Issue: Camera Permissions
- **Solution**: Ensure permissions are properly declared in manifest
- **Solution**: Request permissions at runtime

## 📱 Testing Setup

### 1. Physical Device (Recommended)
- Enable Developer Options
- Enable USB Debugging
- Connect via USB

### 2. Emulator
- Create AVD with API 24+
- Enable camera in emulator settings

## 🚀 Ready to Code!

Once you've created the project and added the dependencies, you'll be ready to implement the actual app code. The next files will provide you with the essential Kotlin classes to get started quickly. 