from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    "localhost",
    "pose.tessercat.net",
    "civicdataecosystem.org",
    "www.civicdataecosystem.org",
    "dev.civicdataecosystem.org",
]

CSRF_TRUSTED_ORIGINS = [
    "https://dev.civicdataecosystem.org",
]

try:
    from .local import *
except ImportError:
    pass
