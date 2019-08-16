import datetime
import json

from common.automator_client import client
from common.repos import ALL_REPOS


def get_items(org, repo, item_type):
    query_params = {
        "org": org,
        "repo": repo,
        "item_type": item_type,
        "limit[]": ['first', '100']
    }
    response = client.github.items.get(query_params=query_params)
    return json.loads(response.body)


total_opened_issues = 0
for org in ALL_REPOS:
    for repo in ALL_REPOS[org]:
        items = get_items(org, repo, 'issues')
        for item in items:
            created_at = datetime.datetime.strptime(item['createdAt'], '%Y-%m-%dT%H:%M:%SZ')
            text = "{}, {} , {}".format(repo, item['url'], created_at.date())
            print(text)
            total_opened_issues = total_opened_issues + 1

print("There were a total of {} open issues across all repos".format(total_opened_issues))
