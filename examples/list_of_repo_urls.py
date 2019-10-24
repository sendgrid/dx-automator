from common.repos import ALL_REPOS

for org in ALL_REPOS:
    for repo in ALL_REPOS[org]:
        print(f'https://github.com/{org}/{repo}')
