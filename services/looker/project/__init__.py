import os

from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()
# must create db before import DXCache
from project.api.dx_cache import DXCache
from project.api.models import DXLooker
dx_cache = DXCache(db, DXLooker)


def create_app(script_info=None):
    app = Flask(__name__)

    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    dx_cache.db.init_app(app)
    # db.init_app(app)

    from project.api.dx_looker import dx_looker_blueprint
    app.register_blueprint(dx_looker_blueprint)

    @app.shell_context_processor
    def ctx():
        # return {"app": app, "db": db}
        return {"app": app, "db": dx_cache.db}

    return app
