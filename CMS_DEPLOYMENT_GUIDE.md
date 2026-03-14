# XpertAI CMS — Complete Deployment Guide

> Everything you need to understand how the Windows `.exe` works, how to build it, and how to deploy it again from scratch.

---

## Table of Contents

1. [How the .exe Works](#how-the-exe-works)
2. [Project Structure](#project-structure)
3. [Key Files Explained](#key-files-explained)
4. [Build Method 1 — GitHub Actions (Recommended)](#build-method-1--github-actions-recommended)
5. [Build Method 2 — Build Locally on Windows](#build-method-2--build-locally-on-windows)
6. [Install and Run on Windows](#install-and-run-on-windows)
7. [First-Time Setup After Install](#first-time-setup-after-install)
8. [Troubleshooting](#troubleshooting)
9. [Making Changes and Rebuilding](#making-changes-and-rebuilding)

---

## How the .exe Works

The Windows installer bundles **three things** into a single `CMS_Setup.exe`:

```
CMS_Setup.exe  (Inno Setup installer)
└── CMS_Server.exe  (PyInstaller bundle)
    ├── Django backend  (Python + all dependencies, frozen)
    ├── React frontend  (pre-built static files)
    ├── SQLite database (initial db.sqlite3)
    └── All static files (CSS, JS, images)
```

**When a user runs `CMS_Server.exe`:**

1. PyInstaller extracts all bundled files to a temp `_internal/` directory
2. `launcher.py` sets up the Django environment
3. It creates a writable `cms_data/` folder next to the `.exe` (for the database and uploaded media)
4. Django migrations run automatically
5. The browser opens at `http://127.0.0.1:8000`
6. The **Waitress** WSGI server starts serving the app (pure Python, Windows-friendly)

The app runs entirely **offline** — no internet required, no Python or Node.js needed on the target machine.

---

## Project Structure

```
cms_exe/
├── .github/
│   └── workflows/
│       └── build-installer.yml     ← GitHub Actions CI build
│
├── cms-backend/                    ← Django project
│   ├── backend/
│   │   ├── settings.py             ← Dev settings
│   │   ├── settings_standalone.py  ← Standalone .exe settings
│   │   ├── urls.py                 ← Dev URL config
│   │   └── urls_standalone.py      ← .exe URL config (includes React catch-all)
│   ├── launcher.py                 ← Entry point for the .exe
│   ├── cms_backend.spec            ← PyInstaller build spec
│   ├── requirements.txt            ← Python dependencies
│   └── manage.py
│
├── cms-frontend/                   ← React app
│   ├── src/
│   ├── public/
│   └── package.json
│
├── installer.iss                   ← Inno Setup script (creates CMS_Setup.exe)
├── build_installer.bat             ← One-click build script for Windows
└── CMS_DEPLOYMENT_GUIDE.md        ← This file
```

---

## Key Files Explained

### `launcher.py`
The entry point that PyInstaller compiles into `CMS_Server.exe`. It:
- Detects whether it's running as a frozen `.exe` or in dev mode
- Creates the writable `cms_data/` directory (database + media)
- Sets Django environment variables
- Runs database migrations
- Opens the browser after 2.5 seconds
- Starts the **Waitress** server on `http://127.0.0.1:8000`

### `cms_backend.spec`
PyInstaller configuration that tells it exactly what to bundle:
- All Django apps and their templates, migrations, static files
- All third-party packages (jazzmin, rest_framework, whitenoise, etc.)
- The React production build (`frontend_build/`)
- The pre-collected static files (`staticfiles/`)
- The initial SQLite database

### `backend/settings_standalone.py`
Django settings used only by the `.exe`. Key differences from `settings.py`:
- Uses **Waitress** instead of Django dev server
- Serves static files via **WhiteNoise** (no separate web server needed)
- Database is stored in `cms_data/db.sqlite3` (writable location next to `.exe`)
- Media uploads stored in `cms_data/media/`
- Email uses console backend (no SMTP needed)
- AWS storage disabled

### `backend/urls_standalone.py`
Extends the normal URL config with a **React SPA catch-all** — any URL that isn't `/api/` or `/admin/` serves the React app's `index.html`, enabling React Router to work.

### `installer.iss`
Inno Setup script that:
- Takes the PyInstaller output (`cms-backend/dist/CMS_Server/`)
- Packages it into a single `CMS_Setup.exe` installer
- Installs to `C:\Users\<user>\AppData\Local\XpertAI CMS\` (no admin rights needed)
- Creates Start Menu shortcut
- Optionally creates Desktop shortcut

### `build_installer.bat`
One-click build script for Windows. Runs all 6 steps automatically:
1. `npm install && npm run build` (React)
2. Copies React build → `cms-backend/frontend_build/`
3. `pip install -r requirements.txt` + waitress + pyinstaller
4. `python manage.py collectstatic`
5. `pyinstaller cms_backend.spec`
6. `ISCC.exe installer.iss` → `Output/CMS_Setup.exe`

---

## Build Method 1 — GitHub Actions (Recommended)

This builds the `.exe` automatically in the cloud on a real Windows machine. No local setup needed.

### Automatic build (on every push)
```bash
git add .
git commit -m "your changes"
git push
```
GitHub Actions triggers automatically and builds `CMS_Setup.exe`.

### Manual build (trigger without a commit)
1. Go to `https://github.com/vizz-bob/cms_exeFB/actions`
2. Click **"Build Windows Installer"** in the left sidebar
3. Click **"Run workflow"** → **"Run workflow"**
4. Wait ~15 minutes for the build to complete

### Download the built `.exe`

**Via GitHub website:**
1. Go to `https://github.com/vizz-bob/cms_exeFB/actions`
2. Click the latest successful run (green ✅)
3. Scroll to **Artifacts** section at the bottom
4. Click **"CMS_Setup_Windows"** to download the zip
5. Unzip → `CMS_Setup.exe`

**Via GitHub CLI (from Mac terminal):**
```bash
# Install GitHub CLI
brew install gh
gh auth login

# Find the latest run ID
gh run list --repo vizz-bob/cms_exeFB --json databaseId,displayTitle -L 1

# Download (replace RUN_ID with the actual number)
gh run download RUN_ID --repo vizz-bob/cms_exeFB --name CMS_Setup_Windows --dir ~/Desktop/CMS_exe
```

### Create a permanent download link (GitHub Release)
```bash
git tag v1.0.0
git push origin v1.0.0
```
This creates a release at `https://github.com/vizz-bob/cms_exeFB/releases` with a permanent clickable download link.

---

## Build Method 2 — Build Locally on Windows

Use this if you want to build on your own Windows machine instead of GitHub Actions.

### Prerequisites (install once)

| Tool | Download | Notes |
|------|----------|-------|
| Python 3.11 | https://python.org/downloads | Tick **"Add Python to PATH"** |
| Node.js 18+ | https://nodejs.org | LTS version |
| Git | https://git-scm.com | |
| Inno Setup 6 | https://jrsoftware.org/isinfo.php | For the final installer |

### Steps

**1. Clone the repo on Windows:**
```cmd
git clone https://github.com/vizz-bob/cms_exeFB cms_exe
cd cms_exe
```

**2. Run the one-click build script:**
```cmd
build_installer.bat
```

**3. Find your installer:**
```
cms_exe\Output\CMS_Setup.exe
```

The build takes 10–20 minutes the first time (downloading all packages).

---

## Install and Run on Windows

### Install
1. Copy `CMS_Setup.exe` to the Windows machine
2. Double-click `CMS_Setup.exe`
3. Follow the installer wizard (Next → Next → Install)
4. Optionally tick **"Create desktop shortcut"**
5. Click **Finish**

The app installs to:
```
C:\Users\<YourName>\AppData\Local\XpertAI CMS\
```

### Run
- **Start Menu** → search **"XpertAI CMS"** → click it
- Or double-click the Desktop shortcut if you created one
- Or from Command Prompt:
  ```cmd
  cd "%LOCALAPPDATA%\XpertAI CMS"
  CMS_Server.exe
  ```

**Important:** The black console window that opens must stay open. Closing it stops the server.

### Access the app
| URL | Description |
|-----|-------------|
| `http://127.0.0.1:8000` | Main website (React frontend) |
| `http://127.0.0.1:8000/admin/` | Django admin panel |
| `http://127.0.0.1:8000/api/` | REST API |

---

## First-Time Setup After Install

### Create an admin user

The first time you install, you need to create a superuser to log into `/admin/`.

**Option A — From Command Prompt on Windows:**
```cmd
cd "%LOCALAPPDATA%\XpertAI CMS\_internal"
CMS_Server.exe createsuperuser
```

**Option B — Run `CMS_Server.exe`, then in a second Command Prompt:**
```cmd
cd "%LOCALAPPDATA%\XpertAI CMS\_internal"
python manage.py createsuperuser --settings=backend.settings_standalone
```

Enter a username, email, and password when prompted. Then visit `http://127.0.0.1:8000/admin/` and log in.

### Data storage
All user-generated data is stored in:
```
C:\Users\<YourName>\AppData\Local\XpertAI CMS\cms_data\
├── db.sqlite3   ← Database (all content, users, etc.)
└── media\       ← Uploaded files (images, documents)
```

**Back up this folder regularly** — it contains all your content.

---

## Troubleshooting

### `ModuleNotFoundError: No module named 'xyz'`
A Python module wasn't bundled by PyInstaller. Fix:
1. Open `cms-backend/cms_backend.spec` on Mac
2. Find the `_extra_hidden` list
3. Add `'xyz'` to the list
4. Push to GitHub → new build → reinstall

### `PermissionError: Access is denied`
The app is trying to write to a protected location. Fix:
- Right-click `CMS_Server.exe` → **Run as Administrator**
- Or reinstall with the latest `CMS_Setup.exe` (which installs to AppData, not Program Files)

### `Site can't be reached` at `127.0.0.1:8000`
The server isn't running. Fix:
- Make sure the black console window is open and shows `[CMS] Server running at http://127.0.0.1:8000`
- If the window closed with an error, open Command Prompt and run `CMS_Server.exe` to see the error

### Static files not loading (CSS/JS broken)
The `staticfiles/` directory wasn't bundled. Fix:
On Mac, run:
```bash
cd cms-backend
source venv/bin/activate
CMS_BUILD_MODE=true python manage.py collectstatic --noinput --settings=backend.settings_standalone
```
Then push and rebuild.

### React frontend shows blank page or 404
The React build wasn't copied to `cms-backend/frontend_build/`. Fix:
```bash
cd cms-frontend
npm run build
cp -r build ../cms-backend/frontend_build
```
Then run collectstatic and rebuild.

### Black console window flashes and immediately closes
The app crashed on startup. Run it from Command Prompt to see the error:
```cmd
cd "%LOCALAPPDATA%\XpertAI CMS"
CMS_Server.exe
```

---

## Making Changes and Rebuilding

### Workflow for any change

```
Make changes on Mac
       ↓
git add . && git commit -m "description" && git push
       ↓
GitHub Actions builds new CMS_Setup.exe (~15 min)
       ↓
Download new CMS_Setup.exe from GitHub Actions artifacts
       ↓
On Windows: Uninstall old version → Install new version
```

### Backend change (Django / Python)
1. Edit files in `cms-backend/`
2. Test locally: `python launcher.py` from `cms-backend/`
3. Push → GitHub builds new `.exe`

### Frontend change (React)
1. Edit files in `cms-frontend/src/`
2. Test locally: `npm start` from `cms-frontend/`
3. Push → GitHub builds new `.exe`

### Adding a new Python package
1. Install it: `pip install package-name`
2. Add to `cms-backend/requirements.txt`
3. Add to `_extra_hidden` in `cms-backend/cms_backend.spec`:
   ```python
   'package_name',
   'package_name.submodule',
   ```
4. Push → rebuild

### Changing the app version
Edit `installer.iss`:
```ini
#define AppVersion   "1.1.0"
```

---

## Quick Reference

```bash
# Test backend locally (Mac)
cd cms-backend && source venv/bin/activate && python launcher.py

# Test frontend locally (Mac)
cd cms-frontend && npm start

# Build React + copy to backend (Mac)
cd cms-frontend && npm run build && cp -r build ../cms-backend/frontend_build

# Collect static files (Mac)
cd cms-backend && CMS_BUILD_MODE=true python manage.py collectstatic --noinput --settings=backend.settings_standalone

# Trigger GitHub Actions build
git add . && git commit -m "rebuild" && git push

# Download latest .exe (Mac)
gh run list --repo vizz-bob/cms_exeFB --json databaseId -L 1
gh run download <RUN_ID> --repo vizz-bob/cms_exeFB --name CMS_Setup_Windows --dir ~/Desktop/CMS_exe

# Create a release with permanent download link
git tag v1.0.0 && git push origin v1.0.0
```

---

*Last updated: March 2026 | Repo: https://github.com/vizz-bob/cms_exeFB*
