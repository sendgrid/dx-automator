import datetime
import json

from common.automator_client import client
from common.repos import ALL_REPOS


def get_releases(org, repo):
    query_params = {
        "org": org,
        "repo": repo,
    }
    response = client.github.releases.get(query_params=query_params)
    return json.loads(response.body)


total_releases = 0
for org in ALL_REPOS:
    for repo in ALL_REPOS[org]:
        releases = get_releases(org, repo)
        for release in releases:
            created_at = datetime.datetime.strptime(release['created_at'], '%Y-%m-%dT%H:%M:%SZ')
            print("{}, {}, {}".format(repo, created_at.date(), release['tag_name']))
            total_releases = total_releases + 1

print("There are a total of {} releases across all repos".format(total_releases))
