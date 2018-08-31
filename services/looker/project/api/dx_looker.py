import os

from flask import Blueprint, jsonify, request
from sqlalchemy import exc

from project.api.models import DXLooker
from project import db#, dx_cache

dx_looker_blueprint = Blueprint("dx_looker", __name__)

ESM = "email_send_month"


@dx_looker_blueprint.route("/dx_looker/ping", methods=["GET"])
def ping_pong():
    return jsonify({
        "status": "success",
        "message": "pong"
    })
