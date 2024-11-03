"""
Django settings for furniture project.

Generated by 'django-admin startproject' using Django 4.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
import dj_database_url
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"


AUTH_USER_MODEL = "users.User"

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    "rest_framework_simplejwt.token_blacklist",
    'drf_spectacular',
    "debug_toolbar",
    "corsheaders",
    'users',
    'categories',
    'products',
    
]

INTERNAL_IPS = [
    "127.0.0.1",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = 'furniture.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Spectacular settings for api auto documentation
SPECTACULAR_SETTINGS = {
    "TITLE": "Furniture API",
    "DESCRIPTION": "This is swagger interactive API documentation for Furniture Project",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}


WSGI_APPLICATION = 'furniture.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": dj_database_url.config(
        default=os.getenv("POSTGRES_URL"),
        conn_max_age=600,
    )
}



# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": "amjad-furniture",
#         "USER": "postgres",
#         "PASSWORD": os.getenv("LOCALPASSWORD"),
#         "HOST": "localhost",
#         "PORT": "5432",
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",  # for api auto documentation
    "DEFAULT_RENDERER_CLASSES": [
        "renderers.CustomJSONRenderer",  # Custom JSON format for responses
        "rest_framework.renderers.BrowsableAPIRenderer",  # Optional, for the DRF web interface
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": ["custom.CustomJWTAuthentication"],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "1000/day",
        "user": "100000/day",
    },
}


SIMPLE_JWT = {
    # Token lifetimes
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "SLIDING_TOKEN_LIFETIME": timedelta(days=1),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=7),
    # Refresh token rotation and blacklisting
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    # Update last login field in User model on token refresh
    "UPDATE_LAST_LOGIN": False,
    # Security settings
    "ALGORITHM": "HS256",  # Consider RS256 for added security(asymmetric encryption)
    "SIGNING_KEY": os.getenv("SECRET_KEY"),
    "VERIFYING_KEY": None,  # Set if using asymmetric encryption
    "LEEWAY": 0,  # Adjust to allow for clock skew
    # Custom JWT claims
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",  # JWT ID claim for unique identification
    # Authentication settings
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    # Token classes
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    # Serializers
    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
    # Optional settings (use as needed)
    "AUDIENCE": None,  # Intended audience for the token
    "ISSUER": None,  # Token issuer
    "JSON_ENCODER": None,  # specify a custom JSON encoder class if your tokens need special encoding
    "JWK_URL": None,  # URL for JSON Web Key Set
}



# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_ROOT = str(BASE_DIR / "staticfiles")
# STATICFILES_DIRS = [str(BASE_DIR / "static")]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]
STATIC_URL = "/static/"

MEDIA_ROOT = str(BASE_DIR / "media")
MEDIA_URL = "/media/"


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = "users.User"

# Edit these values in production!
CORS_ALLOW_ALL_ORIGINS = True
ALLOWED_HOSTS = ["*"]
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = ['https://gym-backend-production-65cc.up.railway.app']