from pathlib import Path
from dotenv import load_dotenv
import os
from datetime import timedelta

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #external package
    'rest_framework',
    'mptt',
    'drf_spectacular',
    'rest_framework_simplejwt',
    'drf_yasg',
    #internal package
    'BEComputerVision.product',
    'BEComputerVision.users',
    'BEComputerVision.roles',
    'BEComputerVision.projects',
    'BEComputerVision.images',
    'BEComputerVision.annotations',
    'BEComputerVision.dataset',
    'BEComputerVision.versions',
]

CORS_ALLOW_CREDENTIALS = True # to accept cookies via ajax request
CORS_ORIGIN_WHITELIST = [
    '*' # the domain for front-end app(you can add more than 1) 
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'BEComputerVision.settings.middleware.custom_middleware.JWTAuthenticationMiddleware'
]

ROOT_URLCONF = 'BEComputerVision.urls'

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

WSGI_APPLICATION = 'BEComputerVision.wsgi.application'

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

TIME_ZONE = 'Asia/Ho_Chi_Minh'  # Thiết lập múi giờ Việt Nam
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=500),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

# SIMPLE_JWT = {
#     'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
#     'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
#     'SLIDING_TOKEN_LIFETIME': timedelta(days=30),
#     'SLIDING_TOKEN_REFRESH_LIFETIME_LATE_USER': timedelta(days=1),
#     'SLIDING_TOKEN_LIFETIME_LATE_USER': timedelta(days=30),
# }

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'BEComputerVision.users.authentication.SafeJWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),

    # 'DEFAULT_AUTHENTICATION_CLASSES': [
    #     'rest_framework_simplejwt.authentication.JWTAuthentication',
    # ],
}

SPECTACULAR_SETTINGS = {
    "TITLE": "DJANGO DRF ComputerVision"
} 

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587  # hoặc 465 nếu cần SSL
EMAIL_USE_TLS = False  # hoặc False nếu không cần TLS
EMAIL_HOST_USER = os.environ.get("EMAIL")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_PASSWORD")