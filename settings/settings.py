import os

from dotenv import load_dotenv

load_dotenv()

DATABASE = {
    "USER": os.environ.get("POSTGRES_USER"),
    "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
    "HOST": os.environ.get("POSTGRES_HOST"),
    "PORT": os.environ.get("POSTGRES_PORT"),
    "DB_NAME": os.environ.get("POSTGRES_DB_NAME"),
    "TEST_DB_NAME": os.environ.get("POSTGRES_TEST_DB_NAME"),
}
