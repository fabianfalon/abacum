"""Testing settings.
With these settings, tests run faster.
"""

from .base import *  # NOQA
from .base import env

# Base
DEBUG = False
SECRET_KEY = env("DJANGO_SECRET_KEY", default="7lEaACt4wsCj8JbXYgQLf4BmdG5QbuHTMYUGir2Gc1GHqqb2Pv8w9iXwwlIIviI2")

TEST_RUNNER = "django.test.runner.DiscoverRunner"

# Templates
TEMPLATES[0]["OPTIONS"]["debug"] = DEBUG  # NOQA
TEMPLATES[0]["OPTIONS"]["loaders"] = [  # NOQA
    (
        "django.template.loaders.cached.Loader",
        [
            "django.template.loaders.filesystem.Loader",
            "django.template.loaders.app_directories.Loader",
        ],
    )
]
