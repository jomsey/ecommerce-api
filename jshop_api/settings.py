from pathlib import Path
from datetime import timedelta
import environ

#initialize environement varrialbles
environ.Env.read_env()
env = environ.Env()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = ['*']
INTERNAL_IPS = [
    "127.0.0.1",
]


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'debug_toolbar',
    'django_filters',
    'corsheaders',
    'django_q',
    
    'main',
    'store',
]


MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'jshop_api.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            
            ],
            'libraries' : {
                'staticfiles': 'django.templatetags.static', 
            }
        },
    },
]

WSGI_APPLICATION = 'jshop_api.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': env('DATABASE_NAME'),
    #     'USER':env('DATABASE_USER'),
    #     'PORT':5432,
    #     'PASSWORD':env('DATABASE_PASSWORD'),
    #     'HOST':env('HOST')


    # }
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}



AUTH_USER_MODEL="main.CustomUser"
swappable = 'AUTH_USER_MODEL'



# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Nairobi'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR/'staticfiles',]
STATIC_ROOT = BASE_DIR/'static'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


REST_FRAMEWORK = { 'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema' ,

                   'DEFAULT_AUTHENTICATION_CLASSES': ['rest_framework.authentication.BasicAuthentication',
                                                     'rest_framework.authentication.SessionAuthentication',
                                                     'rest_framework_simplejwt.authentication.JWTAuthentication',
                                                    ],

                   'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
                   'PAGE_SIZE': 28,

                   'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend',
                                               'rest_framework.filters.SearchFilter'

                                              ]
                   ,

                  }


SIMPLE_JWT = {
                'ACCESS_TOKEN_LIFETIME': timedelta(weeks=1),
                'REFRESH_TOKEN_LIFETIME': timedelta(weeks=1),
                'ROTATE_REFRESH_TOKENS': False,
                'BLACKLIST_AFTER_ROTATION': True,
                 
}

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# More details https://django-q.readthedocs.io/en/latest/configure.html
Q_CLUSTER = {
    'timeout': 60,
    'retry': 100,
    "name": "j-shop",
    "orm": "default",  # Use Django's ORM + database for broker
}


CORS_ALLOWED_ORIGINS = [
   'http://localhost:5173',
   'https://jecomm.netlify.app'
]