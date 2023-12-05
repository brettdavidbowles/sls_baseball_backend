"""
Django settings for sls_baseball project.

Generated by 'django-admin startproject' using Django 3.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import environ
import json
import os
import mimetypes
mimetypes.add_type("text/css", ".css", True)

env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# if env('ENVIRONMENT') == 'production':
DEBUG = True
ALLOWED_HOSTS = ['baseballsimulator.online',
                 'slsbaseballbackend-production.up.railway.app',
                 'https://sls-baseball-frontend.vercel.app',
                 'localhost',
                 ]
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'None'
CSRF_COOKIE_SAMESITE = 'None'
CSRF_COOKIE_DOMAIN = 'https://sls-baseball-frontend.vercel.app'
CSRF_TRUSTED_ORIGINS = ['https://baseballsimulator.online',
                        'https://www.baseballsimulator.online',
                        'https://slsbaseballbackend-production.up.railway.app',
                        'https://sls-baseball-frontend.vercel.app',
                        ]
# CSRF_COOKIE_DOMAIN = 'https://slsbaseballbackend-production.up.railway.app'
# SESSION_COOKIE_SECURE = True
# CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = [
    #     "https://baseballsimulator.online",
    #     "https://www.baseballsimulator.online",
    'https://sls-baseball-frontend.vercel.app',
]
# if env('ENVIRONMENT') == 'development':
#     DEBUG = True
#     ALLOWED_HOSTS = ['baseballsimulator.online',
#                      '3.129.154.203', 'localhost']
#     CSRF_TRUSTED_ORIGINS = [
#         'https://baseballsimulator.online',
#         # 'http://localhost:3000',
#         'https://sls-baseball-frontend.vercel.app']
#     CORS_ALLOW_CREDENTIALS = True
#     CORS_ORIGIN_WHITELIST = [
#         "https://baseballsimulator.online",
#         "https://www.baseballsimulator.online",
#         # "http://localhost:3000"
#     ]


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'baseball.apps.BaseballConfig',
    'strawberry.django',
    "corsheaders",
]

AUTH_USER_MODEL = 'baseball.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://baseballsimulator.online",
    "https://slsbaseballbackend-production.up.railway.app",
    "https://sls-baseball-frontend.vercel.app"
]

ROOT_URLCONF = 'sls_baseball.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'sls_baseball.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# if 'RDS_DB_NAME' in environ:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.postgresql_psycopg2',
#             'NAME': environ['RDS_DB_NAME'],
#             'USER': environ['RDS_USERNAME'],
#             'PASSWORD': environ['RDS_PASSWORD'],
#             'HOST': environ['RDS_HOSTNAME'],
#             'PORT': environ['RDS_PORT'],
#         }
#     }
# else:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env("DATABASE_NAME"),
        'USER': env("DATABASE_USER"),
        'PASSWORD': env("DATABASE_PASSWORD"),
        'HOST': env("DATABASE_HOST"),
        'PORT': env("DATABASE_PORT"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
# if env('ENVIRONMENT') == 'production':
#     STATIC_ROOT = env('STATIC_ROOT')
#     STATICFILES_DIRS = [BASE_DIR / "static"]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STRAWBERRY_DJANGO = {
    "FIELD_DESCRIPTION_FROM_HELP_TEXT": True,
    "TYPE_DESCRIPTION_FROM_MODEL_DOCSTRING": True,
}
