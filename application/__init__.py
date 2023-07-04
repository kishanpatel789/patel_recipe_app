from flask import Flask
import pathlib

basedir = pathlib.Path(__file__).parents[1].resolve()



def create_app():
    app = Flask(__name__)
    app.config.from_pyfile(f"{basedir / 'config.py'}")

    from .models import db
    db.init_app(app)

    with app.app_context():
        # Include our Routes
        from . import routes

        # Register Blueprints

        return app
