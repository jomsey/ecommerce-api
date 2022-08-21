from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-)@+1&z##5&l=(d9)$*&&m**75om#ev=5c0-dmdl$4#1(+=fd@o'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

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
    'rest_framework_swagger',
    'debug_toolbar',
    'django_filters',
    'oauth2_provider',
    'social_django',
    'rest_framework_social_oauth2',

    'main'
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
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
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'jshop_api.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
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

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



REST_FRAMEWORK = { 'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema' ,
                   'DEFAULT_AUTHENTICATION_CLASSES': ['rest_framework.authentication.BasicAuthentication',
                                                     'rest_framework.authentication.SessionAuthentication',
                                                     'rest_framework_simplejwt.authentication.JWTAuthentication',
                                                     # 'oauth2_provider.contrib.rest_framework.OAuth2Authentication',  # django-oauth-toolkit >= 1.0.0
                                                     #  'rest_framework_social_oauth2.authentication.SocialAuthentication',
                                                    ],
                #    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
                #    'PAGE_SIZE': 30,
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

AUTHENTICATION_BACKENDS = [
                           'rest_framework_social_oauth2.backends.DjangoOAuth2',
                           'django.contrib.auth.backends.ModelBackend',
                       ]
# Google configuration
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '839918766631-1vft8r58h9vsoakcuqkh2kpff20p5e6a.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'

# SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE to get extra permissions from Google.
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
                                    'https://www.googleapis.com/auth/userinfo.email',
                                     'https://www.googleapis.com/auth/userinfo.user',
                                ]

