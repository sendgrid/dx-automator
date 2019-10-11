import datetime
import json

from common.automator_client import client
from common.repos import ALL_REPOS


def get_items(org, repo, item_type):
    query_params = {
        "org": org,
        "repo": repo,
        "item_type": item_type,
        "states[]": ['MERGED', 'CLOSED'],
        "limit[]": ['first', '100']
    }
    response = client.github.items.get(query_params=query_params)
    return json.loads(response.body)


total_closed_prs = 0
for org in ALL_REPOS:
    for repo in ALL_REPOS[org]:
        items = get_items(org, repo, 'pull_requests')
        for item in items:
            closed_at = datetime.datetime.strptime(item['closedAt'], '%Y-%m-%dT%H:%M:%SZ')
            text = "{}, {} , {}, {}".format(repo, item['url'], closed_at.date(), item['author'])
            print(text)
            total_closed_prs = total_closed_prs + 1

print("There were a total of {} closed prs across all repos".format(total_closed_prs))
