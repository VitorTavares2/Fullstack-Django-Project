from pathlib import Path
import os
import environ
import cloudinary
import cloudinary.uploader
import cloudinary.api

# ======================
# BASE & ENV
# ======================

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

DEBUG = env.bool("DEBUG", default=False)
print("DEBUG LIDO:", DEBUG)

SITE_ID = int(os.getenv("SITE_ID", 1))


# ======================
# EMAIL (via MailTrap SMTP)
# ======================

EMAIL_BACKEND = env("EMAIL_BACKEND")
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = env.int("EMAIL_PORT")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# ======================
# CLOUDINARY (.env)
# ======================

cloudinary.config(
    cloud_name=env("CLOUD_NAME"),
    api_key=env("CLOUD_API_KEY"),
    api_secret=env("CLOUD_API_SECRET"),
    secure=True
)

DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

# ======================
# SECURITY
# ======================

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "django-insecure-b73v%o)j=m=bu^^7rggu#je1jzgzio=u%)r94jfh-a%^j5q0h_"
)

ALLOWED_HOSTS = [
    "fullstack-django-project-production.up.railway.app",
    "localhost",
    "127.0.0.1",
]

CSRF_TRUSTED_ORIGINS = [
    "https://fullstack-django-project-production.up.railway.app",
]

# ======================
# APPLICATIONS
# ======================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "django.contrib.sites",

    # Allauth
    "allauth",
    "allauth.account",
    "allauth.socialaccount",

    # Cloudinary
    "cloudinary_storage",
    "cloudinary",

    # Apps
    "stellaric",
    "users",
    "cart",
]

SITE_ID = 1

ACCOUNT_FORMS = {
    "login": "allauth.account.forms.LoginForm",
    "signup": "users.forms.CustomSignupForm",
}

# ======================
# MIDDLEWARE
# ======================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    "allauth.account.middleware.AccountMiddleware",
]

# ======================
# URLS / WSGI
# ======================

ROOT_URLCONF = "djangoProject.urls"
WSGI_APPLICATION = "djangoProject.wsgi.application"

# ======================
# TEMPLATES
# ======================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ======================
# AUTHENTICATION
# ======================

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
ACCOUNT_PREVENT_NUMERATION = False
LOGIN_REDIRECT_URL = "/"
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = False
ACCOUNT_SESSION_REMEMBER = True

LOGIN_URL = "account_login"
LOGIN_REDIRECT_URL = "/"
ACCOUNT_LOGOUT_REDIRECT_URL = "/"

# ======================
# DATABASE
# ======================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ======================
# PASSWORD VALIDATION
# ======================

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ======================
# INTERNATIONALIZATION
# ======================

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ======================
# STATIC FILES
# ======================

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "assets",
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ======================
# MEDIA
# ======================

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
