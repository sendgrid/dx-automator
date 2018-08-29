import os

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify


db = SQLAlchemy()


def create_app(script_info=None):
    app = Flask(__name__)

    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    db.init_app(app)

    from project.api.dx_looker import dx_looker_blueprint
    app.register_blueprint(dx_looker_blueprint)

    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    return app


# from flask_debugtoolbar import DebugToolbarExtension
#
# # instantiate the db
# db = SQLAlchemy()
# toolbar = DebugToolbarExtension()
#
#
# def create_app(script_info=None):
#
#     # instantiate the app
#     app = Flask(__name__)
#
#     # set config
#     app_settings = os.getenv('APP_SETTINGS')
#     app.config.from_object(app_settings)
#
#     # set up extensions
#     db.init_app(app)
#     toolbar.init_app(app)
#
#     # register blueprints
#     from project.api.looker import dx_looker_blueprint
#     app.register_blueprint(dx_looker_blueprint)
#
#     # shell context for flask cli
#     @app.shell_context_processor
#     def ctx():
#         return {'app': app, 'db': db}
#
#     return app
