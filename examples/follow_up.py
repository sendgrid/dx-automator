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

list_of_maintainers = [
    'aroach',
    'thinkingserious',
    'kylearoberts',
    'SendGridDX',
    'codecov'
]

def get_items(repo, item_type):
    client = Client(host="http://{}".format(os.environ.get('DX_IP')))
    query_params = {
        "repo":repo,
        "item_type":item_type,
        "states[]":['OPEN'],
        "limit[]":['first', '100']
        }
    response = client.github.items.get(query_params=query_params)
    items = json.loads(response.body)
    return items  

total_issues = 0
total_prs = 0
for repo in all_repos:
    prs = get_items(repo, 'pull_requests')
    for pr in prs:
        if pr['last_comment_author'] and (pr['last_comment_author'] not in list_of_maintainers):
            text = "{} , {}".format(pr['url'], pr['createdAt'])
            print(text)
            total_prs = total_prs + 1
    issues = get_items(repo, 'issues')
    for issue in issues:
        if issue['last_comment_author'] and (issue['last_comment_author']not in list_of_maintainers):
            text = "{} , {}".format(issue['url'], issue['createdAt'])
            print(text)
            total_issues = total_issues + 1

print("There are a total of {} prs needing a response across all repos".format(total_prs))
print("There are a total of {} issues needing a response across all repos".format(total_issues))
print("There are a total of {} issues + prs needing a response across all repos".format(total_prs + total_issues))
