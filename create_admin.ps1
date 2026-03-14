# create_admin.ps1 - Creates a Django superuser directly in the CMS SQLite database
# Run from PowerShell: .\create_admin.ps1
# Default login: admin / admin123

$dbPath = "$env:LOCALAPPDATA\XpertAI CMS\cms_data\db.sqlite3"

if (-not (Test-Path $dbPath)) {
    Write-Host "ERROR: Database not found at: $dbPath" -ForegroundColor Red
    Write-Host "Make sure you have launched the CMS app at least once first." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Found database: $dbPath" -ForegroundColor Green

# Download sqlite3.exe if not present
$sqlitePath = "$env:TEMP\sqlite3.exe"
if (-not (Test-Path $sqlitePath)) {
    Write-Host "Downloading sqlite3 tool..." -ForegroundColor Cyan
    try {
        $url = "https://www.sqlite.org/2024/sqlite-tools-win-x64-3460100.zip"
        $zipPath = "$env:TEMP\sqlite_tools.zip"
        Invoke-WebRequest -Uri $url -OutFile $zipPath -UseBasicParsing
        Expand-Archive -Path $zipPath -DestinationPath "$env:TEMP\sqlite_tools" -Force
        Copy-Item "$env:TEMP\sqlite_tools\sqlite3.exe" $sqlitePath -Force
        Write-Host "sqlite3 downloaded." -ForegroundColor Green
    } catch {
        Write-Host "Could not download sqlite3. Trying alternate method..." -ForegroundColor Yellow
        # Try using Python if available
        $pythonCmd = Get-Command python -ErrorAction SilentlyContinue
        if (-not $pythonCmd) { $pythonCmd = Get-Command python3 -ErrorAction SilentlyContinue }
        if ($pythonCmd) {
            Write-Host "Using Python to create superuser..." -ForegroundColor Cyan
            $pyScript = @"
import sys, os
sys.path.insert(0, r'$env:LOCALAPPDATA\XpertAI CMS\_internal')
os.environ['DJANGO_SETTINGS_MODULE'] = 'backend.settings_standalone'
os.environ['CMS_DATA_DIR'] = r'$env:LOCALAPPDATA\XpertAI CMS\cms_data'
os.environ['CMS_BUNDLE_DIR'] = r'$env:LOCALAPPDATA\XpertAI CMS\_internal'
os.environ['DJANGO_SECRET_KEY'] = 'cms-standalone-secret-key-change-me-in-production-abc123'
try:
    import django; django.setup()
    from django.contrib.auth import get_user_model
    User = get_user_model()
    if User.objects.filter(username='admin').exists():
        print('User admin already exists.')
    else:
        User.objects.create_superuser('admin', 'admin@xpertai.com', 'admin123')
        print('Superuser created: admin / admin123')
except Exception as e:
    print(f'Error: {e}')
"@
            & $pythonCmd.Source -c $pyScript
            Write-Host ""
            Write-Host "Done! Open http://127.0.0.1:8000/admin/ and log in with admin / admin123" -ForegroundColor Green
            Read-Host "Press Enter to exit"
            exit 0
        }
        Write-Host "ERROR: Cannot create superuser. Please push the code update from Mac and rebuild." -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

# Django PBKDF2-SHA256 hash for password 'admin123'
$passwordHash = "pbkdf2_sha256`$720000`$makeadmin1234salt`$cgR5C0RYWNK7vxCPMNnvlCIbxJ73IubtiSBLfLHSMqY="
$dateJoined = (Get-Date).ToUniversalTime().ToString("yyyy-MM-dd HH:mm:ss.ffffff")

$sqlCommands = @"
INSERT OR IGNORE INTO auth_user (
    password, last_login, is_superuser, username,
    first_name, last_name, email, is_staff, is_active, date_joined
) VALUES (
    '$passwordHash',
    NULL,
    1,
    'admin',
    'Admin',
    '',
    'admin@xpertai.com',
    1,
    1,
    '$dateJoined'
);
SELECT 'Result: ' || CASE WHEN changes() > 0 THEN 'Admin user created!' ELSE 'User already exists (not changed).' END;
SELECT 'Username: admin', 'Password: admin123';
"@

# Write SQL to temp file
$sqlFile = "$env:TEMP\create_admin.sql"
$sqlCommands | Out-File -FilePath $sqlFile -Encoding UTF8 -NoNewline

# Run sqlite3
Write-Host ""
Write-Host "Creating admin superuser..." -ForegroundColor Cyan
& $sqlitePath $dbPath ".read $sqlFile"

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "  Admin user ready!" -ForegroundColor Green
Write-Host "  URL     : http://127.0.0.1:8000/admin/" -ForegroundColor White
Write-Host "  Username: admin" -ForegroundColor White
Write-Host "  Password: admin123" -ForegroundColor White
Write-Host "  (Change your password after first login)" -ForegroundColor Yellow
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Read-Host "Press Enter to exit"
