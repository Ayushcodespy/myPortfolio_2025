import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def _get_bool(key, default=False):
    value = os.getenv(key)
    if value is None:
        return default
    return value.strip().lower() in ("1", "true", "yes", "on")


def _get_list(key, default=""):
    value = os.getenv(key, default)
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "django-insecure-&x9_c@7-5l@5w916a_7e+9xuj1&$_v7nyp!cn11dsfmmgw#eto",
)
DEBUG = _get_bool("DEBUG", True)
ALLOWED_HOSTS = _get_list("ALLOWED_HOSTS", "*") or ["*"]

DATABASE_URL = os.getenv("DATABASE_URL", "")

RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID", "")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET", "")

EMAIL_BACKEND = os.getenv("EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = os.getenv("EMAIL_HOST", "")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_SSL = _get_bool("EMAIL_USE_SSL", False)
EMAIL_USE_TLS = _get_bool("EMAIL_USE_TLS", True)
if EMAIL_USE_SSL:
    EMAIL_USE_TLS = False

DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER)
PORTFOLIO_ADMIN_EMAIL = os.getenv("PORTFOLIO_ADMIN_EMAIL", DEFAULT_FROM_EMAIL)

SITE_URL = os.getenv("SITE_URL", "http://127.0.0.1:8000")
EMAIL_LOGO_URL = os.getenv("EMAIL_LOGO_URL", "")
