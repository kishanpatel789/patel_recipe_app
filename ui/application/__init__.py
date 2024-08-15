from flask import Flask
from .config import Config

def create_app():
    app = Flask(__name__)

    # read config json
    app.config.from_object(Config)

    with app.app_context():
        # Include our Routes
        from . import routes

        # Register Blueprints

        return app

