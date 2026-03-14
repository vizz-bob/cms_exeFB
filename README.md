# XpertAI CMS — Windows Desktop App

A full-stack CMS (Content Management System) that runs as a **native Windows desktop application** — no internet required, no Python or Node.js needed on the target machine. Everything is bundled into a single `CMS_Setup.exe` installer.

---

## Technologies Used

| Layer | Technology | Purpose |
|---|---|---|
| **Backend** | Django 5.2 | Web framework, ORM, admin panel |
| **API** | Django REST Framework | JSON REST API for frontend |
| **Admin UI** | Jazzmin | Beautiful Django admin theme |
| **Frontend** | React 19 + Tailwind CSS | User-facing website |
| **Database** | SQLite3 | Embedded database (no server needed) |
| **WSGI Server** | Waitress | Pure-Python Windows-friendly server |
| **App Window** | PyWebView 5+ | Native desktop window (uses Edge WebView2) |
| **Bundler** | PyInstaller | Packages Python app into Windows .exe |
| **Installer** | Inno Setup 6 | Creates the Windows setup wizard |
| **CI/CD** | GitHub Actions | Builds the .exe automatically on every push |
| **Static Files** | WhiteNoise | Serves CSS/JS/images from Python |

---

## How It Works

```
CMS_Setup.exe  (Inno Setup installer — what the user downloads)
└── CMS_Server.exe  (PyInstaller bundle — the actual app)
    ├── launcher.py          ← Entry point: starts Django + opens window
    ├── Django backend       ← All Python code + dependencies frozen
    ├── React frontend       ← Pre-built static files (HTML/CSS/JS)
    ├── staticfiles/         ← Django collected static files
    └── templates/           ← HTML templates
```

**What happens when the user launches the app:**

1. `CMS_Server.exe` starts — PyInstaller extracts files to `_internal/`
2. `launcher.py` sets up the Django environment
3. Creates writable `cms_data/` folder (database + uploaded media stored here)
4. Django migrations run automatically (creates all database tables)
5. If no admin user exists → creates `admin / admin123` automatically
6. Waitress WSGI server starts on `http://127.0.0.1:8000`
7. PyWebView opens a native Windows app window showing the admin panel
8. If PyWebView fails → falls back to opening in the default browser

**Install location:** `%LOCALAPPDATA%\XpertAI CMS\` (no admin rights needed)
**Data location:** `%LOCALAPPDATA%\XpertAI CMS\cms_data\`
**Log file:** `%LOCALAPPDATA%\XpertAI CMS\cms_data\cms.log`

---

## Project Structure

```
cms_exe/
├── .github/
│   └── workflows/
│       └── build-installer.yml   ← GitHub Actions CI/CD pipeline
├── cms-backend/                  ← Django project
│   ├── launcher.py               ← PyInstaller entry point (CRITICAL)
│   ├── cms_backend.spec          ← PyInstaller build specification
│   ├── requirements.txt          ← Python dependencies
│   ├── manage.py
│   ├── backend/
│   │   ├── settings.py           ← Dev settings
│   │   ├── settings_standalone.py← .exe-specific settings
│   │   ├── urls.py
│   │   ├── urls_standalone.py    ← Adds React SPA catch-all
│   │   └── wsgi.py
│   ├── about/                    ← CMS app: About page
│   ├── blog/                     ← CMS app: Blog
│   ├── careers/                  ← CMS app: Careers
│   ├── homepage/                 ← CMS app: Homepage
│   └── ...                       ← Other CMS apps
├── cms-frontend/                 ← React 19 app
│   ├── src/
│   ├── public/
│   └── package.json
├── installer.iss                 ← Inno Setup script
└── README.md
```

---

## Key Files

### `cms-backend/launcher.py`
The heart of the desktop app. It:
- Sets up Django environment variables
- Points Django at `settings_standalone.py`
- Runs database migrations on startup
- Auto-creates `admin / admin123` if no superuser exists
- Starts Waitress server in a background thread
- Opens the admin panel in a PyWebView native window

### `cms-backend/cms_backend.spec`
PyInstaller specification. Tells PyInstaller exactly what to bundle:
- All Django apps and their templates/migrations
- All third-party packages (jazzmin, rest_framework, whitenoise, etc.)
- React production build
- Pre-collected static files
- **Note:** `db.sqlite3` is intentionally NOT bundled — the app always creates a fresh database on first run

### `cms-backend/backend/settings_standalone.py`
Django settings for the `.exe` mode:
- Database at `cms_data/db.sqlite3`
- Media at `cms_data/media/`
- Static files served by WhiteNoise
- `ALLOWED_HOSTS = ['127.0.0.1', 'localhost']`

### `installer.iss`
Inno Setup script that creates the Windows installer:
- Installs to `%LOCALAPPDATA%\XpertAI CMS` (no admin rights needed)
- Creates desktop shortcut
- Creates uninstaller

### `.github/workflows/build-installer.yml`
GitHub Actions pipeline (12 steps, ~5 minutes):
1. Checkout code
2. Set up Node.js 18
3. Set up Python 3.11
4. Build React frontend (`npm run build`)
5. Copy React build → `cms-backend/frontend_build/`
6. Install Python dependencies
7. Run Django `collectstatic` (gathers all CSS/JS)
8. Run PyInstaller → produces `CMS_Server.exe`
9. Install Inno Setup 6
10. Run Inno Setup → produces `CMS_Setup.exe`
11. Upload `CMS_Setup.exe` as artifact (30-day retention)
12. Create GitHub Release (if a version tag was pushed)

---

## Build & Deploy — Step by Step

### Prerequisites
- Mac (or any machine) with Git and GitHub CLI (`gh`) installed
- GitHub account with the repo at `https://github.com/vizz-bob/cms_exeFB`
- Windows machine (or VMware Windows VM) to run the app

---

### Step 1 — Make your code changes on Mac

```bash
cd /Users/vijayendrasingh/Claude-DevOps-Workspace/cms_exe
# ... edit files as needed ...
```

---

### Step 2 — Push to GitHub (triggers the build automatically)

```bash
git add .
git commit -m "your change description"
git push origin main
```

GitHub Actions starts building immediately. You can watch it at:
```
https://github.com/vizz-bob/cms_exeFB/actions
```

Build takes ~5 minutes. You will see a green ✅ when done.

---

### Step 3 — Download the new installer

```bash
# See recent builds
gh run list --repo vizz-bob/cms_exeFB --limit 5

# Download the latest build (replace RUN_ID with the ID from above)
gh run download RUN_ID --repo vizz-bob/cms_exeFB --dir ~/Downloads/cms_build

# Find the file
ls ~/Downloads/cms_build/
```

The `CMS_Setup.exe` will be inside `~/Downloads/cms_build/CMS_Setup_Windows/`.

---

### Step 4 — Install on Windows

1. Copy `CMS_Setup.exe` to your Windows machine (drag into VMware, USB, etc.)
2. Double-click `CMS_Setup.exe`
3. Click through the installer (no admin rights needed)
4. Launch **XpertAI CMS** from the desktop shortcut

---

### Step 5 — First Login

The app opens the admin panel automatically.

- **URL:** `http://127.0.0.1:8000/admin/`
- **Username:** `admin`
- **Password:** `admin123`

> ⚠️ Change your password immediately: click **Admin** (top right) → **Change password**

---

### Step 6 — Managing Content

From the admin panel you can manage:
- **About** — About page content, Awards, Team Members, Technology Stack
- **Blog** — Blog posts
- **Careers** — Job listings
- **Homepage** — Homepage sections
- **Services** — Services page content
- **Contact / Leads** — Form submissions
- **Auth Tokens** — API authentication tokens

---

## Rebuilding from Scratch

If you ever need to start completely fresh:

```bash
# 1. Clone the repo
git clone https://github.com/vizz-bob/cms_exeFB.git
cd cms_exeFB

# 2. Push any change to trigger a build
git commit --allow-empty -m "trigger build"
git push origin main

# 3. Download the installer
gh run download --repo vizz-bob/cms_exeFB --dir ~/Downloads/cms_build
```

---

## Local Development (Mac)

```bash
# Terminal 1 — Django backend
cd cms-backend
source venv/bin/activate
python manage.py runserver 0.0.0.0:8000

# Terminal 2 — React frontend
cd cms-frontend
npm start

# Terminal 3 — Build React and collect static (before building .exe)
cd cms-frontend && npm run build
cp -r build ../cms-backend/frontend_build
cd ../cms-backend
CMS_BUILD_MODE=true python manage.py collectstatic --noinput
```

---

## Troubleshooting

### App opens but "site can't be reached"
The server is still starting. Wait 20 seconds and refresh.

### Login not working after reinstall
The old database may still exist. On Windows PowerShell:
```powershell
Stop-Process -Name "CMS_Server" -Force
Remove-Item "$env:LOCALAPPDATA\XpertAI CMS\cms_data\db.sqlite3" -Force
Remove-Item "$env:LOCALAPPDATA\XpertAI CMS\_internal\db.sqlite3" -Force
```
Then relaunch the app — it will create a fresh `admin / admin123` account.

### Check the app log
```powershell
Get-Content "$env:LOCALAPPDATA\XpertAI CMS\cms_data\cms.log" -Tail 20
```

### GitHub Actions build failed
Check the Actions tab at `https://github.com/vizz-bob/cms_exeFB/actions` for the error. Common causes:
- Missing Python package → add to `requirements.txt`
- Missing Django app module → add to `hiddenimports` in `cms_backend.spec`
- React build error → check `cms-frontend/` for syntax errors

### Artifact download fails
```bash
# List runs with full IDs
gh run list --repo vizz-bob/cms_exeFB --limit 5

# Download by run ID
gh run download RUN_ID --repo vizz-bob/cms_exeFB --dir ~/Downloads/cms_build
```

---

## Creating a Versioned Release

To create a permanent GitHub Release (not just a 30-day artifact):

```bash
git tag v1.0.0
git push origin v1.0.0
```

This triggers the workflow and automatically creates a Release at:
```
https://github.com/vizz-bob/cms_exeFB/releases
```

---

## Data Locations on Windows

| What | Location |
|---|---|
| App files | `%LOCALAPPDATA%\XpertAI CMS\_internal\` |
| Database | `%LOCALAPPDATA%\XpertAI CMS\cms_data\db.sqlite3` |
| Uploaded media | `%LOCALAPPDATA%\XpertAI CMS\cms_data\media\` |
| Log file | `%LOCALAPPDATA%\XpertAI CMS\cms_data\cms.log` |
| Desktop shortcut | `%USERPROFILE%\Desktop\XpertAI CMS.lnk` |
