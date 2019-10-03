from flask import Blueprint, jsonify, current_app, request
from .graphql import GraphQL

github_blueprint = Blueprint('github', __name__)

MAINTAINERS = {
    'eshanholtz',
    'thinkingserious',
    'kylearoberts',
    'childish-sambino',
    'krantikt',
    'SendGridDX',
    'codecov'
}

DIFFICULTY_POINTS = {
    'difficulty: easy': 1,
    'difficulty: medium': 3,
    'difficulty: hard': 7,
    'difficulty: very hard': 15,
}


def get_points(labels):
    for label in get_labels(labels):
        if label in DIFFICULTY_POINTS:
            return DIFFICULTY_POINTS[label]
    return 0


def get_labels(labels):
    all_labels = [label.get('node').get('name') for label in labels]
    return all_labels


def get_reviewers(reviewers, author):
    logins = [reviewer.get('author').get('login') for reviewer in reviewers]
    logins = [reviewer for reviewer in logins if reviewer != author and reviewer not in MAINTAINERS]
    return list(set(logins))


def get_author(item):
    return (item['author'] or {}).get('login')


def is_follow_up_needed(item):
    author = get_author(item)
    comments = item['comments'].get('nodes') or None
    follow_up_needed = author not in MAINTAINERS

    if follow_up_needed and comments:
        last_comment = comments[-1]
        last_comment_author = get_author(last_comment)
        thumbs_up_logins = [reaction.get('user').get('login')
                            for reaction in last_comment.get('reactions').get('nodes')
                            if reaction.get('content') == 'THUMBS_UP']
        follow_up_needed = bool(last_comment_author not in MAINTAINERS and
                                not set(thumbs_up_logins) & MAINTAINERS)

    return follow_up_needed


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
    member = False
    if username not in current_app.config.get('EXCEPTIONS'):
        result, status = GraphQL.run_query(query)
        if status:
            if (result is not None and result.get('user') and
                result.get('user').get('organization')):
                member = True
        else:
            return "GITHUB_TOKEN may not be valid", 400
    else:
        member = True
    response_object = {
        'is_member': member
    }
    status_code = 200 if member else 404
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
            if result.get('pageInfo').get('hasNextPage'):
                end_cursor = result.get('pageInfo').get('endCursor')
        else:
            break
    return jsonify(members), 200


@github_blueprint.route('/github/items', methods=['GET'])
def get_items():
    items = list()
    labels = list()
    states = list()
    limit = list()
    list_of_limits = request.args.getlist('limit[]', type=str)
    for limits in list_of_limits:
        if limits:
            limit.append(limits)
    limit = (limit[0], int(limit[1]))
    item_type = request.args.get('item_type', type=str)
    org = request.args.get('org', type=str, default=current_app.config['GITHUB_ORG'])
    repo = request.args.get('repo', type=str)
    list_of_labels = request.args.getlist('labels[]', type=str)
    for label in list_of_labels:
        if label:
            labels.append(label)
    list_of_states = request.args.getlist('states[]', type=str)
    for state in list_of_states:
        try:
            states.append(state)
        except:
            continue
    if not states:
        states.append('OPEN')
        states.append('CLOSED')
    end_cursor = ''
    has_next_page = True
    github_type = 'pullRequests' if item_type == 'pull_requests' else item_type

    while has_next_page:
        query = GraphQL(
            github_type=github_type,
            organization=org,
            repo=repo,
            states=states,
            labels=labels,
            limit=limit,
            end_cursor=end_cursor
        )
        result, status = GraphQL.run_query(query.__str__())
        if not status:
            return "GITHUB_TOKEN may not be valid", 400
        elif result:
            result = result.get('organization').get('repository').get(github_type)
            for r in result.get('nodes'):
                item = {
                    'url': r.get('url'),
                    'title': r.get('title'),
                    'createdAt': r.get('createdAt'),
                    'updatedAt': r.get('updatedAt'),
                    'author': get_author(r) or 'unknown',
                    'num_reactions': r.get('reactions').get('totalCount') or 0,
                    'num_comments': r.get('comments').get('totalCount') or 0,
                    'follow_up_needed': is_follow_up_needed(r),
                    'labels': None,
                    'num_labels': 0,
                    'points': 0,
                    'reviewers': None,
                    'num_reviewers': 0,
                    'reviewer_points': 0
                }

                if r.get('labels'):
                    item['labels'] = get_labels(r.get('labels').get('edges'))
                    item['num_labels'] = len(item['labels'])
                    item['points'] = get_points(r.get('labels').get('edges'))
                
                if r.get('reviews'):
                    reviews = r.get('reviews').get('nodes')
                    if len(reviews) == 0:
                        item['reviewers'] = get_reviewers(reviews, item['author'])
                        item['num_reviewers'] = len(item['reviewers'])
                        item['reviewer_points'] = len(item['reviewers']) * (item['points'] / 2)

                items.append(item)
            has_next_page = result.get('pageInfo').get('hasNextPage') or None
            if has_next_page:
                end_cursor = result.get('pageInfo').get('endCursor') or None
        else:
            break
    return jsonify(items), 200

@github_blueprint.route('/github/releases', methods=['GET'])
def get_releases():
    """Retrieve a list of release tags from a given repo"""
    releases = list()
    has_next_page = True
    end_cursor = ''
    org = request.args.get('org', type=str, default=current_app.config['GITHUB_ORG'])
    repo = request.args.get('repo', type=str)
    github_org = current_app.config['GITHUB_ORG']
    while has_next_page:
        query = f"""query Repositories {{
            repository(owner: "{org}", name: "{repo}") {{
                nameWithOwner
                releases(first: 100, orderBy: {{field:CREATED_AT, direction:DESC}}{end_cursor}) {{
                    totalCount
                    nodes {{
                        releaseAssets(first: 1) {{
                            nodes {{
                                name
                                downloadCount
                                createdAt
                            }}
                        }}
                        createdAt
                        tagName
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
            result = result.get('repository').get('releases')
            for r in result.get('nodes'):
                release = {
                    'repo': repo,
                    'tag_name': r.get('tagName'),
                    'created_at': r.get('createdAt')
                }
                releases.append(release)
            has_next_page = result.get('pageInfo').get('hasNextPage')
            if has_next_page:
                end_cursor = ', after: {}'.format(result.get('pageInfo').get('endCursor'))
            
    return jsonify(releases), 200