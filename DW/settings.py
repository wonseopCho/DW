"""
Django settings for DW project.

Generated by 'django-admin startproject' using Django 2.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'j)p9lo0zybdy77%2-6xzdps=spd0894+1dt9g*lczgd*_kkpjc'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '*', '.ktripguide.com', 'ktripguide.com', '.ap-northeast-2.compute.amazonaws.com']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_summernote',
    "sslserver",
    'pwa',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.twitter',
    'sortedm2m',
    'storages',
    'colorful',
    'embed_video',
    'imagekit',
    'multiupload',
    'smart_selects',
    'widget_tweaks',
    'blog',
    'blog2',
    'bookmark',
    'mapAPI',
    'accounts',
    'tips',
    'tips.templatetags',
    'recommendation',
    'board',
    'qna',
]

PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, 'service-worker.js') # in template the name 'serviceworker.js must be kept'
PWA_APP_NAME = 'KOREAtripGuide'
PWA_APP_SHORT_NAME = 'KOREAtripGuide'
PWA_APP_DESCRIPTION = 'KOREAtripGuide'
PWA_APP_THEME_COLOR = '#4dc7a0'
PWA_APP_BACKGROUND_COLOR = '#F7F8F9'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_START_URL = '/'
PWA_APP_ICONS = [
    {
      "src": "/static/Images/gps.png",
      "type": "image/png",
      "sizes": "48x48"
    },
    {
      "src": "/static/Images/gps.png",
      "type": "image/png",
      "sizes": "96x96"
    },
    {
      "src": "/static/Images/gps.png",
      "type": "image/png",
      "sizes": "144x144"
    },
    {
      "src": "/static/Images/gps.png",
      "type": "image/png",
      "sizes": "192x192"
    }
]
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'offline',
        }
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # 'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'DW.middleware.LoginRequiredMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',
    
]

ROOT_URLCONF = 'DW.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            #JB- 
            os.path.join(BASE_DIR, 'DW', 'templates'),
            #JB- To apply for glabal templates
        ],
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

AUTHENTICATION_BACKENDS = (
    
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
    
)

WSGI_APPLICATION = 'DW.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

'''
DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'wonseop$DW',
        'USER': 'wonseop',
        'PASSWORD': 'Cho277412',
        'HOST': 'wonseop.mysql.pythonanywhere-services.com',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}
'''
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

#smart_seletct requirments
# JQUERY_URL = True
USE_DJANGO_JQUERY = True
#------------------------------

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'DW', 'static')
]


# STATIC_ROOT = "/home/wonseop/DW/static" # for pyrthonanywhre
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'DW', 'media')
MEDIA_URL = '/media/'

GOOGLE_API_KEY = 'AIzaSyDTkQh8Koyc8fx_BluoKD3y45EeT3Qmong'

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/login/'

LOGIN_EXEMPT_URLS = [
    r'^login/$',
    r'^accounts/login/$',
    r'^accounts/register/$',
    r'^accounts/reset-password/$',
    r'^accounts/reset-password/done/$',
    r'^accounts/reset-password/confirm/<uidb64>/<token>/$',
    r'^accounts/reset-password/complete/$',
]

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#         'TIMEOUT': 3600,
#     }
# }

# CACHE_MIDDLEWARE_ALIAS = 'default'
# CACHE_MIDDLEWARE_SECONDS = 60 * 10
# CACHE_MIDDLEWARE_KEY_PREFIX = ''

if DEBUG :
    SITE_ID = 2
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    EMAIL_HOST = 'localhost'
    EMAIL_PORT = 1025
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'DW',
            'USER': 'JB',
            'PASSWORD': 'JB',
            'HOST': 'localhost',
            'PORT': '3306',
            'OPTIONS': {
                'charset': 'utf8',
                'init_command': 'SET character_set_connection=utf8;'
                                'SET collation_connection=utf8_unicode_ci;'
                                "SET NAMES 'utf8';"
                                "SET CHARACTER SET utf8;"
                                "SET sql_mode='STRICT_TRANS_TABLES'"
            }
        }
    }

    SUMMERNOTE_CONFIG = {
        'iframe': True,
        'airMode': False,
        'styleWithSpan': True,
        'direction': 'ltr',
        'empty': ('<p><br/></p>', '<p><br></p>'),
        'width': '100%',
        'toolbar': [
            ['style', ['style']],
            ['font', ['bold']],
            ['fontname', ['fontname']],
            ['fontsize', ['fontsize']],
            ['color', ['color']],
            ['para', ['paragraph']],
            ['height', ['height']],
            ['table', ['table']],
            ['insert', ['link', 'picture', 'video', 'hr']],
            ['view', ['fullscreen', 'codeview']],
            ['help', ['help']],
        ],
        'attachment_filesize_limit': 1024 * 1024 * 10, #10MB limits
        'js': ('/static/js/tips/article.js',),
    }

else :
    SITE_ID = 1
    EMAIL_BACKEND = 'django_amazon_ses.EmailBackend'
    EMAIL_HOST = 'email-smtp.us-west-2.amazonaws.com'
    EMAIL_PORT = 465
    EMAIL_USE_SSL = True
    MEDIAFILES_LOCATION = 'media'
    STATICFILES_LOCATION = 'static'
    AWS_ACCESS_KEY_ID = 'DW.keys.AWS_ACCESS_KEY_ID'
    AWS_SECRET_ACCESS_KEY = 'DW.keys.AWS_SECRET_ACCESS_KEY'
    AWS_STORAGE_BUCKET_NAME = 'ktrip'
    AWS_S3_CUSTOM_DOMAIN = "%s.s3.amazonaws.com" % AWS_STORAGE_BUCKET_NAME
    AWS_SES_REGION = 'us-west-2'
    DEFAULT_FROM_EMAIL = 'ktripguideservice@gmail.com'
    STATIC_URL = "https://%s/static/" % AWS_S3_CUSTOM_DOMAIN
    STATICFILES_STORAGE = 'DW.s3storages.StaticStorage'
    MEDIA_URL = "https://%s/media/" % AWS_S3_CUSTOM_DOMAIN
    DEFAULT_FILE_STORAGE = 'DW.s3storages.MediaStorage'

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'KtripDB',
            'USER': 'JB',
            'PASSWORD': 'Cho277412',
            'HOST': 'ktripdbinstance.c0p3n05acild.ap-northeast-2.rds.amazonaws.com',
            'PORT': '3306',
            'OPTIONS': {
                'charset': 'utf8',
                'init_command': 'SET character_set_connection=utf8;'
                                'SET collation_connection=utf8_unicode_ci;'
                                "SET NAMES 'utf8';"
                                "SET CHARACTER SET utf8;"
                                "SET sql_mode='STRICT_TRANS_TABLES'"
            }
        }
    }

    SUMMERNOTE_CONFIG = {
        'iframe': True,
        'airMode': False,
        'styleWithSpan': True,
        'direction': 'ltr',
        'empty': ('<p><br/></p>', '<p><br></p>'),
        'width': '100%',
        'toolbar': [
            ['style', ['style']],
            ['font', ['bold']],
            ['fontname', ['fontname']],
            ['fontsize', ['fontsize']],
            ['color', ['color']],
            ['para', ['paragraph']],
            ['height', ['height']],
            ['table', ['table']],
            ['insert', ['link', 'picture', 'video', 'hr']],
            ['view', ['fullscreen', 'codeview']],
            ['help', ['help']],
        ],
        'attachment_filesize_limit': 1024 * 1024 * 10, #10MB limits
        'js': ("https://%s/static/js/tips/article.js" % AWS_S3_CUSTOM_DOMAIN ,),
    }

    PWA_APP_ICONS = [
        {
          "src": "https://%s/static/Images/gps.png" % AWS_S3_CUSTOM_DOMAIN ,
          "type": "image/png",
          "sizes": "48x48"
        },
        {
          "src": "https://%s/static/Images/gps.png" % AWS_S3_CUSTOM_DOMAIN ,
          "type": "image/png",
          "sizes": "96x96"
        },
        {
          "src": "https://%s/static/Images/gps.png" % AWS_S3_CUSTOM_DOMAIN ,
          "type": "image/png",
          "sizes": "144x144"
        },
        {
          "src": "https://%s/static/Images/gps.png" % AWS_S3_CUSTOM_DOMAIN,
          "type": "image/png",
          "sizes": "192x192"
        }
    ]

    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT =True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    LOGGING_CONFIG = None


