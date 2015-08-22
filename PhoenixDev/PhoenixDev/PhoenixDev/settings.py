"""
Django settings for phoenix project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+spp&+9d7v%un8%xo@&=oni-)dxv2ihj930834hjug4)o2h5ae'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    
    
    'PhoenixDev.PhoenixWebService.User',
    'PhoenixDev.PhoenixWebService.Seller',
    'PhoenixDev.PhoenixWebService.Product',
    'PhoenixDev.PhoenixWebService.Bargain',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    #'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'django.contrib.messages.middleware.MessageMiddleware',
    #'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'PhoenixDev.urls'

WSGI_APPLICATION = 'PhoenixDev.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default_orig': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    'default' : {
		'ENGINE': 'django.db.backends.mysql',
		'NAME': 'phoenix_dev',
		'USER': 'project005',
		'PASSWORD': 'pivotproject005',
		'HOST': 'project005.cloudapp.net',
		'PORT': '3306',
	}
		
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'


SESSION_ENGINE  = 'django.contrib.sessions.backends.db'

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

#SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_SECURE = False 


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'debug_logfile.txt'),
            'formatter': 'verbose',
        },
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s:%(asctime)s:%(pathname)s:%(funcName)s:%(lineno)d:%(process)d:%(thread)d [%(message)s]'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },

    'loggers': {
        'phoenix.logger': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
            
        },
    },
}

