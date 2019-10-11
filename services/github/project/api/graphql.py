from flask import current_app
import json
import requests


class GraphQL(object):
    def __init__(self,
                 organization,
                 github_type,
                 repo,
                 states=None,
                 labels=None,
                 limit=['first', 100],
                 end_cursor=None):
        """Create a GitHub GraphQL v4 Query

        :param organization: Name of your GitHub organization
        :type organization: string, required
        :param github_type: A 'pull_request' or 'issue'
        :type github_type : string, required
        :param repo: A GitHub repository name
        :type repo: string, required
        :param states: The state of the GitHub PR or issue to filter by
        :type states: list, optional
        :param labels: The names of the labels to filter by
        :type labels: list, optional
        :param limit: The limit of results per page. (<first or last>, int)
        :type limit: tuple
        """
        self.organization = organization
        self.github_type = github_type
        self.repo = repo
        self.states = states
        self.labels = labels
        self.limit = limit
        self.end_cursor = end_cursor

        if github_type in {'pull_requests', 'pullRequests'}:
            self.github_type = 'pullRequests'
            self.review = f"""reviews(first: 10) {{
                                nodes {{
                                    author {{
                                        login
                                    }}
                                }}
                            }}"""
        else:
            self.review = ''

        if self.limit:
            self.limit = '{}: {}, '.format(self.limit[0], str(self.limit[1]))
        else:
            self.limit = ''

        if self.states:
            self.states = '{}: {}, '.format('states', json.dumps(self.states).replace('"', ''))
        else:
            self.states = ''

        if self.labels:
            self.labels = '{}: {}, '.format('labels', json.dumps(self.labels))
        else:
            self.labels = ''

        if self.end_cursor:
            self.end_cursor = '{}: {}'.format('after', json.dumps(self.end_cursor))
        else:
            self.end_cursor = ''

        self.query = f"""query{{
            organization(login: "{self.organization}") {{
                repository(name: "{self.repo}") {{
                    {self.github_type}({self.limit}{self.states}{self.labels}{self.end_cursor}) {{
                        nodes {{
                            url
                            state
                            title
                            createdAt
                            updatedAt
                            closedAt
                            mergedAt
                            {self.review}
                            author {{
                                login
                            }}
                            labels(first: 20) {{
                                edges {{
                                    node {{
                                        name
                                        id
                                    }}
                                }}
                            }}
                            comments(last: 1) {{
                                totalCount
                                nodes {{
                                    author {{
                                        login
                                    }}
                                    reactions(last: 100) {{
                                        nodes {{
                                            content
                                            user {{
                                                login
                                            }}
                                        }}
                                    }}
                                }}
                            }}
                            reactions(last: 100) {{
                                totalCount
                            }}
                        }}
                        pageInfo {{
                            endCursor
                            hasNextPage
                        }}
                    }}
                }}
            }}
        }}"""

    @classmethod
    def run_query(self, query):
        print(query)
        """Runs GraphQL query"""
        url = "https://api.github.com/graphql"
        github_token = current_app.config['GITHUB_TOKEN']
        headers = {
            "Authorization": f"bearer {github_token}"
        }
        response = requests.post(url, json={'query': query}, headers=headers)
        if response.ok:
            return response.json().get('data'), response.ok
        return None, response.ok

    def __str__(self):
        return self.query
