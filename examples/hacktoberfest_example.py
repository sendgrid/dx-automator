import json
from collections import defaultdict

from common.automator_client import client
from common.repos import ALL_REPOS


def get_prs(org, repo):
    query_params = {
        "org": org,
        "repo": repo,
        "item_type": 'pull_requests',
        "labels[]": ['status: hacktoberfest approved'],
        "limit[]": ['first', '100']
    }
    response = client.github.items.get(query_params=query_params)
    return json.loads(response.body)

total_hacktoberfest_approved_prs = 0.0
total_points_earned = 0.0
total_contributors = list()
points_earned = defaultdict(int)
for org in ALL_REPOS:
    for repo in ALL_REPOS[org]:
        repo_points_earned = 0.0
        repo_hacktoberfest_approved_prs = 0.0
        repo_contributors = list()
        prs = get_prs(org, repo)
        for pr in prs:
            text = "{} by {} is worth {} points".format(pr['url'], pr['author'], pr['points'])
            if pr['num_reviewers'] > 0:
                reviewers = ', '.join(str(x) for x in pr['reviewers'])
                print("{}, there were {} reviewers ({}) on this PR, worth {} points".format(text, pr['num_reviewers'], reviewers, pr['reviewer_points']))
                for reviewer in pr['reviewers']:
                    points_earned[reviewer] += pr['points'] / 2
                    total_contributors.append(reviewer)
                    repo_contributors.append(reviewer)
            else:
                print(text)
            points_earned[pr['author']] += pr['points']
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

print("There were a total of {} unique contributors ".format(len(list(set(total_contributors)))))
print("There are a total of {} qualifying PRs".format(total_hacktoberfest_approved_prs))
print("For a total of {} points earned\n".format(total_points_earned))

sorted_points_earned = [(k, points_earned[k]) for k in sorted(points_earned, key=points_earned.__getitem__, reverse=True)]
for author, points in sorted_points_earned:
    print("{} earned {} points".format(author, float(points)))
