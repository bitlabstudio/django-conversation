"""Settings that need to be set in order to run the tests."""
import os

DEBUG = True
USE_TZ = True
SITE_ID = 1

APP_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..'))


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

MIDDLEWARE_CLASSES = (
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'conversation.tests.urls'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(APP_ROOT, '../app_static')
MEDIA_ROOT = os.path.join(APP_ROOT, '../app_media')
STATICFILES_DIRS = (
    os.path.join(APP_ROOT, 'static'),
)

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'APP_DIRS': True,
    'DIRS': [os.path.join(APP_ROOT, 'tests/test_app/templates')],
    'OPTIONS': {
        'context_processors': (
            'django.contrib.auth.context_processors.auth',
            'django.template.context_processors.i18n',
            'django.template.context_processors.request',
            'django.template.context_processors.media',
            'django.template.context_processors.static',
            'django.contrib.messages.context_processors.messages',
        )
    }
}]

EXTERNAL_APPS = [
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'django_libs',
]

INTERNAL_APPS = [
    'conversation',
    'conversation.tests.test_app',
]

INSTALLED_APPS = EXTERNAL_APPS + INTERNAL_APPS

SECRET_KEY = 'foobar'

FROM_EMAIL = "info@example.com"
DEFAULT_FROM_EMAIL = FROM_EMAIL
SERVER_EMAIL = FROM_EMAIL
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
