from base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ('*',)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'stream3',
        'USER': 'djangouser',
        'PASSWORD': 'Rai9Pb3cWMMfnVmMNmjW6rFG',
        'HOST': 'localhost',
        'PORT': '',
    }
}

# static files in production
STATIC_ROOT = '/var/www/stream3.jamcoy.com/'

STRIPE_SECRET = os.getenv('STRIPE_SECRET', 'sk_test_NQbrilT8lvYivrEJiDLrU8El')
STRIPE_PUBLISHABLE = os.getenv('STRIPE_PUBLISHABLE', 'pk_test_1pT0Ki5W4blEr9hnrqxnjpb9')

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'testing@example.com'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
EMAIL_PORT = 1025