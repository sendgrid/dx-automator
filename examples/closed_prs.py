import datetime
import json

from common.automator_client import client
from common.repos import ALL_REPOS


def get_items(org, repo, item_type):
    query_params = {
        "org": org,
        "repo": repo,
        "item_type": item_type,
        "states[]": ['CLOSED'],
        "limit[]": ['first', '100']
    }
    response = client.github.items.get(query_params=query_params)
    return json.loads(response.body)


total_closed_prs = 0
for org in ALL_REPOS:
    for repo in ALL_REPOS[org]:
        items = get_items(org, repo, 'pull_requests')
        for item in items:
            updated_at = datetime.datetime.strptime(item['updatedAt'], '%Y-%m-%dT%H:%M:%SZ')
            text = "{}, {} , {}, {}, {}".format(repo, item['url'], item['points'],
                                                item['reviewer_points'], updated_at.date())
            print(text)
            total_closed_prs = total_closed_prs + 1

print("There were a total of {} closed prs across all repos".format(total_closed_prs))
