from .base import *

DEBUG = True

ALLOWED_HOSTS = [
    "localhost",
    "pose.tessercat.net",
    "civicdataecosystem.org",
    "www.civicdataecosystem.org",
]

try:
    from .local import *
except ImportError:
    pass
