import os
import unittest
from unittest.mock import patch, Mock

from requests import HTTPError

from examples.common.git_hub_api import GRAPH_QL_URL, submit_graphql_search_query, post, substitute


@patch.dict(os.environ, {"GITHUB_TOKEN": "THE TOKEN"})
class TestGitHubApi(unittest.TestCase):

    @patch('examples.common.git_hub_api.requests')
    def test_submit_graphql_search_query_single_page(self, requests_mock):
        response_mock = Mock()
        response_mock.json.return_value = {
            'data': {
                'search': {
                    'nodes': [{'id', 111}, {'id': 123}],
                    'pageInfo': {
                        'endCursor': 123,
                        'hasNextPage': False,
                    },
                },
            },
        }
        requests_mock.post.return_value = response_mock

        nodes = list(submit_graphql_search_query('some_query %cursor%'))

        self.assertEqual(2, len(nodes))
        requests_mock.post.assert_called_once_with(GRAPH_QL_URL,
                                                   json={'query': 'some_query '},
                                                   headers={'Authorization': 'token THE TOKEN'})

    @patch('examples.common.git_hub_api.requests')
    def test_submit_graphql_search_query_multi_page(self, requests_mock):
        response_mock = Mock()
        response_mock.json.side_effect = [{
            'data': {
                'search': {
                    'nodes': [{'id', 111}, {'id': 123}],
                    'pageInfo': {
                        'endCursor': 123,
                        'hasNextPage': True,
                    },
                },
            },
        }, {
            'data': {
                'search': {
                    'nodes': [{'id', 456}],
                    'pageInfo': {
                        'endCursor': 456,
                        'hasNextPage': False,
                    },
                },
            },
        }]
        requests_mock.post.return_value = response_mock

        nodes = list(submit_graphql_search_query('some_query %cursor%'))

        self.assertEqual(3, len(nodes))
        requests_mock.post.assert_any_call(GRAPH_QL_URL,
                                           json={'query': 'some_query '},
                                           headers={'Authorization': 'token THE TOKEN'})
        requests_mock.post.assert_any_call(GRAPH_QL_URL,
                                           json={'query': 'some_query after: "123"'},
                                           headers={'Authorization': 'token THE TOKEN'})

    @patch('examples.common.git_hub_api.requests')
    def test_post_retry_success(self, requests_mock):
        response_mock = Mock()
        response_mock.status_code = 403
        response_mock.raise_for_status.side_effect = [HTTPError('limited!', response=response_mock), None]
        requests_mock.post.return_value = response_mock

        self.assertEqual(response_mock, post('url'))
        self.assertEqual(2, requests_mock.post.call_count)

    @patch('examples.common.git_hub_api.requests')
    def test_post_retry_failure(self, requests_mock):
        response_mock = Mock()
        response_mock.status_code = 500
        response_mock.raise_for_status.side_effect = HTTPError('Server Error!', response=response_mock)
        requests_mock.post.return_value = response_mock

        with self.assertRaises(HTTPError):
            post('url')

        requests_mock.post.assert_called_once()

    def test_substitute(self):
        self.assertEqual('no substitutions', substitute('no substitutions', {}))
        self.assertEqual('missing  here', substitute('missing %substitution% here', {'sub': 'me?'}))
        self.assertEqual('normal sub', substitute('normal %replace_me%', {'replace_me': 'sub'}))
        self.assertEqual('list: 1 2 3', substitute('list: %items%', {'items': ['1', '2', '3']}))
