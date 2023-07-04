import pathlib

import connexion
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

basedir = pathlib.Path(__file__).parent.resolve()
# connex_app = connexion.App(__name__, specification_dir=basedir)
connex_app = connexion.FlaskApp(__name__, specification_dir=basedir)
# connex_app.add_api(basedir / "swagger.yml")


app = connex_app.app
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{basedir / 'recipe.db'}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["DEBUG"] = True

db = SQLAlchemy(app)
ma = Marshmallow(app)
