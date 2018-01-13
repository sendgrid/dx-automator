from flask import Blueprint, jsonify, request

from project.api.models import Item_Status
from project import db

from sqlalchemy import exc

items_statuses_blueprint = Blueprint('items_statuses', __name__)

@items_statuses_blueprint.route('/item_statuses', methods=['POST'])
def add_item_status():
    post_data = request.get_json()
    if not post_data:
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400
    name = post_data.get('name')
    value = post_data.get('value')
    value_type = post_data.get('value_type')

    if not name:
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400

    if not value:
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400

    if not value_type:
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400


    try:
        Item_Status.query.filter_by(name=name).first()
        item_status = Item_Status.query.filter_by(name=name).first()

        if not item_status:
            item_status = db.session.add(Item_Status(name=name, value=value, value_type=value_type))
            db.session.commit()
            item_status = Item_Status.query.filter_by(name=name).first()
            response_object = {
                'status': 'success',
                'message': '{} was added!'.format(name),
                'data': {
                    'id': item_status.id,
                    'name': item_status.name,
                    'value': item_status.value,
                    'value_type': item_status.value_type,
                    'created_at': item_status.created_at,
                    'updated_at': item_status.updated_at
                }
            }
            return jsonify(response_object), 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'Sorry. That item status already exists.'
            }
            return jsonify(response_object), 400
    except exc.IntegrityError as e:
        db.session.rollback()
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400


@items_statuses_blueprint.route('/item_statuses/<item_status_id>', methods=['GET'])
def get_single_item_status(item_status_id):
    """Get single item status details"""
    response_object = {
        'status': 'fail',
        'message': 'Item status does not exist'
    }
    try:
        item_status = Item_Status.query.filter_by(id=int(item_status_id)).first()
        if not item_status:
            return jsonify(response_object), 404
        else:
            response_object = {
                'status': 'success',
                'data': {
                    'id' : item_status_id,
                    'name': item_status.name,
                    'value': item_status.value,
                    'value_type': item_status.value_type,
                    'created_at': item_status.created_at,
                    'updated_at': item_status.updated_at
                }
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


@items_statuses_blueprint.route('/item_statuses', methods=['GET'])
def get_all_item_statuses():
    """Get all item statuses"""
    items_statuses = Item_Status.query.all()
    item_status_list = []
    for item_status in items_statuses:
        item_status_object = {
            'id': item_status.id,
            'name': item_status.name,
            'value': item_status.value,
            'value_type': item_status.value_type,
            'created_at': item_status.created_at,
            'updated_at': item_status.updated_at
        }
        item_status_list.append(item_status_object)
    response_object = {
        'status': 'success',
        'data': {
            'item_statuses': item_status_list
        }
    }
    return jsonify(response_object), 200

@items_statuses_blueprint.route('/item_statuses/<item_status_id>', methods=['PATCH'])
def edit_single_item_status():
    """Edit a single todo item"""
