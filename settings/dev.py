from base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

INTERNAL_IPS = ('127.0.0.1',)

# Application definition

INSTALLED_APPS.append('debug_toolbar')

MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

STRIPE_SECRET = os.getenv('STRIPE_SECRET', 'sk_test_NQbrilT8lvYivrEJiDLrU8El')
STRIPE_PUBLISHABLE = os.getenv('STRIPE_PUBLISHABLE', 'pk_test_1pT0Ki5W4blEr9hnrqxnjpb9')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = 'james@mtb.space'
EMAIL_HOST = 'mail.privateemail.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'james@mtb.space'
EMAIL_HOST_PASSWORD = 'E?V48+h397bz'
EMAIL_USE_SSL = True

EMAIL_TO = 'james@mtb.space'
