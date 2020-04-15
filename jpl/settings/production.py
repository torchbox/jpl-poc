from .base import *

DEBUG = False
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
AWS_QUERYSTRING_AUTH = False

AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")

try:
    from .local import *
except ImportError:
    pass

WAGTAILCONTENTIMPORT_MICROSOFT_CLIENT_ID = os.getenv(
    "WAGTAILCONTENTIMPORT_MICROSOFT_CLIENT_ID", ""
)

# Make sure Django can detect a secure connection properly on Heroku:
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Redirect all requests to HTTPS
SECURE_SSL_REDIRECT = os.getenv('DJANGO_SECURE_SSL_REDIRECT', 'off') == 'on'