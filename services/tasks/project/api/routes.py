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
    client = Client(host="http://{}".format(os.environ.get('DX_IP')))
    query_params = {
        "repo":repo,
        "item_type":item_type,
        "states[]":['OPEN'],
        "limit[]":['first', '100']
        }
    response = client.github.items.get(query_params=query_params)
    items = json.loads(response.body)
    return items  

@tasks_blueprint.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        db.session.add(Task(creator=request.form['creator'],
                       url=request.form['url']))
        db.session.commit()
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)


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
                'data': {
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
        'data': {
            'tasks': [task.to_json() for task in Task.query.all()]
        }
    }
    return jsonify(response_object), 200



@tasks_blueprint.route('/tasks/init/db', methods=['GET'])
def populate_db():
    all_repos = current_app.config['REPOS']

    response_object = dict()
    for repo in all_repos:
        prs = get_items(repo['name'], 'pull_requests')
        issues = get_items(repo['name'], 'issues')
        items = issues + prs
        response_object[repo['name']] = items

    for repo in all_repos:
        if len(response_object[repo['name']]) != 0:
            for issue in response_object[repo['name']]:
                if issue != None:
                    if 'pull' in issue['url']:
                        task_type = 'pr'
                    else:
                        task_type = 'issue'
                    creator = issue['author']
                    url = issue['url']
                    created_at = issue['createdAt']
                    updated_at = issue['updatedAt']
                    labels = issue['labels']
                    num_of_comments = issue['comments']
                    num_of_reactions = issue['reactions']
                    title = issue['title']
                    language = repo['programming_language']
                    try:
                        db.session.add(
                            Task(
                                created_at=created_at,
                                updated_at=updated_at,
                                creator=creator,
                                labels=labels,
                                language=language,
                                num_of_comments=num_of_comments,
                                num_of_reactions=num_of_reactions,
                                title=title,
                                url=url,
                                task_type=task_type
                            )
                        )
                        db.session.commit()
                    except exc.IntegrityError:
                        db.session.rollback()
                        return jsonify(response_object), 400
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
            return jsonify(response_object), 400
        response_object = {
            'status': 'success',
            'data': {
                'id': task.id,
                'url': task.url,
                'creator': task.creator,
                'rice_total': task.rice_total
            }
        }
        return jsonify(response_object), 200
    