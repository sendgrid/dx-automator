from flask import Blueprint, jsonify, current_app
from github3 import login

github_blueprint = Blueprint('github', __name__)

@github_blueprint.route('/github/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })

@github_blueprint.route('/github/is_member/<username>', methods=['GET'])
def is_member(username):
    """Check if user is a member of your GitHub organization"""
    github_token = current_app.config['GITHUB_TOKEN']
    github = login(token=github_token)
    try:
        org = github.organization(current_app.config['GITHUB_ORG'])
        is_member = org.is_member(username)
        if not is_member:
            is_member = True if username in current_app.config['EXCEPTIONS'] else False
        response_object = {
            'is_member': is_member
        }
        status_code = 200 if is_member else 404
        return jsonify(response_object), status_code
    except AttributeError:
        return "GITHUB_TOKEN may not be valid", 400


@github_blueprint.route('/github/members', methods=['GET'])
def get_all_members():
    """Get all the members from your Github organization"""
    members = []
    github_token = current_app.config['GITHUB_TOKEN']
    github = login(token=github_token)
    try:
        org = github.organization(current_app.config['GITHUB_ORG'])
        for member in org.iter_members():
            members.append(member.login)
        members = jsonify(members)
        status_code = 200
        return members, status_code
    except AttributeError:
        status_code = 400
        return "GITHUB_TOKEN may not be valid", status_code
