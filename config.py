import pathlib

basedir = pathlib.Path(__file__).parent.resolve()

SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / 'recipe.db'}"
SQLALCHEMY_TRACK_MODIFICATIONS = False

DEBUG = True

