"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY','(n5=3!jpyt8_2ln5ni^d*0kj0*9t6nqkk6+l7y6_axy%d*rm8l')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG',True)

ALLOWED_HOSTS = []
allowed_host = os.getenv('ALLOWED_HOSTS', '*')
if  allowed_host is not None:
    ALLOWED_HOSTS.extend(allowed_host.split(','))

CORS_ORIGIN_ALLOW_ALL = os.getenv('CORS_ORIGIN_ALLOW_ALL', True)
CORS_ORIGIN_WHITELIST = []
cors_allowed_host = None#  os.getenv('ALLOWED_HOST', 'http://*,https://*')
if  cors_allowed_host is not None:
    CORS_ORIGIN_WHITELIST.extend(cors_allowed_host.split(','))

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles', # required for serving swagger ui's css/js files
    'django_extensions',
    # Django REST framework , swagger
    'rest_framework',
    'drf_spectacular',
    # CORS
    'corsheaders',

    #OWN APPS
    'app.orders.apps.OrdersConfig',
    'app.pc_components.apps.PcComponentsConfig',
    'app.users.apps.UsersConfig'
]

MIDDLEWARE = [
    # CORS
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'app.app.urls'

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

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# Get key from .env
load_dotenv()
DATABASE_ADMIN_PASSWORD_RENDER = os.getenv('DATABASE_ADMIN_PASSWORD_RENDER')  #DATABASE_ADMIN_PASSWORD_LOCAL = os.getenv('DATABASE_ADMIN_PASSWORD_LOCAL')

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",                             #django.db.backends.postgresql
        "NAME": "Database_for_django_pc_webshop_api",                          #django_pc_shop_api
        "USER": "database_for_django_pc_webshop_api_user",                     #shop_api_admin
        "PASSWORD": DATABASE_ADMIN_PASSWORD_RENDER,                            #DATABASE_ADMIN_PASSWORD_LOCAL
        "HOST": "dpg-cv9kbglumphs73a8e7eg-a.frankfurt-postgres.render.com",    #localhost
        "PORT": "5432",
    }
}


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

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

'DEFAULT_AUTHENTICATION_CLASSES': [
    'rest_framework_simplejwt.authentication.JWTAuthentication',
    ]

}

#Swagger Documentation
SPECTACULAR_SETTINGS = {
    "TITLE": "Django DRF Ecommerce",
}


REDOC_SETTINGS = {
    'LAZY_RENDERING': False,
}





# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
STATIC_URL = '/static/'
MEDIA_URL = 'media/'

#STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_ROOT = '/share/static/'


AUTH_USER_MODEL = 'users.User'