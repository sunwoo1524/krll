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

CFTS_SITE_KEY = os.environ.get("CF_TURNSTILE_SITE_KEY")
CFTS_SECRET_KEY = os.environ.get("CF_TURNSTILE_SECRET_KEY")
