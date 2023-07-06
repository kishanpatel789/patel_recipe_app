import pathlib
import os
from dotenv import load_dotenv


basedir = pathlib.Path(__file__).parent.resolve()
load_dotenv(basedir / ".env")

SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / 'recipe.db'}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = True

