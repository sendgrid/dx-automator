from flask import Blueprint, jsonify, current_app
from github3 import login

github_blueprint = Blueprint('github', __name__)

@github_blueprint.route('/is_a_member/<username>', methods=['GET'])
def is_a_member(username):
    """Check if user is a member of your GitHub organization"""
    github_token = current_app.config['GITHUB_TOKEN']
    github = login(token=github_token)
    org = github.organization(current_app.config['GITHUB_ORG'])
    is_member = org.is_member(username)
    if not is_member:
        is_member = True if username in current_app.config['EXCEPTIONS'] else False
    response_object = {
        'is_member': is_member
    }
    status_code = 200 if is_member else 404
    return jsonify(response_object), status_code
