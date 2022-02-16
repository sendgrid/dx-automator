import json
import os
import re
from typing import Iterator, Dict

import requests

GRAPH_QL_URL = 'https://api.github.com/graphql'


def submit_graphql_query(query: str) -> Iterator[Dict]:
    github_token = os.environ['GITHUB_TOKEN']
    headers = {'Authorization': f'token {github_token}'}
    cursor = None

    while True:
        paged_query = substitute(query, {'cursor': f'after: "{cursor}"' if cursor else ''})

        response = requests.post(GRAPH_QL_URL, json={'query': paged_query}, headers=headers)
        response.raise_for_status()
        response = response.json()

        if 'data' not in response:
            print(json.dumps(response, indent=2))

        search = response['data']['search']
        for node in search['nodes']:
            yield node

        page_info = search['pageInfo']
        cursor = page_info['endCursor']

        if not page_info['hasNextPage']:
            break


def substitute(target: str, values: Dict) -> str:
    for name, value in values.items():
        value = ' '.join(value) if isinstance(value, list) else value
        target = target.replace(f'%{name}%', value)
    return re.sub('%[^%]*%', '', target)
