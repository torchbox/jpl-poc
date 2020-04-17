from .base import *

DEBUG = False
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
AWS_QUERYSTRING_AUTH = False

AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")

ICONTACT_SETTINGS = {
    "version": "2.2",
    "url": env("ICONTACT_URL"),
    "app_id": env("ICONTACT_APP_ID"),
    "username": env("ICONTACT_USERNAME"),
    "password": env("ICONTACT_PASSWORD"),
    "campaign_id": env("ICONTACT_CAMPAIGN_ID"),
}

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

try:
    from .local import *
except ImportError:
    pass
