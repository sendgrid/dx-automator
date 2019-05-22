# services/tasks/project/api/tasks.py


from flask import Blueprint, jsonify, request, render_template, current_app
from project import db
from sqlalchemy import exc
from project.api.models import Task
from python_http_client import Client
from .priority import Priority
import os
import json
import time

tasks_blueprint = Blueprint('tasks', __name__, template_folder='./templates')

def get_items(repo, item_type):
    client = Client(host=current_app.config['LOCALHOST'])
    query_params = {
        "repo": repo,
        "item_type": item_type,
        "states[]": ['OPEN'],
        "limit[]": ['first', '100']
        }
    response = client.github.items.get(query_params=query_params)
    items = json.loads(response.body)
    return items

@tasks_blueprint.route('/tasks/ping/pong', methods=['GET'])
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

    # TODO: Add the other optional paramaters here
    creator = post_data.get('creator')
    url = post_data.get('url')
    try:
        task = Task.query.filter_by(url=url).first()
        if not task:
            db.session.add(Task(creator=creator, url=url))
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': f'{url} was added!'
            }
            return jsonify(response_object), 201
        else:
            response_object['message'] = 'Sorry. That url already exists.'
            return jsonify(response_object), 400
    except exc.IntegrityError:
        response_object = {
            'status': 'fail',
            'message': current_app.config['ERROR_DB_WRITE_FAILURE']
        }
        db.session.rollback()
        return jsonify(response_object), 400


@tasks_blueprint.route('/tasks/<task_id>', methods=['GET'])
def get_single_task(task_id):
    response_object = {
        'status': 'fail',
        'message': f'task_id {task_id} does not exist'
    }
    try:
        task = Task.query.filter_by(id=int(task_id)).first()
        if not task:
            return jsonify(response_object), 404
        else:
            response_object = {
                'status': 'success',
                'message': {
                    'id': task.id,
                    'url': task.url,
                    'creator': task.creator,
                    'labels': task.labels,
                    'language': task.language,
                    'num_of_comments': task.num_of_comments,
                    'num_of_reactions': task.num_of_reactions,
                    'updated_at': task.updated_at,
                    'updated_locally_at': task.updated_locally_at,
                    'task_type': task.task_type
                }
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


@tasks_blueprint.route('/tasks', methods=['GET'])
def get_all_tasks():
    response_object = {
        'status': 'success',
        'message': {
            'tasks': [task.to_json() for task in Task.query.all()]
        }
    }
    return jsonify(response_object), 200



@tasks_blueprint.route('/tasks/init/db', methods=['GET'])
def populate_db():
    all_repos = current_app.config['REPOS']

    repos = dict()
    for repo in all_repos:
        prs = get_items(repo['name'], 'pull_requests')
        issues = get_items(repo['name'], 'issues')
        items = issues + prs
        repos[repo['name']] = items

    for repo in all_repos:
        if len(repos[repo['name']]) != 0:
            for item in repos[repo['name']]:
                if item != None:
                    task_type = 'pr' if 'pull' in item['url'] else 'issue'
                    try:
                        db.session.add(
                            Task(
                                created_at=item['createdAt'],
                                updated_at=item['updatedAt'],
                                creator=item['author'],
                                labels=item['labels'],
                                language=repo['programming_language'],
                                num_of_comments=item['comments'],
                                num_of_reactions=item['reactions'],
                                title=item['title'],
                                url=item['url'],
                                task_type=task_type
                            )
                        )
                        db.session.commit()
                    except exc.IntegrityError:
                        response_object = {
                            'status': 'fail',
                            'message': current_app.config['ERROR_DB_WRITE_FAILURE']
                        }
                        db.session.rollback()
                        return jsonify(response_object), 400
    response_object = {
        'status': 'success',
        'message': 'DB Initailized'
    }
    return jsonify(response_object), 201

@tasks_blueprint.route('/tasks/rice/<task_id>', methods=['GET'])
def calculate_rice_score(task_id):
    response_object = {
        'status': 'fail',
        'message': f'task_id {task_id} does not exist'
    }
    task = Task.query.filter_by(id=int(task_id)).first()
    if not task:
        return jsonify(response_object), 404
    else:
        priority = Priority()
        elements = {
            'reach': request.args.get('reach', type = float),
            'impact': request.args.get('impact', type = float),
            'confidence': request.args.get('confidence', type = float),
            'effort': request.args.get('effort', type = float),
        }
        rice_score = priority.calculate_priority(elements)
        try:
            task.rice_total = rice_score
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
            response_object = {
                'status': 'fail',
                'message': current_app.config['ERROR_DB_WRITE_FAILURE']
            }
            return jsonify(response_object), 400
        response_object = {
            'status': 'success',
            'message': task.to_json()
        }
        return jsonify(response_object), 200
    

@tasks_blueprint.route('/tasks/rice', methods=['GET'])
def rice_sorted_backlog():
    page_index = request.args.get('page_index', type = int)
    num_results = request.args.get('num_results', type = int) or 20
    
    try:
        if page_index:
            tasks = Task.query.order_by(Task.rice_total.desc()).paginate(page_index, num_results, False).items
        else:
            tasks = Task.query.order_by(Task.rice_total.desc()).all()
    except exc.IntegrityError:
        db.session.rollback()
        response_object = {
            'status': 'fail',
            'message': current_app.config['ERROR_DB_WRITE_FAILURE']
        }
        return jsonify(response_object), 400

    response_object = {
        'status': 'success',
        'message': [task.to_json() for task in tasks]
    }
    
    return jsonify(response_object), 200
