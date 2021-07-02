from .base import *

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

if 'SENTRY_DSN' in os.environ:
    sentry_sdk.init(
        dsn=os.environ.get('SENTRY_DSN'),
        integrations=[DjangoIntegration()],

        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0,

        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True
    )

DEBUG = False
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
AWS_QUERYSTRING_AUTH = False

AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")

WAGTAILCONTENTIMPORT_MICROSOFT_CLIENT_ID = os.getenv(
    "WAGTAILCONTENTIMPORT_MICROSOFT_CLIENT_ID", ""
)

# Make sure Django can detect a secure connection properly on Heroku:
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Redirect all requests to HTTPS
SECURE_SSL_REDIRECT = os.getenv('DJANGO_SECURE_SSL_REDIRECT', 'off') == 'on'

# Email settings
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = env("EMAIL_PORT")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = env("EMAIL_USE_TLS")
EMAIL_USE_SSL = env("EMAIL_USE_SSL")
EMAIL_SUBJECT_PREFIX = env("EMAIL_SUBJECT_PREFIX")
SERVER_EMAIL = DEFAULT_FROM_EMAIL = env("SERVER_EMAIL")

WAGTAIL_IMAGE_IMPORT_GOOGLE_PICKER_API_KEY = os.getenv("WAGTAIL_IMAGE_IMPORT_GOOGLE_PICKER_API_KEY", "")
WAGTAILIMAGEIMPORT_GOOGLE_OAUTH_CLIENT_SECRET = os.getenv("WAGTAILIMAGEIMPORT_GOOGLE_OAUTH_CLIENT_SECRET", "")

try:
    from .local import *
except ImportError:
    pass
