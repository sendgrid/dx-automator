from flask import Blueprint, jsonify, current_app
import requests

github_blueprint = Blueprint('github', __name__)


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
        print("Iteration ")
        query = f"""query{{
            organization(login: {github_org}){{
                members(first: 50 after: {end_cursor}){{
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
