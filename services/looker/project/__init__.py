import os

from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()
# must create db before import DXCache
from project.api.db_cache import DBCache
from project.api.models import DXLooker, InvoicingByLibrary, SendsByLibrary

ibl_cache = DBCache(InvoicingByLibrary)
sends_cache = DBCache(SendsByLibrary)

look_ids = {
    "4404": ibl_cache,
    "4405": sends_cache
}


def create_app(script_info=None):
    app = Flask(__name__)

    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    db.init_app(app)

    from project.api.routes import dx_looker_blueprint
    app.register_blueprint(dx_looker_blueprint)

    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    return app
