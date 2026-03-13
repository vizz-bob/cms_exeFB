@echo off
setlocal enabledelayedexpansion

echo.
echo =============================================================
echo   XpertAI CMS  —  Windows Installer Builder
echo =============================================================
echo.

REM ---------------------------------------------------------------
REM Store the root folder (where this .bat lives)
REM ---------------------------------------------------------------
set "ROOT_DIR=%~dp0"
set "ROOT_DIR=%ROOT_DIR:~0,-1%"

REM ---------------------------------------------------------------
REM STEP 0 — Check prerequisites
REM ---------------------------------------------------------------
echo [0/6] Checking prerequisites...

where python >nul 2>&1
if errorlevel 1 (
    echo.
    echo  ERROR: Python is not installed or not in PATH.
    echo  Download Python 3.10+ from https://python.org
    echo  Make sure to tick "Add Python to PATH" during install.
    pause & exit /b 1
)

python --version
echo     Python OK

where node >nul 2>&1
if errorlevel 1 (
    echo.
    echo  ERROR: Node.js is not installed or not in PATH.
    echo  Download Node.js from https://nodejs.org
    pause & exit /b 1
)
node --version
echo     Node.js OK

where npm >nul 2>&1
if errorlevel 1 (
    echo  ERROR: npm not found.
    pause & exit /b 1
)
npm --version
echo     npm OK

REM Check Inno Setup (optional — installer won't be built if missing)
set "INNO_FOUND=0"
set "INNO_PATH="
if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
    set "INNO_PATH=C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
    set "INNO_FOUND=1"
)
if exist "C:\Program Files\Inno Setup 6\ISCC.exe" (
    set "INNO_PATH=C:\Program Files\Inno Setup 6\ISCC.exe"
    set "INNO_FOUND=1"
)
if "%INNO_FOUND%"=="1" (
    echo     Inno Setup 6 OK
) else (
    echo     Inno Setup 6 NOT FOUND ^(installer .exe will be skipped^)
    echo     Download from: https://jrsoftware.org/isinfo.php
)

echo.
echo All required prerequisites satisfied. Starting build...
echo.

REM ---------------------------------------------------------------
REM STEP 1 — Build React frontend
REM ---------------------------------------------------------------
echo [1/6] Building React frontend...
echo.

cd /d "%ROOT_DIR%\cms-frontend"

call npm install --legacy-peer-deps
if errorlevel 1 (
    echo  ERROR: npm install failed.
    cd /d "%ROOT_DIR%"
    pause & exit /b 1
)

call npm run build
if errorlevel 1 (
    echo  ERROR: React build failed.
    cd /d "%ROOT_DIR%"
    pause & exit /b 1
)

cd /d "%ROOT_DIR%"
echo     React build complete!
echo.

REM ---------------------------------------------------------------
REM STEP 2 — Copy React build into Django project
REM ---------------------------------------------------------------
echo [2/6] Copying React build into cms-backend\frontend_build\...
echo.

if exist "%ROOT_DIR%\cms-backend\frontend_build" (
    rmdir /s /q "%ROOT_DIR%\cms-backend\frontend_build"
)
xcopy /s /e /i "%ROOT_DIR%\cms-frontend\build" "%ROOT_DIR%\cms-backend\frontend_build" >nul

echo     Copy complete!
echo.

REM ---------------------------------------------------------------
REM STEP 3 — Install Python dependencies
REM ---------------------------------------------------------------
echo [3/6] Installing Python dependencies...
echo.

cd /d "%ROOT_DIR%\cms-backend"

pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo  ERROR: pip install -r requirements.txt failed.
    cd /d "%ROOT_DIR%"
    pause & exit /b 1
)

pip install waitress pyinstaller --quiet
if errorlevel 1 (
    echo  ERROR: Could not install waitress / pyinstaller.
    cd /d "%ROOT_DIR%"
    pause & exit /b 1
)

echo     Python dependencies installed!
echo.

REM ---------------------------------------------------------------
REM STEP 4 — Collect Django static files
REM ---------------------------------------------------------------
echo [4/6] Collecting Django static files...
echo.

mkdir "%ROOT_DIR%\cms-backend\build_data" 2>nul

set DJANGO_SETTINGS_MODULE=backend.settings_standalone
set ALLOWED_HOSTS=localhost,127.0.0.1
set DJANGO_SECRET_KEY=build-time-key-do-not-use-in-production
set CMS_BUILD_MODE=true
set CMS_BUNDLE_DIR=%ROOT_DIR%\cms-backend
set CMS_DATA_DIR=%ROOT_DIR%\cms-backend\build_data

python manage.py collectstatic --noinput --verbosity=1
if errorlevel 1 (
    echo  WARNING: collectstatic returned an error.
    echo           The build will continue, but static files may be missing.
)

REM Clean up temp build_data dir
if exist "%ROOT_DIR%\cms-backend\build_data" (
    rmdir /s /q "%ROOT_DIR%\cms-backend\build_data"
)

echo     Static files collected into cms-backend\staticfiles\
echo.

REM ---------------------------------------------------------------
REM STEP 5 — Build .exe bundle with PyInstaller
REM ---------------------------------------------------------------
echo [5/6] Building standalone .exe with PyInstaller...
echo       (This may take 5-15 minutes)
echo.

cd /d "%ROOT_DIR%\cms-backend"
pyinstaller cms_backend.spec --clean --noconfirm

if errorlevel 1 (
    echo  ERROR: PyInstaller build failed.
    echo  Check the output above for details.
    cd /d "%ROOT_DIR%"
    pause & exit /b 1
)

cd /d "%ROOT_DIR%"
echo     PyInstaller build complete!
echo     Bundle located at: cms-backend\dist\CMS_Server\
echo.

REM ---------------------------------------------------------------
REM STEP 6 — Create Windows installer with Inno Setup
REM ---------------------------------------------------------------
if "%INNO_FOUND%"=="1" (
    echo [6/6] Creating Windows installer with Inno Setup...
    echo.

    mkdir "%ROOT_DIR%\Output" 2>nul

    "%INNO_PATH%" "%ROOT_DIR%\installer.iss"
    if errorlevel 1 (
        echo  ERROR: Inno Setup failed.
        echo  Check the output above for details.
        pause & exit /b 1
    )

    echo     Installer created!
    echo.
    echo =============================================================
    echo   BUILD COMPLETE
    echo   Installer: %ROOT_DIR%\Output\CMS_Setup.exe
    echo =============================================================
) else (
    echo [6/6] SKIPPED — Inno Setup not installed.
    echo.
    echo =============================================================
    echo   BUILD COMPLETE  ^(no installer^)
    echo   App bundle: %ROOT_DIR%\cms-backend\dist\CMS_Server\
    echo   Run it:     %ROOT_DIR%\cms-backend\dist\CMS_Server\CMS_Server.exe
    echo =============================================================
    echo.
    echo   To create a proper .exe installer, install Inno Setup 6 from:
    echo   https://jrsoftware.org/isinfo.php
    echo   Then re-run this script.
)

echo.
pause
