import json

from common.automator_client import client
from common.repos import ALL_REPOS


def get_issues(org, repo):
    query_params = {
        "org": org,
        "repo": repo,
        "item_type": 'issues',
        "states[]": ['OPEN'],
        "limit[]": ['first', '100']
    }
    response = client.github.items.get(query_params=query_params)
    return json.loads(response.body)


total_unlabeled_issues = 0
for org in ALL_REPOS:
    for repo in ALL_REPOS[org]:
        issues = get_issues(org, repo)
        for issue in issues:
            if issue['num_labels'] == 0:
                text = "{} , {}".format(issue['url'], issue['createdAt'])
                print(text)
                total_unlabeled_issues = total_unlabeled_issues + 1

print("There are a total of {} issues that need to be labeled".format(total_unlabeled_issues))
