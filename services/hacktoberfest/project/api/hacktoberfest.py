from sqlalchemy import func, extract, exc
from flask import Blueprint, jsonify, request, render_template

from project.api.models import Hacktoberfest, Swag
from project.api.utils.response import response_json_bad_request
from project import db

from python_http_client import Client
import json
import os
from collections import defaultdict

all_repos = [
    'sendgrid-nodejs',
    'sendgrid-csharp',
    'sendgrid-php',
    'sendgrid-python',
    'sendgrid-java',
    'sendgrid-go',
    'sendgrid-ruby',
    'smtpapi-nodejs',
    'smtpapi-go',
    'smtpapi-python',
    'smtpapi-php',
    'smtpapi-csharp',
    'smtpapi-java',
    'smtpapi-ruby',
    'sendgrid-oai',
    'open-source-library-data-collector',
    'python-http-client',
    'php-http-client',
    'csharp-http-client',
    'java-http-client',
    'ruby-http-client',
    'rest',
    'nodejs-http-client',
    'dx-automator',
    'dx-mobile',
    'ui-components',
    'docs'
]

hacktoberfest_blueprint = Blueprint('hacktoberfest', __name__, template_folder='./templates')

def get_prs(repo):
    client = Client(host="http://{}".format(os.environ.get('DX_IP')))
    query_params = {"repo":repo, "labels":"status: hacktoberfest approved"}
    response = client.github.prs.get(query_params=query_params)
    prs = json.loads(response.body)
    return prs

@hacktoberfest_blueprint.route('/hacktoberfest/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })

@hacktoberfest_blueprint.route('/hacktoberfest/sendgrid/leaders/<int:year>', methods=['GET'])
def hacktoberfest_sendgrid_leaders(year):
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

@hacktoberfest_blueprint.route('/hacktoberfest/leaders/update', methods=['GET'])
def hacktoberfest_leaders_update():
    points_earned = defaultdict(int)
    for repo in all_repos:
        prs = get_prs(repo)
        for pr in prs:
            num_reviewers = len(pr['reviewers'])
            if num_reviewers > 0:
                for reviewer in pr['reviewers']:
                    points_earned[reviewer] += pr['points'] / 2
            points_earned[pr['author']] += pr['points']

    sorted_points_earned = [(k, points_earned[k]) for k in sorted(points_earned, key=points_earned.__getitem__, reverse=True)]
    for author, points in sorted_points_earned:
        try:
            leader = Hacktoberfest.query.join(Swag).filter(Swag.github_username == author).first()
            if leader:
                leader.total_points = int(points)
                leader.update()
        except exc.IntegrityError as e:
            return response_json_bad_request(jsonify(e))
    
    return jsonify(sorted_points_earned), 200
