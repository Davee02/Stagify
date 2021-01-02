from pathlib import Path
import os
import sys

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'q+@9+9br!&gal37kganb367-9!+tra4(4g68^gdwm99pc&ja-^')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('IS_DEBUG', 'TRUE') == 'TRUE'

ALLOWED_HOSTS = ['*']




# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'corsheaders',
    'api.apps.ApiConfig',
    "storages"
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'stagifyapi.urls'

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

CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
    "http://stagifyapp.azurewebsites.net",
    "https://stagifyapp.azurewebsites.net",
]

WSGI_APPLICATION = 'stagifyapi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DATABASE_NAME', 'stagify'),
        'USER': os.environ.get('DATABASE_USER', 'stagify-user'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', 'stagify-password'),
        'HOST': os.environ.get('DATABASE_HOST', 'localhost'),
        'PORT':  os.environ.get('DATABASE_PORT', '5433'),
        'OPTIONS': {
            'sslmode': os.environ.get('DATABASE_SSL_MODE', 'allow')
        }
    }
}

if 'test' in sys.argv:
    DATABASES['default'] = {'ENGINE': 'django.db.backends.sqlite3'}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_URL = '/uploads/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')

AZURE_CONTAINER = os.environ.get('AZURE_MEDIA_STORAGE_CONTAINER', 'container for media storage on azure')
AZURE_CONNECTION_STRING = os.environ.get('AZURE_MEDIA_STORAGE_CONNECTION_STRING', 'connection string for media storage on azure')
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = False