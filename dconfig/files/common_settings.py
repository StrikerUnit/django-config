import os

from utils.misc import import_app


class EnvironDict(object):

    def __getattr__(self, attrname):
        import os
        if attrname in os.environ:
            return os.environ[attrname]
        raise AttributeError()

try:
    import configs
except ImportError:
    try:
        configs = EnvironDict()
    except:
        configs = {}


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = getattr(configs, 'SECRET_KEY', '{SECRET_KEY}')
PRODUCTION = getattr(configs, 'PRODUCTION', False)

DEBUG = not PRODUCTION
TEMPLATE_DEBUG = not PRODUCTION

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
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

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

ENGINE = getattr(configs, 'ENGINE', None)
if not ENGINE or ENGINE == 'sqlite3':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': getattr(configs, 'DB_NAME', os.path.join(BASE_DIR, 'db.sqlite3')),
        }
    }
elif ENGINE == 'mysql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': getattr(configs, 'DB_NAME', 'dbname'),
            'USER': getattr(configs, 'DB_USER', 'root'),
            'PASSWORD': getattr(configs, 'DB_PASSWORD', 'password'),
            'HOST': getattr(configs, 'DB_HOST', '127.0.0.1'),
        }
    }
elif ENGINE == 'postgresql'
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': getattr(configs, 'DB_NAME', 'dbname'),
            'USER': getattr(configs, 'DB_USER', 'root'),
            'PASSWORD': getattr(configs, 'DB_PASSWORD', 'password'),
            'HOST': getattr(configs, 'DB_HOST', '127.0.0.1'),
            'PORT': '5432',
        }
    }

ALLOWED_HOSTS = getattr(configs, 'ALLOWED_HOSTS', [])

ROOT_URLCONF = '{DJANGO_PROJECT}.urls'
WSGI_APPLICATION = '{DJANGO_PROJECT}.wsgi.application'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Bangkok'
USE_I18N = True
USE_L10N = True
USE_TZ = False
DATE_FORMAT = "SHORT_DATE_FORMAT"

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

TEMPLATE_CONTEXT_PROCESSORS = [
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.template.context_processors.debug',
    'django.template.context_processors.i18n',
    'django.template.context_processors.media',
    'django.template.context_processors.static',
    'django.template.context_processors.tz',
    'django.template.context_processors.request',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': TEMPLATE_DIRS,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': TEMPLATE_CONTEXT_PROCESSORS,
        },
    },
]

if DEBUG:
    if import_app('debug_toolbar', INSTALLED_APPS):
        INTERNAL_IPS = ['127.0.0.1']
        MIDDLEWARE_CLASSES.insert(
            MIDDLEWARE_CLASSES.index('django.middleware.common.CommonMiddleware') + 1,
            'debug_toolbar.middleware.DebugToolbarMiddleware')

import_app('dconfig', INSTALLED_APPS)  # Try import dconfig it self

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',  # Older version use django.utils.log.NullHandler
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'WARN',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARN',
        },
    },
}

RAVEN_DSN = getattr(configs, 'RAVEN_DSN', False)
if RAVEN_DSN:
    import raven
    INSTALLED_APPS += [
        'raven.contrib.django.raven_compat',
    ]

    RAVEN_CONFIG = {
        'dsn': RAVEN_DSN,
        'release': raven.fetch_git_sha(str(BASE_DIR)),
    }

    LOGGING['formatters']['verbose']  = {
        'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
    }
    LOGGING['handlers']['sentry'] = {
        'level': 'ERROR',
        'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
    }
    LOGGING['root'] = {
        'level': 'WARNING',
        'handlers': ['sentry'],
    }
    LOGGING['loggers']['raven'] = {
        'level': 'DEBUG',
        'handlers': ['console'],
        'propagate': False,
    }
    LOGGING['loggers']['sentry.errors'] = {
        'level': 'ERROR',
        'handlers': ['console'],
        'propagate': False,
    }
    LOGGING['handlers']['console']['formatter'] = 'verbose'

    MIDDLEWARE_CLASSES.append('raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware')
