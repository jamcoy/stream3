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

STRIPE_PUBLISHABLE = os.getenv('STRIPE_PUBLISHABLE', 'publishable key')
STRIPE_SECRET = os.getenv('STRIPE_SECRET', 'secret key')
