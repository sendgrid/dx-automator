from python_http_client import Client
import datetime
import os
import json

all_repos = {
  'sendgrid': [
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
    'dx-automator',
  ],
  'twilio': [
    'twilio-node',
    'twilio-csharp',
    'twilio-php',
    'twilio-python',
    'twilio-java',
    'twilio-ruby',
    'twilio-cli',
    'twilio-cli-core'
  ]
}

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

total_closed_prs = 0
for org in all_repos:
    for repo in all_repos[org]:
        items = get_items(org, repo, 'pull_requests')
        for item in items:
            updated_at = datetime.datetime.strptime(item['updatedAt'], '%Y-%m-%dT%H:%M:%SZ')
            text = "{}, {} , {}".format(repo, item['url'], updated_at.date())
            print(text)
            total_closed_prs = total_closed_prs + 1

print("There were a total of {} closed prs across all repos".format(total_closed_prs))
