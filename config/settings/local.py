from os import getenv, path

from dotenv import load_dotenv

from .base import *  # noqa
from .base import APPS_DIRS

local_env_file = path.join(BASE_DIR, ".vens", ".env.local")
if path.isfile(local_env_file):
    load_dotenv(local_env_file)

SECRET_KEY = getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = getenv("DEBUG")
SITE_NAME = getenv("SITE_NAME")
ALLOWED_HOSTS = getenv("ALLOWED_HOSTS", "localhost,127.0.0.1,0.0.0.0").split(",")

ADMIN_URL = getenv("ADMIN_URL")

# Email settings
EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"
EMAIL_HOST = getenv("EMAIL_HOST")
EMAIL_PORT = getenv("EMAIL_PORT")
DEFAULT_FROM_EMAIL = getenv("DEFAULT_FROM_EMAIL", default="alisinasultani@gmail.com")
MAX_UPLOAD_SIZE = 1 * 1024 * 1024

CSRF_TRUSTED_ORIGINS = ["http://localhost:8000"]
LOCKOUT_DURATION = timedelta(minutes=1)
LOGIN_ATTEMPTS = 3
OPT_EXPIRATION = timedelta(minutes=1)
