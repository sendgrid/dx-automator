from python_http_client import Client
import datetime
import json
import os

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

def get_releases(org, repo):
    client = Client(host="http://{}".format(os.environ.get('DX_IP')))
    query_params = {
        "repo":repo,
        "org": org,
    }
    response = client.github.releases.get(query_params=query_params)
    releases = json.loads(response.body)
    return releases

total_releases = 0
for org in all_repos:
    for repo in all_repos[org]:
        releases = get_releases(org, repo)
        for release in releases:
            created_at = datetime.datetime.strptime(release['created_at'], '%Y-%m-%dT%H:%M:%SZ')
            print("{}, {}, {}".format(repo, created_at.date(), release['tag_name']))
            total_releases = total_releases + 1

print("There are a total of {} releases across all repos".format(total_releases))