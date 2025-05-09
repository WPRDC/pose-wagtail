from .base import *
import os
from dotenv import load_dotenv

load_dotenv()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# dev apps
if os.environ.get("ENVIRONMENT") != "production":
    INSTALLED_APPS += [
        "django_browser_reload",
    ]


try:
    from .local import *
except ImportError:
    pass
