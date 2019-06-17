from python_http_client import Client
import os
import json
from repos import all_repos

def get_items(repo, item_type):
    client = Client(host="http://{}".format(os.environ.get('DX_IP')))
    query_params = {
        "repo":repo,
        "item_type":item_type,
        "labels[]":['type: bug'],
        "states[]":['OPEN'],
        "limit[]":['first', '100']
    }
    response = client.github.items.get(query_params=query_params)
    items = json.loads(response.body)
    return items

total_bugs = 0
for repo in all_repos:
    issues = get_items(repo, 'issues')
    prs = get_items(repo, 'pull_requests')
    items = issues + prs
    for item in items:
        text = "{} , {}".format(item['url'], item['createdAt'])
        print(text)
        total_bugs = total_bugs + 1

print("There are a total of {} open bugs needing assistance across all repos".format(total_bugs))
        
