from base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ('*',)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

STRIPE_SECRET = os.getenv('STRIPE_SECRET', 'sk_test_NQbrilT8lvYivrEJiDLrU8El')
STRIPE_PUBLISHABLE = os.getenv('STRIPE_PUBLISHABLE', 'pk_test_1pT0Ki5W4blEr9hnrqxnjpb9')