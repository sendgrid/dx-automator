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
    'dx-automator',
    'dx-mobile',
    'ui-components',
    'docs'
]

def get_prs(repo):
    client = Client(host="http://{}".format(os.environ.get('DX_IP')))
    query_params = {"repo":repo, "labels":"status: hacktoberfest approved"}
    response = client.github.prs.get(query_params=query_params)
    prs = json.loads(response.body)
    return prs

total_hacktoberfest_approved_prs = 0.0
total_points_earned = 0.0
total_contributors = list()
for repo in all_repos:
    repo_points_earned = 0.0
    repo_hacktoberfest_approved_prs = 0.0
    repo_contributors = list()
    prs = get_prs(repo)
    for pr in prs:
        text = "{} by {} is worth {} points".format(pr['url'], pr['author'], pr['points'])
        num_reviewers = len(pr['reviewers'])
        if num_reviewers > 0:
            reviewers = ', '.join(str(x) for x in pr['reviewers'])
            print("{}, there were {} reviewers ({}) on this PR, worth {} points".format(text, num_reviewers, reviewers, pr['reviewer_points']))
            for reviewer in pr['reviewers']:
                total_contributors.append(reviewer)
                repo_contributors.append(reviewer)
        else:
            print(text)
        total_points_earned += pr['points'] + pr['reviewer_points']
        repo_points_earned += pr['points'] + pr['reviewer_points']
        total_contributors.append(pr['author'])
        repo_contributors.append(pr['author'])
    num_prs = len(prs)
    total_hacktoberfest_approved_prs += num_prs
    repo_hacktoberfest_approved_prs += num_prs
    print("There were a total of {} unique contributors for repo {}".format(len(list(set(repo_contributors))), repo))
    print("There are a total of {} qualifying PRs for repo {}".format(repo_hacktoberfest_approved_prs, repo))
    print("For a total of {} points earned for repo {}\n".format(repo_points_earned, repo))

print("There were a total of {} unique contributors ".format(len(list(set(repo_contributors)))))
print("There are a total of {} qualifying PRs".format(total_hacktoberfest_approved_prs))
print("For a total of {} points earned".format(total_points_earned))