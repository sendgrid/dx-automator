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
    query_params = {"repo":repo}
    response = client.github.issues.get(query_params=query_params)
    issues = json.loads(response.body)
    return issues

for repo in all_repos:
    issues = get_issues(repo)
    for issue in issues:
        text = "{}, {}".format(issue['url'], issue['createdAt'])
        print(text)
        
