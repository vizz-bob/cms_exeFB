# cms_backend.spec
# ================
# PyInstaller specification for the XpertAI CMS standalone .exe
#
# Run from the cms-backend/ directory:
#   pyinstaller cms_backend.spec --clean --noconfirm
#
# Output:  cms-backend/dist/CMS_Server/CMS_Server.exe

import os
from PyInstaller.utils.hooks import (
    collect_all,
    collect_data_files,
    collect_submodules,
)

block_cipher = None

# ---------------------------------------------------------------------------
# Collect data + hidden-imports for third-party packages
# ---------------------------------------------------------------------------

_packages = [
    'django',
    'rest_framework',
    'jazzmin',
    'corsheaders',
    'whitenoise',
    'adminsortable2',
    'colorfield',
    'multiselectfield',
    'admin_tools',
    'admin_interface',
]

all_datas       = []
all_binaries    = []
all_hidden      = []

for _pkg in _packages:
    try:
        _d, _b, _h = collect_all(_pkg)
        all_datas    += _d
        all_binaries += _b
        all_hidden   += _h
    except Exception as _e:
        print(f"[spec] Warning: collect_all({_pkg!r}) — {_e}")

# Extra data-only packages
for _pkg in ['decouple', 'PIL', 'storages', 'boto3', 'botocore', 'waitress']:
    try:
        all_datas += collect_data_files(_pkg)
    except Exception as _e:
        print(f"[spec] Warning: collect_data_files({_pkg!r}) — {_e}")

# ---------------------------------------------------------------------------
# Django project apps
# ---------------------------------------------------------------------------

_project_root = '.'

_django_apps = [
    'core', 'blog', 'cms', 'contact', 'leads', 'theme',
    'pages', 'careers', 'stakeholders', 'homepage',
    'resources_page', 'lead_system_page', 'legal',
    'services_page', 'about', 'branding', 'backend',
]

for _app in _django_apps:
    _app_path = os.path.join(_project_root, _app)
    if not os.path.isdir(_app_path):
        continue

    # Collect submodules (views, models, serializers, etc.)
    try:
        all_hidden += collect_submodules(_app)
    except Exception:
        pass

    # Include all data directories inside the app
    for _subdir in ('templates', 'migrations', 'static', 'management', 'fixtures'):
        _p = os.path.join(_app_path, _subdir)
        if os.path.isdir(_p):
            all_datas.append((_p, f'{_app}/{_subdir}'))

# ---------------------------------------------------------------------------
# Project-level data files
# ---------------------------------------------------------------------------

_project_data = [
    # Destination                        Source path
    ('templates',                        'templates'),
    ('staticfiles',                      'staticfiles'),       # pre-collected static
    ('frontend_build',                   'frontend_build'),    # React production build
    ('db.sqlite3',                       '.'),                 # initial database
]

for _src, _dst in _project_data:
    _full = os.path.join(_project_root, _src)
    if os.path.exists(_full):
        all_datas.append((_full, _dst))
    else:
        print(f"[spec] Note: {_full!r} not found — will be skipped.")

# ---------------------------------------------------------------------------
# Additional hidden imports
# ---------------------------------------------------------------------------

_extra_hidden = [
    # Django internals
    'django.template.loaders.cached',
    'django.template.loaders.filesystem',
    'django.template.loaders.app_directories',
    'django.contrib.admin.apps',
    'django.contrib.admin.templatetags.admin_list',
    'django.contrib.admin.templatetags.admin_modify',
    'django.contrib.admin.templatetags.admin_urls',
    'django.contrib.admin.templatetags.base',
    'django.contrib.admin.templatetags.log',
    'django.contrib.staticfiles.finders',
    'django.contrib.staticfiles.storage',
    'django.db.backends.sqlite3',
    # third-party
    'whitenoise.middleware',
    'whitenoise.storage',
    'whitenoise.responders',
    'corsheaders.middleware',
    'corsheaders.signals',
    'rest_framework.authentication',
    'rest_framework.permissions',
    'rest_framework.response',
    'rest_framework.serializers',
    'rest_framework.viewsets',
    'rest_framework.routers',
    'rest_framework.authtoken',
    'rest_framework.authtoken.models',
    'adminsortable2.admin',
    'decouple',
    'PIL',
    'PIL._imaging',
    'PIL.Image',
    'waitress',
    'waitress.server',
    'waitress.task',
    'waitress.channel',
    # storages (disabled in standalone but must be importable)
    'storages.backends.s3boto3',
    'boto3',
    'botocore',
    'botocore.stub',
    'botocore.loaders',
]

all_hidden += _extra_hidden

# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------

a = Analysis(
    ['launcher.py'],
    pathex=[_project_root],
    binaries=all_binaries,
    datas=all_datas,
    hiddenimports=all_hidden,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # not needed — reduces bundle size
        'tkinter', 'matplotlib', 'numpy', 'scipy', 'pandas',
        'IPython', 'jupyter', 'notebook',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='CMS_Server',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,          # Keep console window so users can see status / errors
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,             # Replace with 'icon.ico' if you have one
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='CMS_Server',
)
