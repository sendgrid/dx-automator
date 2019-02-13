from python_http_client import Client
import os
import json
import time

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

def get_prs(repo):
    client = Client(host="http://{}".format(os.environ.get('DX_IP')))
    query_params = {
        "repo":repo,
        "labels":"status: code review request",
        "states":"OPEN",
        }
    response = client.github.prs.get(query_params=query_params, limit=100)
    issues = json.loads(response.body)
    return issues

total_to_review = 0
# count = 0
for repo in all_repos:
    prs = get_prs(repo)
    for pr in prs:
        text = "{}, {}".format(pr['url'], pr['createdAt'])
        print(text)
        total_to_review += 1
    # count += 1
    # if count % 5 == 0:
    #     time.sleep(60)

print("There are a total of {} open bugs needing assistance across all repos".format(total_bugs))