# Building the XpertAI CMS Windows Installer

This guide explains how to produce `CMS_Setup.exe` — a one-click Windows installer
that bundles your Django backend + React frontend into a self-contained desktop app.

---

## Architecture overview

```
CMS_Setup.exe  (installer)
    └── installs CMS_Server/          (PyInstaller bundle, ~150–300 MB)
            ├── CMS_Server.exe        ← double-click to start
            ├── _internal/            ← Python runtime + Django apps
            ├── staticfiles/          ← pre-collected CSS/JS assets
            ├── frontend_build/       ← React production build
            ├── templates/            ← Django HTML templates
            └── db.sqlite3            ← initial empty database

On first run the app creates:
    CMS_Server/cms_data/
        ├── db.sqlite3   ← writable database
        └── media/       ← uploaded images / files
```

When launched, `CMS_Server.exe`:
1. Copies the initial database to `cms_data/` (first run only)
2. Runs Django migrations automatically
3. Starts a local web server on `http://127.0.0.1:8000`
4. Opens your default browser automatically

---

## Prerequisites  (install once)

| Tool | Where to get it | Notes |
|---|---|---|
| **Python 3.10+** | https://python.org | Tick "Add Python to PATH" during install |
| **Node.js 18+** | https://nodejs.org | Includes npm |
| **Inno Setup 6** | https://jrsoftware.org/isinfo.php | For the final `.exe` installer |
| **Git** | https://git-scm.com | To clone the repos |

---

## Folder structure expected

```
cms_exe/                    ← run build_installer.bat from here
    cms-frontend/           ← https://github.com/vizz-bob/cms_exeFB
    cms-backend/            ← https://github.com/vizz-bob/cms_exeFB
    build_installer.bat     ← ← ← run this
    installer.iss
    BUILD_INSTRUCTIONS.md
```

Clone both repos if you haven't already:

```bat
git clone https://github.com/vizz-bob/cms_exeFB
git clone https://github.com/vizz-bob/cms_exeFB
```

---

## Build steps (automated)

### Option A — One-click build (recommended)

1. Open **Command Prompt** or **PowerShell** as Administrator
2. `cd` into the `cms_exe` folder
3. Run:
   ```
   build_installer.bat
   ```
4. Wait ~10–20 minutes for the full build
5. Your installer will be at **`Output\CMS_Setup.exe`**

---

### Option B — Manual step-by-step

If you prefer to run each step yourself:

```bat
REM --- 1. Build React ---
cd cms-frontend
npm install --legacy-peer-deps
npm run build
cd ..

REM --- 2. Copy React build into Django ---
xcopy /s /e /i cms-frontend\build cms-backend\frontend_build

REM --- 3. Install Python packages ---
cd cms-backend
pip install -r requirements.txt
pip install waitress pyinstaller

REM --- 4. Collect static files ---
set DJANGO_SETTINGS_MODULE=backend.settings_standalone
set ALLOWED_HOSTS=localhost,127.0.0.1
set DJANGO_SECRET_KEY=build-time-key-123
set CMS_BUILD_MODE=true
set CMS_BUNDLE_DIR=%cd%
set CMS_DATA_DIR=%cd%\build_data
mkdir build_data
python manage.py collectstatic --noinput

REM --- 5. Build the .exe bundle ---
pyinstaller cms_backend.spec --clean --noconfirm
cd ..

REM --- 6. Build the installer ---
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
```

---

## What the build produces

| File / folder | Description |
|---|---|
| `cms-backend/dist/CMS_Server/` | Raw PyInstaller bundle (no installer needed, can be zipped and shared) |
| `Output/CMS_Setup.exe` | Polished Windows installer with shortcuts + uninstaller |

---

## After installation — first-time setup

1. Launch **XpertAI CMS** from the Start Menu or Desktop shortcut
2. Wait for the console to say **"Server running at http://127.0.0.1:8000"**
3. Your browser opens automatically
4. To create an admin account, open a **new** Command Prompt, `cd` to the install
   folder and run:
   ```bat
   CMS_Server.exe createsuperuser
   ```
   *(Or use the Django admin panel at `/admin/` after the first user is created via the app's setup flow.)*

---

## Troubleshooting

| Problem | Solution |
|---|---|
| `python: command not found` | Reinstall Python, tick "Add to PATH" |
| `npm: command not found` | Reinstall Node.js |
| `ModuleNotFoundError: No module named 'waitress'` | Run `pip install waitress` again |
| PyInstaller missing hidden import | Add the module name to `hiddenimports` in `cms_backend.spec` and rebuild |
| Port 8000 already in use | Stop the other process, or change the port in `launcher.py` |
| Browser opens but shows blank page | Wait 5–10 seconds and refresh — Django may still be starting |
| Static files (CSS/JS) not loading | Re-run `collectstatic` then rebuild the PyInstaller bundle |

---

## Customisation

### Change port
Edit `launcher.py` → `serve(application, host='127.0.0.1', port=8000, …)`

### Add an app icon
1. Place a `icon.ico` file in `cms-backend/`
2. In `cms_backend.spec`: `icon='icon.ico'`
3. In `installer.iss`: `SetupIconFile=cms-backend\icon.ico`

### Enable real email sending
Edit `cms_exe/cms-backend/backend/settings_standalone.py`:
- Change `EMAIL_BACKEND` to `'django.core.mail.backends.smtp.EmailBackend'`
- Set `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`

### Configure a secret key for production
Create a file called `.env` next to `CMS_Server.exe` after installing:
```
DJANGO_SECRET_KEY=your-very-long-random-secret-key-here
```

---

## Files added to your project

| File | Location | Purpose |
|---|---|---|
| `launcher.py` | `cms-backend/` | PyInstaller entry point |
| `settings_standalone.py` | `cms-backend/backend/` | Django settings for .exe mode |
| `urls_standalone.py` | `cms-backend/backend/` | Django URLs + React catch-all |
| `cms_backend.spec` | `cms-backend/` | PyInstaller build configuration |
| `build_installer.bat` | `cms_exe/` | One-click build script |
| `installer.iss` | `cms_exe/` | Inno Setup installer script |
| `BUILD_INSTRUCTIONS.md` | `cms_exe/` | This file |

No existing source files were modified.
