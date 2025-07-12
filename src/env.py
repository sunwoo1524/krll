from dotenv import load_dotenv
import os


load_dotenv(override=True)

NAME = os.environ.get("NAME")
HOST = os.environ.get("HOST")
CONTACT = os.environ.get("CONTACT")
NTFY = os.environ.get("NTFY")

JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")

POSTGRES_DATABASE = os.environ.get("POSTGRES_DATABASE")
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST")

CAPTCHA_MODE = os.environ.get("CAPTCHA_MODE")

site_key = None
secret_key = None
cap_instance = None

if not CAPTCHA_MODE is None:
    if CAPTCHA_MODE == "turnstile":
        site_key = os.environ.get("CF_TURNSTILE_SITE_KEY")
        secret_key = os.environ.get("CF_TURNSTILE_SECRET_KEY")
    elif CAPTCHA_MODE == "cap":
        site_key = os.environ.get("CAP_SITE_KEY")
        secret_key = os.environ.get("CAP_SECRET_KEY")
        cap_instance = os.environ.get("CAP_INSTANCE")
