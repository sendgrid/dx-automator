import unittest
from unittest.mock import Mock

from examples.common.repos import Repo
from examples.common.sonar_cloud_api import ProjectBranch
from examples.sonar_cloud_metrics import SonarCloudMetricCollector, parse_args

TEST_REPO = Repo('erg', 'goo')


class TestSonarCloudMetricCollector(unittest.TestCase):
    def setUp(self):
        self.sonar_cloud_api_mock = Mock()
        self.datadog_api_mock = Mock()

        self.collector = SonarCloudMetricCollector(self.sonar_cloud_api_mock, self.datadog_api_mock)

    def test_parse_args_nothing(self):
        parsed_args = parse_args([])

        self.assertEqual([], parsed_args['org'])
        self.assertEqual([], parsed_args['include'])
        self.assertEqual([], parsed_args['exclude'])

    def test_parse_args_everything(self):
        parsed_args = parse_args([
            '--org', 'twilio',
            '-i', 'twilio-node', 'twilio-java',
            '-e', 'twilio-csharp'
        ])

        self.assertEqual(['twilio'], parsed_args['org'])
        self.assertEqual(['twilio-node', 'twilio-java'], parsed_args['include'])
        self.assertEqual(['twilio-csharp'], parsed_args['exclude'])

    def test_parse_args_failure(self):
        with self.assertRaises(SystemExit):
            parse_args(['--erg'])

    def test_get_branches(self):
        self.sonar_cloud_api_mock.get_project_branches.return_value = [
            ProjectBranch({'name': 'main', 'isMain': True}),
            ProjectBranch({'name': 'some-pr', 'isMain': False}),
            ProjectBranch({'name': '9.0.0-alpha', 'isMain': False}),
        ]

        branches = self.collector.get_branches(TEST_REPO)

        # 'some-pr' branch should not be included.
        self.assertEqual(2, len(branches))

        self.assertEqual('main', branches[0].name)
        self.assertEqual('9.0.0-alpha', branches[1].name)

    def test_get_branches_too_many_mains(self):
        self.sonar_cloud_api_mock.get_project_branches.return_value = [
            ProjectBranch({'name': 'main', 'isMain': True}),
            ProjectBranch({'name': 'another-main', 'isMain': True}),
        ]

        with self.assertRaises(RuntimeError):
            self.collector.get_branches(TEST_REPO)

    def test_get_branches_too_many_pre_releases(self):
        self.sonar_cloud_api_mock.get_project_branches.return_value = [
            ProjectBranch({'name': '9.0.0-alpha', 'isMain': False}),
            ProjectBranch({'name': '1.0.0-alpha', 'isMain': False}),
        ]

        with self.assertRaises(RuntimeError):
            self.collector.get_branches(TEST_REPO)

    def test_get_branches_empty(self):
        self.sonar_cloud_api_mock.get_project_branches.return_value = None

        branches = self.collector.get_branches(TEST_REPO)

        self.assertEqual(0, len(branches))

    def test_get_series(self):
        series = list(self.collector.get_series(TEST_REPO,
                                                ProjectBranch({'name': 'main', 'isMain': True}),
                                                [{'metric': 'branch_coverage', 'value': '78.9'}]))

        self.assertEqual(1, len(series))

        first = series[0]
        self.assertEqual('sonar_cloud.measures.branch_coverage', first.metric)
        self.assertEqual(['org:erg', 'repo:erg/goo', 'pre-release:False'], first.tags)
        self.assertEqual(1, len(first.points))

    def test_run(self):
        self.sonar_cloud_api_mock.get_project_branches.return_value = [ProjectBranch({'name': 'main', 'isMain': True})]
        self.sonar_cloud_api_mock.get_component_measures.return_value = [{'metric': 'branch_coverage', 'value': '78.9'}]

        self.collector.run([TEST_REPO])

        self.sonar_cloud_api_mock.get_project_branches.assert_called_once()
        self.sonar_cloud_api_mock.get_component_measures.assert_called_once()
        self.datadog_api_mock.submit_metrics.assert_called_once()
