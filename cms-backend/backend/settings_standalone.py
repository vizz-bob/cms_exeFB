"""
settings_standalone.py
======================
Django settings for the PyInstaller-bundled standalone .exe.

Two modes:
  BUILD mode  (CMS_BUILD_MODE=true)  — used by build_installer.bat when
              running collectstatic; reads source dirs.
  RUNTIME mode (default)             — used by launcher.py; reads bundled
              static files from _MEIPASS.
"""

import os
import sys
import datetime
from pathlib import Path


# ---------------------------------------------------------------------------
# Resolve key directories
# ---------------------------------------------------------------------------

# Where bundled (read-only) files live:
#   - BUILD   mode: the cms-backend source directory
#   - RUNTIME mode: PyInstaller's _MEIPASS temp directory
BUNDLE_DIR = os.environ.get(
    'CMS_BUNDLE_DIR',
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

# Where writable runtime files live (db.sqlite3, media/, etc.)
#   - BUILD   mode: cms-backend/build_data/
#   - RUNTIME mode: <next to exe>/cms_data/
DATA_DIR = os.environ.get(
    'CMS_DATA_DIR',
    os.path.join(
        os.path.dirname(sys.executable) if hasattr(sys, 'frozen')
        else os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'cms_data'
    )
)

IS_BUILD_MODE = os.environ.get('CMS_BUILD_MODE', 'false').lower() == 'true'

BASE_DIR = Path(BUNDLE_DIR)
DATA_PATH = Path(DATA_DIR)


# ---------------------------------------------------------------------------
# Core
# ---------------------------------------------------------------------------

SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'cms-standalone-insecure-key-change-me-abc123xyz'
)

DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

_raw_hosts = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1')
ALLOWED_HOSTS = [h.strip() for h in _raw_hosts.split(',') if h.strip()]


# ---------------------------------------------------------------------------
# Application definition
# ---------------------------------------------------------------------------

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # third-party
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'adminsortable2',
    # custom apps
    'core',
    'blog',
    'cms',
    'contact',
    'leads',
    'theme',
    'pages',
    'careers',
    'stakeholders',
    'homepage',
    'resources_page',
    'lead_system_page',
    'legal',
    'services_page',
    'about.apps.AboutConfig',
    'branding',
    'storages',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'backend.middleware.AutomaticThemeMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

ROOT_URLCONF = 'backend.urls_standalone'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BUNDLE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'backend.context_processors.user_avatar_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'


# ---------------------------------------------------------------------------
# Database  (writable location — next to .exe)
# ---------------------------------------------------------------------------

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DATA_PATH / 'db.sqlite3',
    }
}


# ---------------------------------------------------------------------------
# Password validation
# ---------------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ---------------------------------------------------------------------------
# Internationalisation
# ---------------------------------------------------------------------------

LANGUAGE_CODE = 'en-us'
TIME_ZONE     = 'UTC'
USE_I18N      = True
USE_TZ        = True


# ---------------------------------------------------------------------------
# Static & media files
# ---------------------------------------------------------------------------

STATIC_URL = '/static/'

if IS_BUILD_MODE:
    # BUILD: collectstatic writes into cms-backend/staticfiles/
    STATIC_ROOT = os.path.join(BUNDLE_DIR, 'staticfiles')
    _staticfiles_dirs = []
    # Include React build static assets as a source
    _react_static = os.path.join(BUNDLE_DIR, 'frontend_build', 'static')
    if os.path.exists(_react_static):
        _staticfiles_dirs.append(_react_static)
    # Include project-level static dir if it exists
    _project_static = os.path.join(BUNDLE_DIR, 'static')
    if os.path.exists(_project_static):
        _staticfiles_dirs.append(_project_static)
    STATICFILES_DIRS = _staticfiles_dirs
else:
    # RUNTIME: serve from the bundled staticfiles/ (read-only, _MEIPASS)
    STATIC_ROOT      = os.path.join(BUNDLE_DIR, 'staticfiles')
    STATICFILES_DIRS = []

STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

MEDIA_URL  = '/media/'
MEDIA_ROOT = os.path.join(DATA_DIR, 'media')


# ---------------------------------------------------------------------------
# Email  (console backend for standalone — no SMTP config needed)
# ---------------------------------------------------------------------------

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# ---------------------------------------------------------------------------
# REST Framework
# ---------------------------------------------------------------------------

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
}


# ---------------------------------------------------------------------------
# CORS / CSRF  (same-origin in standalone, but keep headers for safety)
# ---------------------------------------------------------------------------

CORS_ALLOW_ALL_ORIGINS  = True
CORS_ALLOW_CREDENTIALS  = True
CSRF_TRUSTED_ORIGINS    = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]


# ---------------------------------------------------------------------------
# AWS storage  (disabled in standalone mode)
# ---------------------------------------------------------------------------

AWS_ACCESS_KEY_ID       = None
AWS_SECRET_ACCESS_KEY   = None
AWS_STORAGE_BUCKET_NAME = None


# ---------------------------------------------------------------------------
# Default PK
# ---------------------------------------------------------------------------

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ---------------------------------------------------------------------------
# Dynamic Jazzmin theme (day / night)
# ---------------------------------------------------------------------------

IST_OFFSET = datetime.timedelta(hours=5, minutes=30)
now_ist    = datetime.datetime.utcnow() + IST_OFFSET
is_daytime = 6 <= now_ist.hour < 18

if is_daytime:
    DYNAMIC_THEME_TWEAKS = {
        'theme': 'lux', 'dark_mode_theme': None,
        'brand_colour': 'navbar-light', 'navbar': 'navbar-white',
        'sidebar': 'sidebar-light-primary', 'accent': 'accent-info',
    }
else:
    DYNAMIC_THEME_TWEAKS = {
        'theme': 'darkly', 'dark_mode_theme': None,
        'brand_colour': 'navbar-dark', 'navbar': 'navbar-dark',
        'sidebar': 'sidebar-dark-indigo', 'accent': 'accent-warning',
    }

JAZZMIN_SETTINGS = {
    'site_title':   'XpertAI Admin',
    'site_header':  'XpertAI Global',
    'site_brand':   'XpertAI CMS',
    'welcome_sign': 'Welcome to XpertAI Global Headquarters',
    'copyright':    'XpertAI Global Ltd',
    'search_model': ['auth.User', 'cms.Service'],
    'topmenu_links': [
        {'name': 'Home',         'url': 'admin:index',           'permissions': ['auth.view_user']},
        {'name': 'View Website', 'url': 'http://127.0.0.1:8000', 'new_window': True},
    ],
    'show_sidebar':         True,
    'navigation_expanded':  True,
    'hide_apps':            [],
    'hide_models':          [],
    'icons': {
        'auth':           'fas fa-users-cog',
        'auth.user':      'fas fa-user',
        'auth.Group':     'fas fa-users',
        'cms.Service':    'fas fa-cogs',
        'blog.BlogPost':  'fas fa-newspaper',
        'leads.Lead':     'fas fa-bullhorn',
        'careers.JobOpening': 'fas fa-briefcase',
        'contact.ContactMessage': 'fas fa-paper-plane',
    },
    'default_icon_parents': 'fas fa-chevron-circle-right',
    'default_icon_children': 'fas fa-circle',
    'related_modal_active': True,
    'use_google_fonts_cdn': True,
    'show_ui_builder':      True,
    'user_avatar':          'user_avatar',
}

JAZZMIN_UI_TWEAKS = {
    'navbar_small_text':           False,
    'footer_small_text':           False,
    'body_small_text':             False,
    'brand_small_text':            False,
    'no_navbar_border':            False,
    'navbar_fixed':                True,
    'layout_boxed':                False,
    'footer_fixed':                False,
    'sidebar_fixed':               True,
    'sidebar_nav_small_text':      False,
    'sidebar_disable_expand':      False,
    'sidebar_nav_child_indent':    False,
    'sidebar_nav_compact_style':   False,
    'sidebar_nav_legacy_style':    False,
    'sidebar_nav_flat_style':      True,
    'button_classes': {
        'primary':   'btn-primary',
        'secondary': 'btn-secondary',
        'info':      'btn-info',
        'warning':   'btn-warning',
        'danger':    'btn-danger',
        'success':   'btn-success',
    },
    **DYNAMIC_THEME_TWEAKS,
}
