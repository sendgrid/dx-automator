from flask import Blueprint, jsonify, current_app, request
import requests
import sys
import json
from .graphql import GraphQL

github_blueprint = Blueprint('github', __name__)

EXCLUSIONS = [
    'aroach',
    'thinkingserious',
    'kylearoberts',
    'childish-sambino',
    'SendGridDX'
]

def get_points(labels):
    for label in labels:
        if label.get('node').get('name') == 'difficulty: easy':
            return 1
        if label.get('node').get('name')  == 'difficulty: medium':
            return 3
        if label.get('node').get('name')  == 'difficulty: hard':
            return 7
        if label.get('node').get('name')  == 'difficulty: very hard':
            return 15 
    return 0

def get_labels(labels):
    l = []
    for label in labels:
        l.append(label.get('node').get('id'))
    return l

def get_reviewers(reviewers, author):
    logins = list()
    for reviewer in reviewers:
        if (reviewer.get('author').get('login') != author) and (reviewer.get('author').get('login') not in EXCLUSIONS):
            logins.append(reviewer.get('author').get('login'))
    return list(set(logins))

@github_blueprint.route('/github/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })

@github_blueprint.route('/github/is_member/<username>', methods=['GET'])
def is_member(username):
    """Check if user is a member of your GitHub organization"""
    github_org = current_app.config['GITHUB_ORG']
    username = '"' + username + '"'
    query = f"""query {{
        user(login:{username}){{
            organization(login:{github_org}) {{
                name
            }}
        }}
    }}"""
    is_member = False
    if username not in current_app.config.get('EXCEPTIONS'):
        result, status = GraphQL.run_query(query)
        if status:
            if (result is not None and result.get('user') and
                    result.get('user').get('organization')):
                is_member = True
        else:
            return "GITHUB_TOKEN may not be valid", 400
    else:
        is_member = True
    response_object = {
        'is_member': is_member
    }
    status_code = 200 if is_member else 404
    return jsonify(response_object), status_code


@github_blueprint.route('/github/members', methods=['GET'])
def get_all_members():
    """Get all the members from your Github organization"""
    members = list()
    end_cursor = ''
    has_next_page = True
    github_org = current_app.config['GITHUB_ORG']
    while has_next_page:
        query = f"""query{{
            organization(login: {github_org}){{
                members(first: 100 after: {end_cursor}){{
                    nodes{{
                        login
                    }}
                    pageInfo{{
                        endCursor
                        hasNextPage
                    }}
                }}
            }}
            }}"""
        result, status = GraphQL.run_query(query)
        if not status:
            return "GITHUB_TOKEN may not be valid", 400
        elif result:
            result = result.get('organization').get('members')
            for member in result.get('nodes'):
                members.append(member.get('login'))
            has_next_page = result.get('pageInfo').get('hasNextPage')
            if has_next_page == True:
                end_cursor = f'"{result["pageInfo"]["endCursor"]}"'
        else:
            break
    return jsonify(members), 200

@github_blueprint.route('/github/items', methods=['GET'])
def get_items():
    items = list()
    labels = list()
    states = list()
    limit = list()
    list_of_limits = request.args.getlist('limit[]', type = str)
    for limits in list_of_limits:
        try:
            limit.append(limits)
        except Exception:
            continue
    limit = (limit[0], int(limit[1]))
    item_type = request.args.get('item_type', type = str)
    if item_type == 'pull_requests':
       item_type = 'pullRequests'
    repo = request.args.get('repo', type = str)
    list_of_labels = request.args.getlist('labels[]', type = str)
    for label in list_of_labels:
        try:
            labels.append(label)
        except Exception:
            continue
    list_of_states = request.args.getlist('states[]', type = str)
    for state in list_of_states:
        try:
            states.append(state)
        except:
            continue
    if not states:
        states.append('OPEN')
        #states.append('MERGED')
        #states.append('CLOSED')
    end_cursor = ''
    has_next_page = True
    github_org = current_app.config['GITHUB_ORG']
    while has_next_page:
        query = GraphQL(
            organization=github_org,
            github_type=item_type,
            repo=repo,
            states=states,
            labels=labels,
            limit=limit,
            end_cursor=end_cursor
        )
        print(query.__str__())
        result, status = GraphQL.run_query(query.__str__())
        if not status:
            return "GITHUB_TOKEN may not be valid", 400
        elif result:
            result = result.get('organization').get('repository').get(item_type)
            for r in result.get('nodes'):
                item = dict()
                last_comment_author = None
                try:
                    for comment in r.get('comments').get('nodes'):
                        last_comment_author = comment.get('author').get('login')
                    item['comments'] = r.get('comments').get('totalCount')
                except:
                    last_comment_author = None
                    item['comments'] = 0
                item['url'] = r.get('url')
                item['createdAt'] = r.get('createdAt')
                try:
                    item['author'] = r.get('author').get('login')
                except Exception:
                    item['author'] = 'unknown'
                try:
                    item['labels'] = get_labels(r.get('labels').get('edges'))
                    item['points'] = get_points(r.get('labels').get('edges'))
                except Exception:
                    item['labels'] = None
                    item['points'] = 0
                try:
                    reviews = r.get('reviews').get('nodes')
                    item['reviewers'] = get_reviewers(reviews, pr['author'])
                    item['num_reviewers'] = len(pr['reviewers'])
                    item['reviewer_points'] = len(pr['reviewers']) * (pr['points'] / 2)
                except Exception:
                    item['reviewers'] = None
                    item['num_reviewers'] = 0
                    item['reviewer_points'] = 0
                try:
                    item['reactions'] = r.get('reactions').get('totalCount')
                except Exception:
                    item['reactions'] = 0
                item['last_comment_author'] = last_comment_author
                item['title'] = r.get('title')
                items.append(item)
            has_next_page = result.get('pageInfo').get('hasNextPage')
            if has_next_page == True:
                end_cursor = result.get('pageInfo').get('endCursor')
        else:
            break
    return jsonify(items), 200

