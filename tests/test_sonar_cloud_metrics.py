import unittest
from unittest.mock import Mock

from examples.common.repos import Repo
from examples.sonar_cloud_metrics import SonarCloudMetricCollector, parse_args


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

    def test_get_series(self):
        series = list(self.collector.get_series(Repo('erg', 'goo'), [{'metric': 'branch_coverage', 'value': "78.9"}]))

        self.assertEqual(1, len(series))

        first = series[0]
        self.assertEqual('sonar_cloud.measures.branch_coverage', first.metric)
        self.assertEqual(['org:erg', 'repo:erg/goo'], first.tags)
        self.assertEqual(1, len(first.points))

    def test_run(self):
        self.sonar_cloud_api_mock.get_component_measures.return_value = [{'metric': 'branch_coverage', 'value': "78.9"}]

        self.collector.run([Repo('erg', 'goo')])

        self.sonar_cloud_api_mock.get_component_measures.assert_called_once()
        self.datadog_api_mock.submit_metrics.assert_called_once()
