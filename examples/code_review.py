import json

from common.automator_client import client
from common.repos import ALL_REPOS


def get_prs(org, repo):
    query_params = {
        "org": org,
        "repo": repo,
        "item_type": 'pull_requests',
        "labels[]": ['status: code review request'],
        "states[]": ['OPEN'],
        "limit[]": ['first', '100']
    }
    response = client.github.items.get(query_params=query_params)
    return json.loads(response.body)


total_prs_to_review = 0
for org in ALL_REPOS:
    for repo in ALL_REPOS[org]:
        prs = get_prs(org, repo)
        for pr in prs:
            text = "{} , {}".format(pr['url'], pr['createdAt'])
            print(text)
            total_prs_to_review += 1

print("There are a total of {} open prs needing a code review across all repos".format(
    total_prs_to_review))
