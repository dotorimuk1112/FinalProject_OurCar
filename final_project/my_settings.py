from dotenv import load_dotenv
import os
import json

load_dotenv()

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "HOST": os.environ.get("DB_HOST"),
        "PORT": os.environ.get("DB_PORT"),
    }
}

AWS_ACCESS_ID=os.environ.get("AWS_ACCESS_ID")
AWS_SECRET_KEY=os.environ.get("AWS_SECRET_KEY")
BUCKET_NAME=os.environ.get("BUCKET_NAME")
REGION_NAME=os.environ.get("REGION_NAME")
CUSTOM_DOMAIN=os.environ.get("CUSTOM_DOMAIN")
DEFAULT_FILE_STORAGE=os.environ.get("DEFAULT_FILE_STORAGE")