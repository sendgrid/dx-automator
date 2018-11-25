from sqlalchemy import exc
from flask import Blueprint, jsonify, request, render_template

from project.api.models import Hacktoberfest
from project import db


hacktoberfest_blueprint = Blueprint('hacktoberfest', __name__, template_folder='./templates')


@hacktoberfest_blueprint.route('/hacktoberfest/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })

