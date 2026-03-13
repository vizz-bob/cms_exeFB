from pathlib import Path
import os
from decouple import config
import datetime

BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------------
# CORE SETTINGS
# -----------------------------

# 1. SECRET KEY
SECRET_KEY = config("DJANGO_SECRET_KEY", default="django-insecure-12345")

# 2. DEBUG
DEBUG = config("DEBUG", default=False, cast=bool)

# 3. HELPER FUNCTION
def parse_env_list(env_var_name, default=""):
    raw_val = config(env_var_name, default=default)
    return [x.strip() for x in raw_val.split(',') if x.strip()]

# 4. ALLOWED HOSTS
ALLOWED_HOSTS = parse_env_list("ALLOWED_HOSTS", default="localhost,127.0.0.1")

# 5. INSTALLED APPS
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

# -----------------------------
# MIDDLEWARE
# -----------------------------
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "backend.middleware.AutomaticThemeMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

ROOT_URLCONF = "backend.urls"

# -----------------------------
# TEMPLATES
# -----------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "backend.context_processors.user_avatar_context", 
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"

# -----------------------------
# DATABASE
# -----------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# -----------------------------
# PASSWORD VALIDATION
# -----------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# -----------------------------
# INTERNATIONALIZATION
# -----------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC" 
USE_I18N = True
USE_TZ = True

# -----------------------------
# STATIC & MEDIA FILES
# -----------------------------
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles") 
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID", default=None)
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY", default=None)
AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME", default=None)

if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY and AWS_STORAGE_BUCKET_NAME:
    AWS_S3_REGION_NAME = config("AWS_S3_REGION_NAME", default="us-east-1")
    AWS_S3_SIGNATURE_VERSION = 's3v4'
    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = None
    AWS_S3_VERIFY = True
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/'
else:
    MEDIA_URL = "/media/"
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# -----------------------------
# EMAIL CONFIGURATION (SMTP)
# -----------------------------
# Switch backend to SMTP to send real emails
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default=EMAIL_HOST_USER)

# -----------------------------
# REST FRAMEWORK
# -----------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ]
}

# -----------------------------
# CORS & CSRF
# -----------------------------
CORS_ALLOWED_ORIGINS = parse_env_list("CORS_ALLOWED_ORIGINS")
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = parse_env_list("CSRF_TRUSTED_ORIGINS")

print(f"DEBUG: ALLOWED_HOSTS loaded: {ALLOWED_HOSTS}")
print(f"DEBUG: CORS_ORIGINS loaded: {CORS_ALLOWED_ORIGINS}")
if AWS_STORAGE_BUCKET_NAME:
    print(f"DEBUG: Using AWS S3 Bucket: {AWS_STORAGE_BUCKET_NAME}")
else:
    print("DEBUG: Using Local Media Storage")

# -----------------------------
# DEFAULT PRIMARY KEY
# -----------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# -----------------------------
# DYNAMIC THEME & JAZZMIN
# -----------------------------
IST_OFFSET = datetime.timedelta(hours=5, minutes=30)
now_utc = datetime.datetime.utcnow()
now_ist = now_utc + IST_OFFSET
is_daytime = 6 <= now_ist.hour < 18

if is_daytime:
    DYNAMIC_THEME_TWEAKS = {
        "theme": "lux", "dark_mode_theme": None, "brand_colour": "navbar-light", 
        "navbar": "navbar-white", "sidebar": "sidebar-light-primary", "accent": "accent-info",
    }
else:
    DYNAMIC_THEME_TWEAKS = {
        "theme": "darkly", "dark_mode_theme": None, "brand_colour": "navbar-dark", 
        "navbar": "navbar-dark", "sidebar": "sidebar-dark-indigo", "accent": "accent-warning",
    }

JAZZMIN_SETTINGS = {
    "site_title": "XpertAI Admin",
    "site_header": "XpertAI Global",
    "site_brand": "XpertAI CMS",
    "welcome_sign": "Welcome to XpertAI Global Headquarters",
    "copyright": "XpertAI Global Ltd",
    "search_model": ["auth.User", "cms.Service"],
    "topmenu_links": [
        {"name": "Home",  "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "View Website", "url": " ", "new_window": True}, 
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "cms.HomeContent": "fas fa-home",
        "cms.AboutContent": "fas fa-info-circle",
        "cms.ServicesContent": "fas fa-briefcase",
        "cms.ContactContent": "fas fa-envelope",
        "cms.CareersContent": "fas fa-user-tie",
        "cms.ResourcesContent": "fas fa-book",
        "cms.Page": "fas fa-file-alt",
        "cms.Service": "fas fa-cogs",
        "cms.CaseStudy": "fas fa-chart-line",
        "cms.Resource": "fas fa-download",
        "careers.JobOpening": "fas fa-briefcase",
        "careers.JobApplication": "fas fa-file-signature",
        "leads.Lead": "fas fa-bullhorn",
        "leads.WebsiteLead": "fas fa-globe",
        "leads.ChatbotLead": "fas fa-robot",
        "contact.ContactMessage": "fas fa-paper-plane",
        "blog.BlogPost": "fas fa-newspaper",
        "homepage.HeroSection": "fas fa-image",
        "homepage.Stat": "fas fa-chart-bar",
        "homepage.Feature": "fas fa-star",
        "homepage.BottomCTA": "fas fa-bullhorn",
        "resources_page.ResourcesHero": "fas fa-image",
        "resources_page.SectionTitles": "fas fa-heading",
        "resources_page.CaseStudy": "fas fa-book-open",
        "resources_page.DownloadableResource": "fas fa-file-download",
        "lead_system_page.LSHero": "fas fa-image",
        "lead_system_page.LSFeature": "fas fa-list",
        "lead_system_page.LSDashboard": "fas fa-tachometer-alt",
        "lead_system_page.LSBottomCTA": "fas fa-bullhorn",
        "services_page.ServiceHero": "fas fa-image",
        "services_page.ServiceCTA": "fas fa-bullhorn",
        "stakeholders.Stakeholder": "fas fa-users",
        "legal.LegalPage": "fas fa-balance-scale",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": True,
    "use_google_fonts_cdn": True,
    "show_ui_builder": True,
    "user_avatar": "user_avatar", 
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": True,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    },
    **DYNAMIC_THEME_TWEAKS
}
# CI/CD test v2 - backend change visible
