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

# @looker_blueprint.route("/looker", methods=["POST"])
# def add_user():
#     post_data = request.get_json()
#     response_object = {
#         "status": "fail",
#         "message": "Invalid payload."
#     }
#     if not post_data:
#         return jsonify(response_object), 400
#     username = post_data.get("username")
#     email = post_data.get("email")
#
#     try:
#         user = Looker.query.filter_by(email=email).first()
#         if not user:
#             db.session.add(Looker(username=username, email=email))
#             db.session.commit()
#             response_object["status"] = "success"
#             response_object["message"] = "{} was added!".format(email)
#             return jsonify(response_object), 201
#         else:
#             response_object["message"] = "Sorry. That email already exists."
#             return jsonify(response_object), 400
#     except exc.IntegrityError as e:
#         db.session.rollback()
#         return jsonify(response_object), 400
#
#
# @looker_blueprint.route("/looker/<user_id>", methods=["GET"])
# def get_single_user(user_id):
#     """Get single user details"""
#     response_object = {
#         "status": "fail",
#         "message": "User does not exist"
#     }
#     try:
#         user = Looker.query.filter_by(id=int(user_id)).first()
#         if not user:
#             return jsonify(response_object), 404
#         else:
#             response_object = {
#                 "status": "success",
#                 "data": {
#                     "id": user.id,
#                     "username": user.username,
#                     "email": user.email,
#                     "active": user.active
#                 }
#             }
#             return jsonify(response_object), 200
#     except ValueError:
#         return jsonify(response_object), 404
#
#
# @looker_blueprint.route("/looker", methods=["GET"])
# def get_all_users():
#     """Get all users"""
#     response_object = {
#         "status": "success",
#         "data": {
#             "users": [user.to_json() for user in Looker.query.all()]
#         }
#     }
#     return jsonify(response_object), 200
