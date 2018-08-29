import os

from flask import Blueprint, jsonify, request
from sqlalchemy import exc

from project.api.models import DXLooker
from project import db

dx_looker_blueprint = Blueprint("dx_looker", __name__)

ESM = "email_send_month"


@dx_looker_blueprint.route("/dx_looker/ping", methods=["GET"])
def ping_pong():
    return jsonify({
        "status": "success",
        "message": "pong"
    })


@dx_looker_blueprint.route("/dx_looker", methods=["POST"])
def add_month():
    post_data = request.get_json()
    response_object = {
        "status": "fail",
        "message": "Invalid payload."
    }
    if not post_data:
        return jsonify(response_object), 400
    esm = post_data.get(ESM)
    try:
        dxl = DXLooker.query.filter_by(email_send_month=esm).first()
        if not dxl:
            db.session.add(DXLooker(email_send_month=esm))
            db.session.commit()
            response_object["status"] = "success"
            response_object["message"] = "{} was added!".format(esm)
            return jsonify(response_object), 201
        else:
            response_object["message"] = "That {} already exists.".format(ESM)
            return jsonify(response_object), 400
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify(response_object), 400


@dx_looker_blueprint.route("/dx_looker/<dxl_id>".format(ESM), methods=["GET"])
def get_single_month(dxl_id):
    """Get single email_send_month details"""
    response_object = {
        "status": "fail",
        "message": "{} does not exist".format(ESM)
    }
    try:
        dxl = DXLooker.query.filter_by(id=int(dxl_id)).first()
        if not dxl:
            return jsonify(response_object), 404
        else:
            response_object = {
                "status": "success",
                "data": dxl.to_json()
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


@dx_looker_blueprint.route("/dx_looker", methods=["GET"])
def get_all_months():
    """Get all months"""
    response_object = {
        "status": "success",
        "data": {
            "rows": [dxl.to_json() for dxl in DXLooker.query.all()]
        }
    }
    return jsonify(response_object), 200
