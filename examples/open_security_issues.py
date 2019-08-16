import json

from common.automator_client import client
from common.repos import ALL_REPOS


def get_items(org, repo, item_type):
    query_params = {
        "org": org,
        "repo": repo,
        "item_type": item_type,
        "labels[]": ['type: security'],
        "states[]": ['OPEN'],
        "limit[]": ['first', '100']
    }
    response = client.github.items.get(query_params=query_params)
    return json.loads(response.body)


total_security_issues = 0
for org in ALL_REPOS:
    for repo in ALL_REPOS[org]:
        issues = get_items(org, repo, 'issues')
        prs = get_items(org, repo, 'pull_requests')
        items = prs + issues
        for item in items:
            text = "{} , {}".format(item['url'], item['createdAt'])
            print(text)
            total_security_issues = total_security_issues + 1

print("There are a total of {} open security issues needing attention across all repos".format(
    total_security_issues))
