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
        "start_creation_date": "2018-01-01",
        "end_creation_date": "2019-01-01",
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
