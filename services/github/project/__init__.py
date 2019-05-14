import os
from flask import Flask, jsonify


def create_app():
    # instantiate the app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # register blueprints
    from project.api.routes import github_blueprint
    app.register_blueprint(github_blueprint)

    return app
