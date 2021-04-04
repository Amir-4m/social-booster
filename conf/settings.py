"""
Django settings for socialboost project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
from datetime import timedelta
from pathlib import Path
import os
# load the environment variable handler library
from decouple import config, Csv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)
DEVEL = config('DEVEL', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost', cast=Csv())
# This is used so that application data can hook into specific sites.
SITE_ID = 1

# Application definition
INSTALLED_APPS = [
    'apps.contents',
    'apps.accounts',
    'apps.packages',
    'apps.payments',

    'drf_yasg',
    'tinymce',
    'rest_framework',
    'django_json_widget',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'conf.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

ASGI_APPLICATION = "conf.asgi.application"
WSGI_APPLICATION = 'conf.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE'),
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASS'),
        'HOST': config('DB_HOST', default=""),
        'PORT': config('DB_PORT', default=""),
    },
}

AUTH_USER_MODEL = 'accounts.User'
AUTHENTICATION_BACKENDS = (
    'apps.accounts.backends.SMSBackend',
    'django.contrib.auth.backends.ModelBackend',
)
# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators
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
# https://docs.djangoproject.com/en/3.1/topics/i18n/
LANGUAGE_CODE = 'fa-ir'
TIME_ZONE = 'Asia/Tehran'
USE_I18N = False
USE_L10N = False
USE_TZ = False

# cache settings for Django
CACHE_KEY_PREFIX = config('CACHE_PREFIX', default='SOCIAL_BOOST')
# CACHES = {
#     'default': {
#         'BACKEND': config('CACHE_BACKEND'),
#         'LOCATION': config('CACHE_LOCATION'),
#         'KEY_PREFIX': CACHE_KEY_PREFIX,
#         'TIMEOUT': None,
#     }
# }

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = config('MEDIA_URL', default='/media/')

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'EXCEPTION_HANDLER': 'utils.exception_handlers.custom_exception_handler',
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    # 'PAGE_SIZE': 20,
    'DEFAULT_THROTTLE_RATES': {
        'register': '2/minute',
        'obtain-token': '2/minute',
        'free_register': '5/hour',
        'forgot-password': '1/minute',
    },
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=config('ACCESS_TOKEN_LIFETIME', default=120, cast=int)),
    'REFRESH_TOKEN_LIFETIME': timedelta(minutes=config('REFRESH_TOKEN_LIFETIME', default=3600, cast=int)),
    'ROTATE_REFRESH_TOKENS': True,
}

PAYMENT_API_URL = config('PAYMENT_API_URL', default='')
PAYMENT_SERVICE_SECRET = config('PAYMENT_SERVICE_SECRET', default='')
CAFE_BAZAAR_PACKAGE_NAME = config('CAFE_BAZAAR_PACKAGE_NAME')

SMS_GATE_WAY_URL = config('SMS_GATE_WAY_URL', default='')
SMS_GATE_WAY_TOKEN = config('SMS_GATE_WAY_TOKEN', default='')
VERIFY_CODE_MIN = config('VERIFY_CODE_MIN', cast=int, default=10000)
VERIFY_CODE_MAX = config('VERIFY_CODE_MAX', cast=int, default=99999)

