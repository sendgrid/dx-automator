from collections import namedtuple
from typing import List

Repo = namedtuple('Repo', 'org name')

ALL_REPOS = {
    'sendgrid': [
        'sendgrid-csharp',
        'sendgrid-go',
        'sendgrid-java',
        'sendgrid-nodejs',
        'sendgrid-php',
        'sendgrid-python',
        'sendgrid-ruby',
        'smtpapi-csharp',
        'smtpapi-go',
        'smtpapi-java',
        'smtpapi-nodejs',
        'smtpapi-php',
        'smtpapi-python',
        'smtpapi-ruby',
        'csharp-http-client',
        'rest',
        'java-http-client',
        'php-http-client',
        'python-http-client',
        'ruby-http-client',
        'sendgrid-oai',
    ],
    'twilio': [
        'twilio-csharp',
        'twilio-java',
        'twilio-node',
        'twilio-php',
        'twilio-python',
        'twilio-ruby',
        'twilio-cli',
        'twilio-cli-core',
        'twilio-oai',
        'plugin-debugger',
        'homebrew-brew',
        'twilio-go',
        'twilio-oai-generator',
        'terraform-provider-twilio'
    ]
}


def get_repos(include_orgs: List[str] = None,
              include_repos: List[str] = None,
              exclude_repos: List[str] = None) -> List[Repo]:
    return [Repo(org, repo) for org in ALL_REPOS for repo in ALL_REPOS[org]
            if is_repo_included(org, repo, include_orgs, include_repos, exclude_repos)]


def is_repo_included(org: str, repo: str,
                     include_orgs: List[str],
                     include_repos: List[str],
                     exclude_repos: List[str]) -> bool:
    if exclude_repos and repo in exclude_repos:
        return False

    if include_orgs:
        return org in include_orgs or (include_repos and repo in include_repos)

    if include_repos:
        return repo in include_repos

    return True
