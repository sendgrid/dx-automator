from flask import Blueprint, jsonify, current_app, request
import requests
import sys
import json

github_blueprint = Blueprint('github', __name__)

EXCLUSIONS = [
    'thinkingserious', 'ksigler7', 'Whatthefoxsays'
]

def run_query(query):
    """Runs GraphQL query"""
    url = "https://api.github.com/graphql"
    github_token = current_app.config['GITHUB_TOKEN']
    headers = {
        "Authorization": f"bearer {github_token}"
    }
    response = requests.post(url, json={'query': query}, headers=headers)
    if response.ok:
        return response.json().get('data'), response.ok
    return None, response.ok

  
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
        result, status = run_query(query)
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
        result, status = run_query(query)
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

# labels must be a list of strings
# TODO: should be able to select from a date range
@github_blueprint.route('/github/prs', methods=['GET'])
def get_prs():
    """Get all of the PRs with a given list of labels from a particular repo"""
    prs = list()
    labels = list()
    states = list()
    repo = request.args.get('repo', type = str)
    list_of_labels = request.args.getlist('labels', type = str)
    for label in list_of_labels:
        try:
            labels.append(label)
        except:
            continue
    list_of_states = request.args.getlist('states', type = str)
    for state in list_of_states:
        try:
            states.append(state)
        except:
            continue
    if not states:
        states.append('OPEN')
        states.append('MERGED')
        states.append('CLOSED')
    
    end_cursor = ''
    has_next_page = True
    github_org = current_app.config['GITHUB_ORG']
    repo = '"' + repo + '"'
    while has_next_page:
        query = f"""query{{
            organization(login: "{github_org}") {{
                repository(name: {repo}) {{
                pullRequests(first: 100, states: {json.dumps(states).replace('"', '')}, labels: {json.dumps(labels)}, after: {end_cursor}) {{
                    nodes {{
                        url
                        state
                        createdAt
                        reviews(first: 10) {{
                            nodes {{
                                author {{
                                    login
                                }}
                            }}
                        }}
                        author {{
                            login
                        }}
                        labels(first: 10) {{
                            edges {{
                                node {{
                                    name
                                }}
                            }}
                        }}
                        comments(last: 1) {{
                                nodes {{
                                    author {{
                                        login
                                    }}
                                }}
                            }}
                        }}
                        pageInfo {{
                            endCursor
                            hasNextPage
                        }}
                    }}
                }}
            }}
        }}"""
        result, status = run_query(query)
        if not status:
            return "GITHUB_TOKEN may not be valid", 400
        elif result:
            result = result.get('organization').get('repository').get('pullRequests')
            for r in result.get('nodes'):
                login = None
                for comment in r.get('comments').get('nodes'):
                    login = comment.get('author').get('login')
                pr = dict()
                pr['url'] = r.get('url')
                pr['createdAt'] = r.get('createdAt')
                pr['author'] = r.get('author').get('login')
                pr['points'] = get_points(r.get('labels').get('edges'))
                pr['reviewers'] = get_reviewers(r.get('reviews').get('nodes'), pr['author'])
                pr['reviewer_points'] = len(pr['reviewers']) * (pr['points'] / 2)
                pr['last_comment_author'] = login
                prs.append(pr)
            has_next_page = result.get('pageInfo').get('hasNextPage')
            if has_next_page == True:
                end_cursor = f'"{result["pageInfo"]["endCursor"]}"'
        else:
            break
    return jsonify(prs), 200 

# labels must be a list of strings
# TODO: should be able to select from a data range
@github_blueprint.route('/github/issues', methods=['GET'])
def get_issues():
    """Get all of the open issues with a given list of labels from a particular repo, if no labels
       are given, you will receive a list of unlabeled issues"""
    issues = list()
    labels = list()
    repo = request.args.get('repo', type = str)
    list_of_labels = request.args.getlist('labels', type = str)
    for label in list_of_labels:
        #print(label, file=sys.stderr)
        try:
            labels.append(label)
        except:
            continue
    end_cursor = ''
    has_next_page = True
    github_org = current_app.config['GITHUB_ORG']
    repo = '"' + repo + '"'
    while has_next_page:
        if labels:
            query = f"""query{{
                organization(login: "{github_org}") {{
                    repository(name: {repo}) {{
                    issues(first: 100, labels: {json.dumps(labels)}, states: [OPEN], after: {end_cursor}) {{
                        nodes {{
                            url
                            state
                            createdAt
                            author {{
                                login
                            }}
                            labels(first: 10) {{
                                edges {{
                                    node {{
                                        name
                                    }}
                                }}
                            }}
                            comments(last: 1) {{
                                nodes {{
                                    author {{
                                        login
                                    }}
                                }}
                            }}
                            }}
                            pageInfo {{
                                endCursor
                                hasNextPage
                            }}
                        }}
                    }}
                }}
            }}"""
            result, status = run_query(query)
        else:
            query = f"""query{{
                organization(login: "{github_org}") {{
                    repository(name: {repo}) {{
                    issues(first: 100, states: [OPEN], after: {end_cursor}) {{
                        nodes {{
                            url
                            state
                            createdAt
                            author {{
                                login
                            }}
                            labels(first: 1) {{
                                edges {{
                                    node {{
                                        name
                                    }}
                                }}
                            }}
                            comments(last: 1) {{
                                nodes {{
                                    author {{
                                        login
                                    }}
                                }}
                            }}
                            }}
                            pageInfo {{
                                endCursor
                                hasNextPage
                            }}
                        }}
                    }}
                }}
            }}"""
            result, status = run_query(query)
        if not status:
            return "GITHUB_TOKEN may not be valid", 400
        elif result:
            result = result.get('organization').get('repository').get('issues')
            for r in result.get('nodes'):
                login = None
                for comment in r.get('comments').get('nodes'):
                    login = comment.get('author').get('login')
                if not labels:
                    if not r.get('labels').get('edges'):
                        issue = dict()
                        issue['url'] = r.get('url')
                        issue['createdAt'] = r.get('createdAt')
                        issue['labels'] = labels
                        issue['last_comment_author'] = login
                        issues.append(issue)
                else:
                    issue = dict()
                    issue['url'] = r.get('url')
                    issue['createdAt'] = r.get('createdAt')
                    issue_labels = list()
                    for label in r.get('labels').get('edges'):
                        issue_labels.append(label.get('node').get('name'))
                    issue['labels'] = issue_labels
                    issue['last_comment_author'] = login
                    issues.append(issue)
            has_next_page = result.get('pageInfo').get('hasNextPage')
            if has_next_page == True:
                end_cursor = f'"{result["pageInfo"]["endCursor"]}"'
        else:
            break
    return jsonify(issues), 200 

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

def get_reviewers(reviewers, author):
    logins = list()
    for reviewer in reviewers:
        if (reviewer.get('author').get('login') != author) and (reviewer.get('author').get('login') not in EXCLUSIONS):
            logins.append(reviewer.get('author').get('login'))
    return list(set(logins))
