"""
CMS Application Launcher
========================
Entry point for the PyInstaller-bundled .exe
Starts the Django backend and opens a native app window via PyWebView.
"""

import sys
import os
import threading
import time
import shutil
import logging


# ---------------------------------------------------------------------------
# Path helpers
# ---------------------------------------------------------------------------

def get_bundle_dir():
    if hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS
    return os.path.abspath(os.path.dirname(__file__))


def get_app_dir():
    if hasattr(sys, 'frozen'):
        return os.path.dirname(sys.executable)
    return os.path.abspath(os.path.dirname(__file__))


# ---------------------------------------------------------------------------
# Data directory setup (writable files: db, media)
# ---------------------------------------------------------------------------

def setup_data_directory(app_dir, bundle_dir):
    data_dir = os.path.join(app_dir, 'cms_data')
    os.makedirs(data_dir, exist_ok=True)

    db_dest = os.path.join(data_dir, 'db.sqlite3')
    db_src  = os.path.join(bundle_dir, 'db.sqlite3')
    if not os.path.exists(db_dest):
        if os.path.exists(db_src):
            shutil.copy2(db_src, db_dest)

    os.makedirs(os.path.join(data_dir, 'media'), exist_ok=True)
    return data_dir


# ---------------------------------------------------------------------------
# Logging (writes to cms_data/cms.log since console is hidden)
# ---------------------------------------------------------------------------

def setup_logging(data_dir):
    os.makedirs(data_dir, exist_ok=True)
    log_file = os.path.join(data_dir, 'cms.log')
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout),
        ]
    )


# ---------------------------------------------------------------------------
# Django environment setup
# ---------------------------------------------------------------------------

def setup_django_env(bundle_dir, data_dir):
    if bundle_dir not in sys.path:
        sys.path.insert(0, bundle_dir)

    os.environ['DJANGO_SETTINGS_MODULE'] = 'backend.settings_standalone'
    os.environ.setdefault('ALLOWED_HOSTS',    'localhost,127.0.0.1')
    os.environ.setdefault('DEBUG',            'False')
    os.environ.setdefault(
        'DJANGO_SECRET_KEY',
        'cms-standalone-secret-key-change-me-in-production-abc123'
    )
    os.environ['CMS_DATA_DIR']   = data_dir
    os.environ['CMS_BUNDLE_DIR'] = bundle_dir


# ---------------------------------------------------------------------------
# Django startup tasks
# ---------------------------------------------------------------------------

def run_migrations():
    from django.core.management import call_command
    logging.info("Applying database migrations...")
    try:
        call_command('migrate', '--run-syncdb', verbosity=0)
        logging.info("Migrations complete.")
    except Exception as exc:
        logging.warning(f"Migration warning (non-fatal): {exc}")


def create_default_superuser():
    """Create a default admin superuser on first run if none exists."""
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@xpertai.com',
                password='admin123',
            )
            logging.info("=" * 50)
            logging.info("  Default admin account created:")
            logging.info("    Username : admin")
            logging.info("    Password : admin123")
            logging.info("  Please change your password after first login!")
            logging.info("  Admin URL: http://127.0.0.1:8000/admin/")
            logging.info("=" * 50)
        else:
            logging.info("Superuser already exists — skipping creation.")
    except Exception as exc:
        logging.warning(f"Could not create default superuser: {exc}")


# ---------------------------------------------------------------------------
# Waitress server (runs in background thread)
# ---------------------------------------------------------------------------

def start_server():
    from waitress import serve
    from backend.wsgi import application
    logging.info("Starting Waitress server on http://127.0.0.1:8000 ...")
    serve(application, host='127.0.0.1', port=8000, threads=6)


def wait_for_server(url='http://127.0.0.1:8000', timeout=30):
    """Poll until Django is accepting connections."""
    import urllib.request
    import urllib.error
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            urllib.request.urlopen(url, timeout=1)
            return True
        except Exception:
            time.sleep(0.3)
    return False


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    bundle_dir = get_bundle_dir()
    app_dir    = get_app_dir()
    data_dir   = setup_data_directory(app_dir, bundle_dir)

    setup_logging(data_dir)
    logging.info("=" * 50)
    logging.info("  XpertAI CMS  —  Starting...")
    logging.info("=" * 50)
    logging.info(f"Bundle : {bundle_dir}")
    logging.info(f"App dir: {app_dir}")
    logging.info(f"Data   : {data_dir}")

    # 1. Configure Django
    setup_django_env(bundle_dir, data_dir)

    # 2. Boot Django
    import django
    django.setup()

    # 3. Run migrations
    run_migrations()

    # 3b. Create default superuser on first run
    create_default_superuser()

    # 4. Start Waitress in a background daemon thread
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    # 5. Wait until the server is actually ready
    logging.info("Waiting for server to be ready...")
    ready = wait_for_server('http://127.0.0.1:8000', timeout=30)
    if not ready:
        logging.error("Server did not start in time — exiting.")
        sys.exit(1)
    logging.info("Server ready.")

    # 6. Open native app window with PyWebView
    try:
        import webview

        window = webview.create_window(
            title='XpertAI CMS',
            url='http://127.0.0.1:8000/admin/',
            width=1366,
            height=820,
            resizable=True,
            min_size=(900, 600),
            text_select=True,
            confirm_close=False,
        )

        logging.info("Opening app window...")
        # gui='edgechromium' uses built-in WebView2 (Windows 10/11)
        webview.start(gui='edgechromium', debug=False)

    except Exception as e:
        # Fallback: open in default browser if webview fails
        logging.warning(f"PyWebView failed ({e}), falling back to browser.")
        import webbrowser
        webbrowser.open('http://127.0.0.1:8000/admin/')
        # Keep server alive until user kills the process
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass

    logging.info("App window closed. Goodbye!")


if __name__ == '__main__':
    main()
