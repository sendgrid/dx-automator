from flask import Blueprint, jsonify, request

from project.api.models import Item
from project import db

from sqlalchemy import exc

items_blueprint = Blueprint('items', __name__)


@items_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


@items_blueprint.route('/items', methods=['POST'])
def add_item():
    post_data = request.get_json()
    if not post_data:
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400

    subject = post_data.get('subject')
    url = post_data.get('url')
    requestor = post_data.get('requestor')

    if not url:
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload. `url` param is required.'
        }
        return jsonify(response_object), 400
    
    if not subject:
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload. `subject` param is required.'
        }
        return jsonify(response_object), 400

    if not requestor:
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload. `requestor` param is required.'
        }
        return jsonify(response_object), 400

    try:
        item = Item.query.filter_by(url=url).first()
        if not item:
            item_id = db.session.add(Item(subject=subject, url=url, requestor=requestor))
            db.session.commit()
            item = Item.query.filter_by(url=url).first()
            response_object = {
                'status': 'success',
                'message': '{} was added!'.format(subject),
                'data' : {
                    'id': item.id,
                    'subject': item.subject,
                    'status' : item.status,
                    'url': item.url,
                    'requestor': item.requestor,
                    'maintainer': item.maintainer,
                    'created_at': item.created_at,
                    'updated_at': item.updated_at,
                    'due_date': item.due_date
                }
            }
            return jsonify(response_object), 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'Sorry. That item already exists.'
            }
            return jsonify(response_object), 400
    except exc.IntegrityError as e:
        db.session.rollback()
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400


@items_blueprint.route('/items/<item_id>', methods=['GET'])
def get_single_item(item_id):
    """Get single item details"""
    response_object = {
        'status': 'fail',
        'message': 'Item does not exist'
    }
    try:
        item = Item.query.filter_by(id=int(item_id)).first()
        if not item:
            return jsonify(response_object), 404
        else:
            response_object = {
                'status': 'success',
                'data': {
                    'id': item.id,
                    'subject': item.subject,
                    'status' : item.status,
                    'url': item.url,
                    'requestor': item.requestor,
                    'maintainer': item.maintainer,
                    'created_at': item.created_at,
                    'updated_at': item.updated_at,
                    'due_date': item.due_date
                }
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


@items_blueprint.route('/items', methods=['GET'])
def get_all_items():
    """Get all items"""
    items = Item.query.all()
    items_list = []
    for item in items:
        item_object = {
            'id': item.id,
            'subject': item.subject,
            'status' : item.status,
            'url': item.url,
            'requestor': item.requestor,
            'maintainer': item.maintainer,
            'created_at': item.created_at,
            'updated_at': item.updated_at,
            'due_date': item.due_date
        }
        items_list.append(item_object)
    response_object = {
        'status': 'success',
        'data': {
            'items': items_list
        }
    }
    return jsonify(response_object), 200


@items_blueprint.route('/items/<item_id>', methods=['PATCH'])
def edit_single_item():
    """Edit a single todo item"""
    post_data = request.get_json()
    if not post_data:
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400

    try:
        item = Item.query.filter_by(id=int(item_id)).first()
        if not item:
            response_object = {
                'status': 'fail',
                'message': 'Sorry. That github item already exists.'
            }
            return jsonify(response_object), 400
        else:
            item_orig = item.copy()
            subject = post_data.get('subject')
            status = post_data.get('status')
            url = post_data.get('url')
            requestor = post_data.get('requestor')
            maintainer = post_data.get('maintainer')

            if subject:
                item.subject = subject
            
            if url:
                item.url = url

            if status:
                item.status = status
            
            if requestor:
                item.requestor = requestor
            
            if maintainer:
                item.maintainer = maintainer

            if item_orig != item:
                db.session.commit()
                response_object = {
                    'status': 'success',
                    'message': '{} was updated!'.format(subject),
                    'data' : {
                        'id': item.id,
                        'subject': item.subject,
                        'status' : item.status,
                        'url': item.url,
                        'requestor': item.requestor,
                        'maintainer': item.maintainer,
                        'created_at': item.created_at,
                        'updated_at': item.updated_at,
                        'due_date': item.due_date
                    }
                }
                return jsonify(response_object), 201
            else:
                response_object = {
                    'status': 'not modified',
                    'message': '{} was not modified.'.format(subject),
                    'data' : {
                        'id': item.id,
                        'subject': item.subject,
                        'status' : item.status,
                        'url': item.url,
                        'requestor': item.requestor,
                        'maintainer': item.maintainer,
                        'created_at': item.created_at,
                        'updated_at': item.updated_at,
                        'due_date': item.due_date
                    }
                }
                return jsonify(response_object), 304

    except exc.IntegrityError as e:
        db.session.rollback()
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400
