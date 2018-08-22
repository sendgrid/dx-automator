from flask import Blueprint, jsonify, request
from sqlalchemy import exc

from project.api.models import Looker
from project import db

looker_blueprint = Blueprint("looker", __name__)


@looker_blueprint.route("/looker/ping", methods=["GET"])
def ping_pong():
    return jsonify({
        "status": "success",
        "message": "pong"
    })


@looker_blueprint.route("/looker", methods=["POST"])
def add_user():
    post_data = request.get_json()
    response_object = {
        "status": "fail",
        "message": "Invalid payload."
    }
    if not post_data:
        return jsonify(response_object), 400
    username = post_data.get("username")
    email = post_data.get("email")

    try:
        user = Looker.query.filter_by(email=email).first()
        if not user:
            db.session.add(Looker(username=username, email=email))
            db.session.commit()
            response_object["status"] = "success"
            response_object["message"] = "{} was added!".format(email)
            return jsonify(response_object), 201
        else:
            response_object["message"] = "Sorry. That email already exists."
            return jsonify(response_object), 400
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify(response_object), 400


@looker_blueprint.route("/looker/<user_id>", methods=["GET"])
def get_single_user(user_id):
    """Get single user details"""
    response_object = {
        "status": "fail",
        "message": "User does not exist"
    }
    try:
        user = Looker.query.filter_by(id=int(user_id)).first()
        if not user:
            return jsonify(response_object), 404
        else:
            response_object = {
                "status": "success",
                "data": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "active": user.active
                }
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


@looker_blueprint.route("/looker", methods=["GET"])
def get_all_users():
    """Get all users"""
    response_object = {
        "status": "success",
        "data":{
            "users": [user.to_json() for user in Looker.query.all()]
        }
    }
    return jsonify(response_object), 200
