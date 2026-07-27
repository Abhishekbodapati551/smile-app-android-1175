# Smile App - Dental Care Adventure ⭐

Smile App is a comprehensive dental care management system featuring an Android application for patients (children) and a web dashboard for doctors. The project uses **Supabase** for real-time data, authentication, and storage.

## 📁 Repository Structure
The repository is organized into the following clear categories:

### 1. 📱 Frontend (Mobile)
- **Folder**: [`app/`](app/)
- Contains the complete Android source code (Java/Kotlin/XML).

### 2. 🌐 Frontend (Web)
- **Main File**: [`index.html`](index.html) (Located at root for GitHub Pages)
- **Mirror Folder**: [`Web_Dashboard/`](Web_Dashboard/)
- Contains the Doctor's Dashboard and Patient Web Entry.

### 3. 🛠️ Backend & Database
- **Folder**: [`Database_Backend/`](Database_Backend/)
- Contains [`database_setup.sql`](Database_Backend/database_setup.sql) for initializing the Supabase/PostgreSQL schema.

### 4. 🧪 Automation & Testing
- **Folder**: [`Automation_Testing/`](Automation_Testing/)
    - **Web**: [`Web_Selenium_Tests/`](Automation_Testing/Web_Selenium_Tests/) (Selenium tests for the dashboard).
    - **Mobile**: [`Mobile_Appium_Tests/`](Automation_Testing/Mobile_Appium_Tests/) (Appium E2E tests for the Android app).

### 5. 📖 Documentation & Scripts
- **Documentation**: [`Documentation_and_Diagrams/`](Documentation_and_Diagrams/) (System architecture and diagrams).
- **Scripts**: [`Scripts_and_Tools/`](Scripts_and_Tools/) (Deployment and utility scripts).

---

## 🚀 Live Web Application
Hosted on GitHub Pages:
[https://abhishekbodapati551.github.io/smile-app-android-1175/](https://abhishekbodapati551.github.io/smile-app-android-1175/)

## ✨ Key Features
- **Mirror Synchronization**: Real-time data sync between Mobile and Web.
- **Brushing Mission**: Interactive 2-minute timer with camera verification.
- **Attendance Tracking**: Doctor-controlled attendance with automatic warning notes.
- **Reward Store**: Digital prize collection using earned points.

## 📦 Setup & Installation
Refer to the individual folders for specific setup instructions for the Android app, Web portal, and Automated tests.

---
*Developed for excellence in pediatric dental management.*
