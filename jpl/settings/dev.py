from .base import *

DEBUG = True
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

INSTALLED_APPS += ["wagtail.contrib.styleguide"]

try:
    from .local import *
except ImportError:
    pass
