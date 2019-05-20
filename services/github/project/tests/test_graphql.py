import json
import logging

from project.tests.base import BaseTestCase
from project.api.graphql import GraphQL

class TestGraphQL(BaseTestCase):
    """Tests for the GraphQL class."""
    logging.basicConfig(level=logging.ERROR)

    def test_init(self):
        graphql = GraphQL(
            organization='twilio',
            github_type='pull_requests',
            repo='twilio-php'
        )
        test_string = '''query{
            organization(login: "twilio") {
                repository(name: "twilio-php") {
                    pullRequests(first: 100, after: ) {
                        nodes {
                            url
                            state
                            title
                            createdAt
                            updatedAt
                            reviews(first:10) {
                                nodes{
                                    author{
                                        login
                                    }
                                }
                            }
                            author {
                                login
                            }
                            labels(first: 20) {
                                edges {
                                    node {
                                        name
                                        id
                                    }
                                }
                            }
                            comments(last: 1) {
                                totalCount
                                nodes {
                                    author {
                                        login
                                    }
                                }
                            }
                            reactions(last:100) {
                                totalCount
                            }

                            }
                            pageInfo {
                                endCursor
                                hasNextPage
                            }
                        }
                    }
                }
            }'''
        
        logging.info(graphql.__str__())

        v1 = ''.join(graphql.__str__().split())
        v2 = ''.join(test_string.split())
        self.maxDiff = None
        self.assertEqual(v1, v2)

    def test_multiple_states(self):
        graphql = GraphQL(
            organization='twilio',
            github_type='issues',
            repo='twilio-python',
            states=['OPEN','MERGED', 'CLOSED'],
            limit=['first', 100]
        )
        test_string = '''query{
            organization(login: "twilio") {
                repository(name: "twilio-python") {
                    issues(first: 100, states: [OPEN, MERGED, CLOSED], after: ) {
                        nodes {
                            url
                            state
                            title
                            createdAt
                            updatedAt
                            author {
                                login
                            }
                            labels(first: 20) {
                                edges {
                                    node {
                                        name
                                        id
                                    }
                                }
                            }
                            comments(last: 1) {
                                totalCount
                                nodes {
                                    author {
                                        login
                                    }
                                }
                            }
                            reactions(last:100) {
                                totalCount
                            }

                            }
                            pageInfo {
                                endCursor
                                hasNextPage
                            }
                        }
                    }
                }
            }'''
        
        logging.info(graphql.__str__())

        v1 = ''.join(graphql.__str__().split())
        v2 = ''.join(test_string.split())
        self.assertEqual(v1, v2)

    def test_multiple_labels(self):
        graphql = GraphQL(
            organization='twilio',
            github_type='pull_requests',
            repo='twilio-python',
            labels=['difficulty: easy', 'status: code review'],
            limit=['first', 100]
        )
        test_string = '''query{
            organization(login: "twilio") {
                repository(name: "twilio-python") {
                    pullRequests(first: 100, labels: ["difficulty: easy", "status: code review"], after: ) {
                        nodes {
                            url
                            state
                            title
                            createdAt
                            updatedAt
                            reviews(first:10) {
                                nodes{
                                    author{
                                        login
                                    }
                                }
                            }
                            author {
                                login
                            }
                            labels(first: 20) {
                                edges {
                                    node {
                                        name
                                        id
                                    }
                                }
                            }
                            comments(last: 1) {
                                totalCount
                                nodes {
                                    author {
                                        login
                                    }
                                }
                            }
                            reactions(last:100) {
                                totalCount
                            }

                            }
                            pageInfo {
                                endCursor
                                hasNextPage
                            }
                        }
                    }
                }
            }'''
        
        logging.info(graphql.__str__())

        v1 = ''.join(graphql.__str__().split())
        v2 = ''.join(test_string.split())
        self.assertEqual(v1, v2)

    def test_multiple_states_and_labels(self):
        graphql = GraphQL(
            organization='sendgrid',
            github_type='pull_requests',
            repo='sendgrid-python',
            states=['OPEN','MERGED'],
            labels=['difficulty: easy', 'status: code review'],
            limit=['first', 100]
        )
        test_string = '''query{
            organization(login: "sendgrid") {
                repository(name: "sendgrid-python") {
                    pullRequests(first: 100, states: [OPEN, MERGED], labels: ["difficulty: easy", "status: code review"], after: ) {
                        nodes {
                            url
                            state
                            title
                            createdAt
                            updatedAt
                            reviews(first:10) {
                                nodes{
                                    author{
                                        login
                                    }
                                }
                            }
                            author {
                                login
                            }
                            labels(first: 20) {
                                edges {
                                    node {
                                        name
                                        id
                                    }
                                }
                            }
                            comments(last: 1) {
                                totalCount
                                nodes {
                                    author {
                                        login
                                    }
                                }
                            }
                            reactions(last:100) {
                                totalCount
                            }

                            }
                            pageInfo {
                                endCursor
                                hasNextPage
                            }
                        }
                    }
                }
            }'''
        
        logging.info(graphql.__str__())

        v1 = ''.join(graphql.__str__().split())
        v2 = ''.join(test_string.split())
        self.assertEqual(v1, v2)
