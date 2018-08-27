# services/tasks/project/api/tasks.py


from flask import Blueprint, jsonify, request
from project import db
from sqlalchemy import exc
from project.api.models import Task


tasks_blueprint = Blueprint('tasks', __name__)


@tasks_blueprint.route('/tasks/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
})

@tasks_blueprint.route('/tasks', methods=['POST'])
def add_single_task():
    post_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    if not post_data:
        return jsonify(response_object), 400
    creator = post_data.get('creator')
    link = post_data.get('link')
    try:
        task = Task.query.filter_by(link=link).first()
        if not task:
            db.session.add(Task(creator=creator, link=link))
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': f'{link} was added!'
            }
            return jsonify(response_object), 201
        else:
            response_object['message'] = 'Sorry. That link already exists.'
            return jsonify(response_object), 400
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify(response_object), 400

@tasks_blueprint.route('/tasks/<task_id>', methods=['GET'])
def get_single_task(task_id):
    response_object = {
        'status': 'fail',
        'message': 'task does not exist'
    }
    try:
        task = Task.query.filter_by(id=int(task_id)).first()
        if not task:
            return jsonify(response_object), 404
        else:
            response_object = {
                'status': 'success',
                'data': {
                    'id': task.id,
                    'link': task.link,
                    'creator': task.creator
                }
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404

@tasks_blueprint.route('/tasks', methods=['GET'])
def get_all_tasks():
    response_object = {
        'status': 'success',
        'data': {
            'tasks': [task.to_json() for task in Task.query.all()]
        }
    }
    return jsonify(response_object), 200
    
