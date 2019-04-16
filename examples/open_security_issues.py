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

def get_issues(repo):
    client = Client(host="http://{}".format(os.environ.get('DX_IP')))
    query_params = {"repo":repo, "labels":"type: security"}
    response = client.github.issues.get(query_params=query_params)
    issues = json.loads(response.body)
    return issues

total_security_issues = 0
for repo in all_repos:
    issues = get_issues(repo)
    for issue in issues:
        # Github GraphQL v4 does not support the AND operator, so we have to do this ourselves
        if "status: help wanted" in issue['labels']:
            text = "{}, {}".format(issue['url'], issue['createdAt'])
            print(text)
            total_security_issues = total_security_issues + 1

print("There are a total of {} open security issues needing attention across all repos".format(total_security_issues))
