"""
CMS Application Launcher
========================
Entry point for the PyInstaller-bundled .exe
Starts the Django backend and opens a browser window.
"""

import sys
import os
import threading
import webbrowser
import time
import shutil


# ---------------------------------------------------------------------------
# Path helpers
# ---------------------------------------------------------------------------

def get_bundle_dir():
    """
    Returns the directory where PyInstaller extracted bundled files.
    In frozen mode this is sys._MEIPASS; in dev it is the script directory.
    """
    if hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS
    return os.path.abspath(os.path.dirname(__file__))


def get_app_dir():
    """
    Returns the directory where the .exe lives (writable).
    In dev mode, returns the script directory.
    """
    if hasattr(sys, 'frozen'):
        return os.path.dirname(sys.executable)
    return os.path.abspath(os.path.dirname(__file__))


# ---------------------------------------------------------------------------
# Data directory setup (writable files: db, media)
# ---------------------------------------------------------------------------

def setup_data_directory(app_dir, bundle_dir):
    """
    Creates <app_dir>/cms_data/ for writable runtime files.
    On first run, copies the initial SQLite database from the bundle.
    """
    data_dir = os.path.join(app_dir, 'cms_data')
    os.makedirs(data_dir, exist_ok=True)

    # Copy initial database on first run
    db_dest = os.path.join(data_dir, 'db.sqlite3')
    db_src  = os.path.join(bundle_dir, 'db.sqlite3')
    if not os.path.exists(db_dest):
        if os.path.exists(db_src):
            shutil.copy2(db_src, db_dest)
            print(f"[CMS] Initialized database at: {db_dest}")
        else:
            print("[CMS] No initial database found — a fresh one will be created.")

    # Ensure media directory exists
    os.makedirs(os.path.join(data_dir, 'media'), exist_ok=True)

    return data_dir


# ---------------------------------------------------------------------------
# Django environment setup
# ---------------------------------------------------------------------------

def setup_django_env(bundle_dir, data_dir):
    """Configures environment variables that settings_standalone.py reads."""

    # Make bundled Django apps importable
    if bundle_dir not in sys.path:
        sys.path.insert(0, bundle_dir)

    os.environ['DJANGO_SETTINGS_MODULE'] = 'backend.settings_standalone'

    # Defaults — can be overridden by a .env file placed next to the .exe
    os.environ.setdefault('ALLOWED_HOSTS',    'localhost,127.0.0.1')
    os.environ.setdefault('DEBUG',            'False')
    os.environ.setdefault(
        'DJANGO_SECRET_KEY',
        'cms-standalone-secret-key-change-me-in-production-abc123'
    )

    # Custom vars read by settings_standalone.py
    os.environ['CMS_DATA_DIR']   = data_dir
    os.environ['CMS_BUNDLE_DIR'] = bundle_dir


# ---------------------------------------------------------------------------
# Django startup tasks
# ---------------------------------------------------------------------------

def run_migrations():
    """Apply any pending database migrations silently."""
    from django.core.management import call_command
    print("[CMS] Applying database migrations...")
    try:
        call_command('migrate', '--run-syncdb', verbosity=0)
        print("[CMS] Migrations complete.")
    except Exception as exc:
        print(f"[CMS] Migration warning (non-fatal): {exc}")


# ---------------------------------------------------------------------------
# Browser launcher
# ---------------------------------------------------------------------------

def open_browser(url, delay=2.5):
    """Opens the default browser after a short delay."""
    def _open():
        time.sleep(delay)
        webbrowser.open(url)
    t = threading.Thread(target=_open, daemon=True)
    t.start()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print()
    print("=" * 55)
    print("  XpertAI CMS  —  Starting...")
    print("=" * 55)

    bundle_dir = get_bundle_dir()
    app_dir    = get_app_dir()

    print(f"[CMS] Bundle : {bundle_dir}")
    print(f"[CMS] App dir: {app_dir}")

    # 1. Setup writable data directory
    data_dir = setup_data_directory(app_dir, bundle_dir)
    print(f"[CMS] Data   : {data_dir}")

    # 2. Configure Django environment
    setup_django_env(bundle_dir, data_dir)

    # 3. Boot Django
    import django
    django.setup()

    # 4. Run migrations
    run_migrations()

    # 5. Schedule browser open
    url = 'http://127.0.0.1:8000'
    print(f"\n[CMS] Opening  {url}  in your browser...")
    open_browser(url, delay=2.5)

    # 6. Start production WSGI server (waitress — pure Python, Windows-friendly)
    from waitress import serve
    from backend.wsgi import application

    print(f"[CMS] Server running at {url}")
    print("[CMS] Admin panel: http://127.0.0.1:8000/admin/")
    print("[CMS] Press Ctrl+C to stop.\n")

    try:
        serve(application, host='127.0.0.1', port=8000, threads=6)
    except KeyboardInterrupt:
        print("\n[CMS] Server stopped. Goodbye!")


if __name__ == '__main__':
    main()
