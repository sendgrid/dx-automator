from python_http_client import Client
import os
import json
from repos import all_repos

def get_issues(repo):
    client = Client(host="http://{}".format(os.environ.get('DX_IP')))
    query_params = {
        "repo":repo,
        "item_type":'issues',
        "states[]":['OPEN'],
        "limit[]":['first', '100']
    }
    response = client.github.items.get(query_params=query_params)
    issues = json.loads(response.body)
    return issues

total_unlabeled_issues = 0
for repo in all_repos:
    issues = get_issues(repo)
    for issue in issues:
        if issue['num_labels'] == 0:
            text = "{} , {}".format(issue['url'], issue['createdAt'])
            print(text)
            total_unlabeled_issues = total_unlabeled_issues + 1

print("There are a total of {} issues that need to be labeled".format(total_unlabeled_issues))