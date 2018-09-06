import os

from flask import Blueprint, jsonify, request

from project.api.looker_api_handler import get_look

dx_looker_blueprint = Blueprint("dx_looker", __name__)

ESM = "email_send_month"


@dx_looker_blueprint.route("/dx_looker/ping", methods=["GET"])
def ping_pong():
    return jsonify({
        "status": "success",
        "message": "pong"
    })


@dx_looker_blueprint.route("/dx_looker/<look_id>", methods=["GET"])
def get_look_id(look_id):
    """Get look_id data"""
    # db_cache = look_ids[look_id]
    # data = db_cache.cache
    # if not db_cache.cache:
    #     db_cache.db.create_all()
    #     db_cache.db.session.commit()
    #     data = db_cache.refresh_cache()
    data = get_look(look_id)
    response_object = {
        "status": "success",
        "data": data
    }
    return jsonify(response_object), 200
