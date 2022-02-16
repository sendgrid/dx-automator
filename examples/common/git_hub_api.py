import json
import os
import re
from typing import Iterator, Dict

import backoff
import requests
from requests import Response

GRAPH_QL_URL = 'https://api.github.com/graphql'


def submit_graphql_query(query: str) -> Iterator[Dict]:
    github_token = os.environ['GITHUB_TOKEN']
    headers = {'Authorization': f'token {github_token}'}
    cursor = None

    while True:
        paged_query = substitute(query, {'cursor': f'after: "{cursor}"' if cursor else ''})

        response = post(GRAPH_QL_URL, json={'query': paged_query}, headers=headers)
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


@backoff.on_exception(backoff.expo,
                      requests.exceptions.RequestException,
                      # Keep trying on 403s which indicate rate-limiting.
                      giveup=lambda e: e.response.status_code != 403)
def post(url, **kwargs) -> Response:
    response = requests.post(url, **kwargs)
    response.raise_for_status()
    return response


def substitute(target: str, values: Dict) -> str:
    for name, value in values.items():
        value = ' '.join(value) if isinstance(value, list) else value
        target = target.replace(f'%{name}%', value)
    return re.sub('%[^%]*%', '', target)
