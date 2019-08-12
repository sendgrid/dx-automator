from python_http_client import Client
import os
import json
import repos

all_repos = repos.ALL_REPOS

def get_items(repo, item_type):
    client = Client(host="http://{}".format(os.environ.get('DX_IP')))
    query_params = {
        "repo":repo,
        "item_type":item_type,
        "labels[]":['type: security'],
        "states[]":['OPEN'],
        "limit[]":['first', '100']
    }
    response = client.github.items.get(query_params=query_params)
    items = json.loads(response.body)
    return items

total_security_issues = 0
for org in all_repos:
    for repo in all_repos[org]:
        issues = get_items(repo, 'issues')
        prs = get_items(repo, 'pull_requests')
        items = prs + issues
        for item in items:
            text = "{} , {}".format(item['url'], item['createdAt'])
            print(text)
            total_security_issues = total_security_issues + 1

print("There are a total of {} open security issues needing attention across all repos".format(total_security_issues))
