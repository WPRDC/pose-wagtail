from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    "pose.tessercat.net",
    "civicdataecosystem.org",
    "www.civicdataecosystem.org",
]

try:
    from .local import *
except ImportError:
    pass
