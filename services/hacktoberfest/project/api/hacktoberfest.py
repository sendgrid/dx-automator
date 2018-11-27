from sqlalchemy import func, extract
from flask import Blueprint, jsonify, request, render_template

from project.api.models import Hacktoberfest, Swag
from project import db


hacktoberfest_blueprint = Blueprint('hacktoberfest', __name__, template_folder='./templates')


@hacktoberfest_blueprint.route('/hacktoberfest/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })

@hacktoberfest_blueprint.route('/hacktoberfest/sendgrid/leaders/<int:year>')
def hacktoberfest(year):
    leaders = Hacktoberfest.query \
            .filter(extract('year', Hacktoberfest.time_logged) == str(year)) \
            .filter(Hacktoberfest.hacktoberfest_approved == True) \
            .filter(Hacktoberfest.sendgrid_employee == True) \
            .join(Swag).filter(Swag.github_username != 'SendGridDX') \
            .filter(Swag.github_username != 'thinkingserious') \
            .filter(Swag.github_username != 'Whatthefoxsays') \
            .filter(Swag.github_username != 'ksigler7') \
            .order_by(Hacktoberfest.total_points.desc()).all()
    hacktoberfest_sendgrid_leaders = []
    hacktoberfest_sendgrid_leader = {}
    for leader in leaders:
        hacktoberfest_sendgrid_leader['github_username'] = leader.swag.github_username
        hacktoberfest_sendgrid_leader['total_points'] = leader.total_points
        hacktoberfest_sendgrid_leader['year_swag_sent'] = leader.hacktoberfest_swag_sent
        hacktoberfest_sendgrid_leaders.append(hacktoberfest_sendgrid_leader)
        hacktoberfest_sendgrid_leader = {}
    return jsonify(hacktoberfest_sendgrid_leaders), 200
