import os

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify
from project.api.dx_cache import DXCache

db = SQLAlchemy()
dx_cache = DXCache(db)


def create_app(script_info=None):
    app = Flask(__name__)

    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    db.init_app(app)
    # dx_cache.db.init_app(app)

    from project.api.dx_looker import dx_looker_blueprint
    app.register_blueprint(dx_looker_blueprint)

    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    return app
