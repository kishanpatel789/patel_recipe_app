import pathlib
import os
from dotenv import load_dotenv


basedir = pathlib.Path(__file__).parent.resolve()
load_dotenv(basedir / ".env")

# SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / 'recipe.db'}"
DB_USER = os.environ.get("DB_USER")
DB_PW = os.environ.get("DB_PW")
DB_HOST = os.environ.get("DB_HOST")
DB_DATABASE = os.environ.get("DB_DATABASE")
SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PW}@{DB_HOST}:5432/{DB_DATABASE}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO=True
SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = True

