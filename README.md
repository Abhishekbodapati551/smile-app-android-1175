# Smile App - Dental Care Adventure ⭐

Smile App is a comprehensive dental care management system featuring an Android application for patients (children) and a web dashboard for doctors. The project uses **Supabase** for real-time data, authentication, and storage.

## 🚀 Live Web Application
The doctor dashboard and patient web entry are hosted on GitHub Pages:
[https://abhishekbodapati551.github.io/smile-app-android-1175/web/index.html](https://abhishekbodapati551.github.io/smile-app-android-1175/web/index.html)

## ✨ Features

### 👦 For Patients (Android App & Web)
- **Brushing Timer**: A 2-minute interactive timer with camera verification.
- **Streak System**: Track daily brushing habits to earn points.
- **Rewards**: Redeem earned points for digital rewards like teddy bears and trophies.
- **Appointments**: View upcoming dental check-ups scheduled by your doctor.
- **Secure Login**: Personalized accounts with doctor-linkage via unique Doctor IDs.

### 👩‍⚕️ For Doctors (Web Dashboard)
- **Patient Management**: View all linked patients and their progress.
- **Approval System**: Review and approve new patient registrations.
- **Video Reviews**: Verify patient brushing sessions and award points.
- **Appointment Scheduler**: Manage clinic visits and notify patients in real-time.
- **Unique Doctor ID**: Every doctor gets a unique 4-digit code (starting from 1176) to share with patients.

## 🛠️ Tech Stack
- **Frontend (Mobile)**: Android (Java/Kotlin), XML Layouts.
- **Frontend (Web)**: HTML5, Tailwind CSS, JavaScript.
- **Backend**: Supabase (PostgreSQL, Auth, Realtime, Storage).
- **Database**: Room (Local Android persistence) & Supabase (Remote synchronization).

## 📦 Setup & Installation

### Android App
1. Open the project in **Android Studio**.
2. Ensure you have the `google-services.json` (if using GMS) or verify the `SupabaseManager.java` config.
3. Sync Gradle and run the `:app` module.

### Web Application
1. The web files are located in the `/web` directory.
2. Open `web/index.html` in any modern browser for local testing.

### Backend (Supabase)
The database schema can be initialized using the `database_setup.sql` file provided in the root directory.

## 🌐 Deploying to GitHub Pages
1. Push your code to the `main` branch.
2. Go to **Settings > Pages** in your GitHub repository.
3. Select **Branch: main** and folder **/(root)**.
4. Click **Save**.
5. Your app will be live at `https://<your-username>.github.io/smile-app-android-1175/web/index.html`.

---
*Created with ❤️ for better dental health.*
