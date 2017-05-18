from .base import *  # NoQA


DEBUG = True

# make tests faster by changing changing password hashers
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

# set dummy cache - we don't need it in tests
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache'
    }
}

# change email backend
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

AUTH_PASSWORD_VALIDATORS = []
