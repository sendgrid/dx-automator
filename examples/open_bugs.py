from python_http_client import Client
import os
import json

all_repos = [
    'sendgrid-nodejs',
    'sendgrid-csharp',
    'sendgrid-php',
    'sendgrid-python',
    'sendgrid-java',
    'sendgrid-go',
    'sendgrid-ruby',
    'smtpapi-nodejs',
    'smtpapi-go',
    'smtpapi-python',
    'smtpapi-php',
    'smtpapi-csharp',
    'smtpapi-java',
    'smtpapi-ruby',
    'sendgrid-oai',
    'open-source-library-data-collector',
    'python-http-client',
    'php-http-client',
    'csharp-http-client',
    'java-http-client',
    'ruby-http-client',
    'rest',
    'nodejs-http-client',
    'dx-automator'
]

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
    for issue in issues:
        text = "{} , {}".format(issue['url'], issue['createdAt'])
        print(text)
        total_bugs = total_bugs + 1
    prs = get_items(repo, 'pull_requests')
    for pr in prs:
        text = "{} , {}".format(pr['url'], pr['createdAt'])
        print(text)
        total_bugs = total_bugs + 1

print("There are a total of {} open bugs needing assistance across all repos".format(total_bugs))
        
