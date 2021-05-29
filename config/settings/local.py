"""Development settings."""

from .base import *  # NOQA
from .base import env
# Base
DEBUG = True

# Security
ALLOWED_HOSTS = [
    "localhost",
    "0.0.0.0",
    "127.0.0.1",
]

# Templates
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG  # NOQA


# django-extensions
INSTALLED_APPS += ['django_extensions']  # noqa F405


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': "abacum",
#         'USER': "sBLRWyyPsInwHftmHAWmYJURGWBGFpLs",
#         'PASSWORD': "tuXL3XSF8O7tsGrcGHoMos4tVNtL3tnrRshSCZokGnIfk4ArDyzaa297k2WgQPSL",
#         'HOST': "127.0.0.1",
#         'PORT': '5432'
#     }
# }
