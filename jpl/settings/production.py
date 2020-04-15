from .base import *

DEBUG = False

try:
    from .local import *
except ImportError:
    pass

WAGTAILCONTENTIMPORT_MICROSOFT_CLIENT_ID = os.getenv('WAGTAILCONTENTIMPORT_MICROSOFT_CLIENT_ID', '')