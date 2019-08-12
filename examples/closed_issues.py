from python_http_client import Client
import datetime
import os
import json
import repos

all_repos = repos.ALL_REPOS

def get_items(org, repo, item_type):
    client = Client(host="http://{}".format(os.environ.get('DX_IP')))
    query_params = {
        "org":org,
        "repo":repo,
        "item_type":item_type,
        "states[]":['CLOSED'],
        "limit[]":['first', '100']
    }
    response = client.github.items.get(query_params=query_params)
    items = json.loads(response.body)
    return items

total_closed_issues = 0
for org in all_repos:
    for repo in all_repos[org]:
        items = get_items(org, repo, 'issues')
        for item in items:
            updated_at = datetime.datetime.strptime(item['updatedAt'], '%Y-%m-%dT%H:%M:%SZ')
            text = "{}, {} , {}".format(repo, item['url'], updated_at.date())
            print(text)
            total_closed_issues = total_closed_issues + 1

print("There were a total of {} closed issues across all repos".format(total_closed_issues))
