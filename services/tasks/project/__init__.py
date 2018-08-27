# services/tasks/project/__init__.py

import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

# instantiate the db
db = SQLAlchemy()
app = Flask(__name__)

def create_app():

    # instantiate the app
    # app = Flask(__name__)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # set up extensions
    db.init_app(app)

    # register blueprints
    # from project.api.views.items import items_blueprint
    # from project.api.views.items_statuses import items_statuses_blueprint
    # from project.api.views.users import users_blueprint
    # app.register_blueprint(items_blueprint)
    # app.register_blueprint(items_statuses_blueprint)
    # app.register_blueprint(users_blueprint)

    return app

# routes
@app.route('/tasks/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })