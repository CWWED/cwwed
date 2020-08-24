"""
Django settings for cwwed project.

Generated by 'django-admin startproject' using Django 2.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import sys
import dj_database_url
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# sentry/logging configuration
sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN', ''),
    integrations=[DjangoIntegration()],
    send_default_pii=True,
)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'ssshhh...')

# deploy stages
DEPLOY_STAGE_LOCAL = 'local'
DEPLOY_STAGE_ALPHA = 'alpha'
DEPLOY_STAGE_DEV = 'dev'
DEPLOY_STAGE_TEST = 'test'
DEPLOY_STAGE_PROD = 'prod'
DEPLOY_STAGES = [DEPLOY_STAGE_LOCAL, DEPLOY_STAGE_ALPHA, DEPLOY_STAGE_DEV, DEPLOY_STAGE_TEST, DEPLOY_STAGE_PROD]
DEPLOY_STAGE = os.environ.get('DEPLOY_STAGE', DEPLOY_STAGE_LOCAL)
assert DEPLOY_STAGE in DEPLOY_STAGES, 'unknown DEPLOY_STAGE "{}"'.format(DEPLOY_STAGE)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if DEPLOY_STAGE == DEPLOY_STAGE_LOCAL else False


# TODO
# https://docs.djangoproject.com/en/2.0/topics/security/#host-headers-virtual-hosting
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'named_storms.apps.NamedStormsConfig',  # specify AppConfig to include custom signals
    'coastal_act',
    'audit',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',  # for drf
    'corsheaders',  # for drf
    'revproxy',  # django-revproxy
    'storages',  # django-storages
    'allauth',
    'allauth.account',
    # TODO - setup social accounts?
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'crispy_forms',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cwwed.urls'

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

FILE_UPLOAD_HANDLERS = [
    # stream directly to temporary disk space
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
]

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

WSGI_APPLICATION = 'cwwed.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    # https://github.com/kennethreitz/dj-database-url
    'default': dj_database_url.config(default='postgis://postgres@localhost:5432/postgres', conn_max_age=300),
}

# https://docs.djangoproject.com/en/2.0/topics/cache/
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': '{}:6379'.format(os.environ.get('CELERY_BROKER', 'localhost')),
    },
    'psa_geojson': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache_psa_geojson',
        'TIMEOUT': None,  # never expire, but this only applies to low level cache operations whereas cache_page() requires a timeout
        'OPTIONS': {
            'MAX_ENTRIES': 5000,
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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


# allauth
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'  # username or email
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 60

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


LOGIN_REDIRECT_URL = 'home'

# https://django-crispy-forms.readthedocs.io/en/latest/index.html
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

# WhiteNoise
# http://whitenoise.evans.io/en/stable/django.html
STATIC_URL = "/static/"
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    os.path.join(BASE_DIR, "frontend/dist"),  # npm assets output directory
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATIC_ANGULAR_ASSETS_URL = "{}cwwed/".format(STATIC_URL)

# custom file storage
DEFAULT_FILE_STORAGE = 'cwwed.storage_backends.S3ObjectStorage'
AWS_ARCHIVE_BUCKET_NAME = 'cwwed-archives'
AWS_S3_ARCHIVE_DOMAIN = '%s.s3.amazonaws.com' % AWS_ARCHIVE_BUCKET_NAME
AWS_DEFAULT_ACL = None

MEDIA_URL = '/media/'
MEDIA_ROOT = '/media/bucket/cwwed'


# Logging
# https://docs.djangoproject.com/en/2.0/topics/logging/
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s  %(asctime)s  %(module)s '
                      '%(process)d  %(thread)d  %(message)s'
        },
    },
    'loggers': {
        '': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': True,
        },
        'cwwed': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': False,
        },
        'django': {
            'level': 'WARNING',
            'handlers': ['console'],
            'propagate': True,
        },
    },
}

SITE_ID = 1

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100,
}

# django-cors-headers
# https://github.com/ottoyiu/django-cors-headers/
CORS_URLS_REGEX = r'^/api/.*$'
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_METHODS = (
    'GET',
    'OPTIONS',
)

# email via sendgrid
# https://docs.djangoproject.com/en/2.0/topics/email/
# https://app.sendgrid.com/guide/integrate/langs/smtp
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
# don't send emails if DEBUG is enabled, instead just print the email to the console
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' if DEBUG else 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@cwwed-staging.com'

#
# CWWED
#

CWWED_HOST = os.environ.get('CWWED_HOST', '127.0.0.1')
CWWED_SCHEME = 'http' if DEPLOY_STAGE == DEPLOY_STAGE_LOCAL else 'https'
CWWED_PORT = 8000 if DEPLOY_STAGE == DEPLOY_STAGE_LOCAL else 443

CWWED_ARCHIVE_EXTENSION = 'tgz'
CWWED_DATA_DIR = MEDIA_ROOT
CWWED_OPENDAP_DIR = 'OPENDAP'

CWWED_COVERED_DATA_DIR_NAME = 'Covered Data'
CWWED_COVERED_DATA_CURRENT_DIR_NAME = '.covered-data-current'
CWWED_COVERED_DATA_SNAPSHOTS_DIR_NAME = 'Covered Data Snapshots'
CWWED_COVERED_ARCHIVE_DIR_NAME = 'Covered Data Archive'
CWWED_COVERED_DATA_INCOMPLETE_DIR_NAME = '.incomplete'

CWWED_NSEM_DIR_NAME = 'NSEM'
CWWED_NSEM_UPLOAD_DIR_NAME = 'upload'
CWWED_NSEM_ARCHIVE_WRITE_MODE = 'w:gz'
CWWED_NSEM_ARCHIVE_READ_MODE = 'r:gz'
CWWED_NSEM_USER = 'nsem'
CWWED_NSEM_PASSWORD = os.environ.get('CWWED_NSEM_PASSWORD')
CWWED_NSEM_TMP_USER_EXPORT_DIR_NAME = '.tmp_nsem_user_export'
CWWED_NSEM_S3_USER_EXPORT_DIR_NAME = 'User Exports'

CWWED_ARCHIVES_ACCESS_KEY_ID = os.environ['CWWED_ARCHIVES_ACCESS_KEY_ID']
CWWED_ARCHIVES_SECRET_ACCESS_KEY = os.environ['CWWED_ARCHIVES_SECRET_ACCESS_KEY']

CWWED_PSA_USER_DATA_EXPORT_DAYS = 1

CWWED_CACHE_PSA_GEOJSON_DAYS = 365

OPENDAP_URL = 'http://{}:9000/opendap/'.format(os.environ.get('OPENDAP_HOST', 'localhost'))

SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
