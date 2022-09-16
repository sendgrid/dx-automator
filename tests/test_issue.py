import unittest

from examples.common.issue import Issue


class TestIssue(unittest.TestCase):

    def test_closed_pr_without_closed_event(self):
        issue_json = {
            '__typename': 'PullRequest',
            'author': {
                'login': 'arthur'
            },
            'createdAt': '2022-01-01T00:00:00Z',
            'closedAt': '2022-02-01T00:00:00Z',
            'url': 'https://github.com/twilio/twilio-node/pull/765',
            'state': 'CLOSED',
            'timelineItems': {
                'nodes': [
                    {
                        '__typename': 'PullRequestCommit',
                        'commit': {
                            'committedDate': '2022-01-01T00:00:00Z',
                            'author': {
                                'user': {
                                    'login': 'arthur'
                                }
                            },
                            'status': None,
                            'statusCheckRollup': {
                                'state': 'SUCCESS'
                            }
                        }
                    }
                ]
            }
        }
        issue = Issue(issue_json, '2022-01-10T00:00:00Z')
        issue.process_events()
        self.assertTrue(issue.is_open())
        self.assertTrue(self.is_awaiting(issue))

        issue = Issue(issue_json, '2022-02-01T00:00:00Z')
        issue.process_events()
        self.assertFalse(issue.is_open())
        self.assertFalse(self.is_awaiting(issue))

    def is_awaiting(self, issue: Issue) -> bool:
        return any(metric for metric in issue.metrics if metric.startswith('time_awaiting'))
