import json

from common.automator_client import client
from common.repos import ALL_REPOS


def get_items(org, repo, item_type):
    query_params = {
        "org": org,
        "repo": repo,
        "item_type": item_type,
        "labels[]": ['type: bug'],
        "states[]": ['OPEN'],
        "limit[]": ['first', '100']
    }
    response = client.github.items.get(query_params=query_params)
    return json.loads(response.body)


total_bugs = 0
for org in ALL_REPOS:
    for repo in ALL_REPOS[org]:
        issues = get_items(org, repo, 'issues')
        prs = get_items(org, repo, 'pull_requests')
        items = issues + prs
        for item in items:
            text = "{} , {}".format(item['url'], item['createdAt'])
            print(text)
            total_bugs = total_bugs + 1

print("There are a total of {} open bugs needing assistance across all repos".format(total_bugs))
