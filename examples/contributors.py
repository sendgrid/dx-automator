import datetime
import json

from common.automator_client import client
from common.repos import ALL_REPOS


def get_items(org, repo, item_type):
    query_params = {
        "org": org,
        "repo": repo,
        "item_type": item_type,
        "states[]": ['MERGED'],
        "limit[]": ['first', '100']
    }
    response = client.github.items.get(query_params=query_params)
    return json.loads(response.body)


total_merged_prs = 0
contributors = []
for org in ALL_REPOS:
    for repo in ALL_REPOS[org]:
        items = get_items(org, repo, 'pull_requests')
        for item in items:
            merged_at = datetime.datetime.strptime(item['closedAt'], '%Y-%m-%dT%H:%M:%SZ')
            if str(merged_at) > '2019-01-01':
                text = "{}, {} , {}, {}".format(repo, item['url'], item['author'], merged_at.date())
                print(text)
                contributors.append(item['author'])
                total_merged_prs = total_merged_prs + 1

print("There were a total of {} merged prs across all repos in 2019".format(total_merged_prs))
print("There were a total of {} contributors across all repos in 2019".format(len(set(contributors))))
