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
import raven
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'ssshhh...')

DEPLOY_STAGE_LOCAL = 'local'
DEPLOY_STAGE_DEV = 'dev'
DEPLOY_STAGE_TEST = 'test'
DEPLOY_STAGE_PROD = 'prod'
DEPLOY_STAGE = os.environ.get('DEPLOY_STAGE', DEPLOY_STAGE_LOCAL)

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
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'crispy_forms',
    'raven.contrib.django.raven_compat',
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


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# sentry/logging configuration
RAVEN_CONFIG = {
    'dsn': os.getenv('SENTRY_DSN', ''),
    # automatically configure the release based on the git info
    'release': raven.fetch_git_sha(os.path.dirname(os.pardir)),
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

# WhiteNoise
# http://whitenoise.evans.io/en/stable/django.html
STATIC_URL = "/static/"
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATIC_ANGULAR_ASSETS_URL = "{}angular/".format(STATIC_URL)

# custom file storage
DEFAULT_FILE_STORAGE = 'cwwed.storage_backends.S3ObjectStorage'
AWS_ARCHIVE_BUCKET_NAME = 'cwwed-archives'
AWS_S3_ARCHIVE_DOMAIN = '%s.s3.amazonaws.com' % AWS_ARCHIVE_BUCKET_NAME

MEDIA_URL = '/media/'
MEDIA_ROOT = '/media/bucket/cwwed'


# Logging
# https://docs.djangoproject.com/en/2.0/topics/logging/
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'sentry': {
            'level': 'WARNING',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'tags': {'custom-tag': 'x'},
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['sentry', 'console'],
        'level': 'INFO',
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s  %(asctime)s  %(module)s '
                      '%(process)d  %(thread)d  %(message)s'
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
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
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
    ),
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

CWWED_ARCHIVE_EXTENSION = 'tgz'
CWWED_DATA_DIR = MEDIA_ROOT
CWWED_THREDDS_DIR = 'THREDDS'

CWWED_COVERED_DATA_DIR_NAME = 'Covered Data'
CWWED_COVERED_ARCHIVE_DIR_NAME = 'Covered Data Archive'
CWWED_COVERED_DATA_INCOMPLETE_DIR_NAME = '.incomplete'

CWWED_NSEM_DIR_NAME = 'NSEM'
CWWED_NSEM_PSA_DIR_NAME = 'Post Storm Assessment'
CWWED_NSEM_UPLOAD_DIR_NAME = 'upload'
CWWED_NSEM_ARCHIVE_WRITE_MODE = 'w:gz'
CWWED_NSEM_ARCHIVE_READ_MODE = 'r:gz'
CWWED_NSEM_USER = 'nsem'
CWWED_NSEM_PASSWORD = os.environ.get('CWWED_NSEM_PASSWORD')

CWWED_ARCHIVES_ACCESS_KEY_ID = os.environ['CWWED_ARCHIVES_ACCESS_KEY_ID']
CWWED_ARCHIVES_SECRET_ACCESS_KEY = os.environ['CWWED_ARCHIVES_SECRET_ACCESS_KEY']

THREDDS_URL = 'http://{}:9000/thredds/'.format(os.environ.get('THREDDS_HOST', 'localhost'))

SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
