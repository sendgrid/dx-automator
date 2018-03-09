from flask import Blueprint, jsonify, request

from project.api.models import User
from project import db

from sqlalchemy import exc

users_blueprint = Blueprint('users', __name__)


@users_blueprint.route('/ping_user', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })



@users_blueprint.route('/users', methods=['POST'])
def add_user():
    post_data = request.get_json()
    if not post_data:
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400

    github_username = post_data.get('github_username')
    email_address = post_data.get('email_address')
    twitter_username = post_data.get('twitter_username')

    if not github_username:
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload. `github_username` param is required.'
        }
        return jsonify(response_object), 400
    
    if not email_address:
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload. `email_address` param is required.'
        }
        return jsonify(response_object), 400

    try:
        user = User.query.filter_by(github_username=github_username,
                                    email_address=email_address,
                                    twitter_username=twitter_username).first()
        if not user:
            user_id = db.session.add(User(github_username=github_username,
                                          email_address=email_address,
                                          twitter_username=twitter_username))
            db.session.commit()
            user = User.query.filter_by(github_username=github_username).first()
            response_object = {
                'status': 'success',
                'message': '{} was added!'.format(github_username),
                'data' : {
                    'id': user.id,
                    'github_username': user.github_username,
                    'email_address' : user.email_address,
                    'twitter_username': user.twitter_username,
                    'created_at': user.created_at,
                    'updated_at': user.updated_at
                }
            }
            return jsonify(response_object), 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'Sorry. That user already exists.'
            }
            return jsonify(response_object), 400
    except exc.IntegrityError as e:
        db.session.rollback()
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400
