from base import *

# SECURITY WARNING: keep the secret key used in production secret!
# REGENERATE BEFORE GOING LIVE
SECRET_KEY = '_pc!4wzqt3@keowtpm_r#6(qiuw9#+)-7dwnx8hl#jg*e0mu10'

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
STATIC_ROOT = '/var/stream3/fuel_tracker_static_files/'

STATIC_URL = '/static/'

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
