import unittest
from unittest.mock import Mock

from examples.metrics import MetricCollector


class TestMetricCollector(unittest.TestCase):
    def setUp(self):
        self.datadog_api_mock = Mock()

        self.collector = MetricCollector(self.datadog_api_mock)

    def test_get_series_for_datadog_1(self):
        series = list(self.collector.get_series_for_datadog({'metrics': {'issue_count': {'count': 3}}}, 'test-org', 'test-repo'))

        self.assertEqual(1, len(series))

        first = series[0]
        self.assertEqual('helper_library.issue_count.count', first.metric)
        self.assertEqual(['org:test-org', 'repo:test-org/test-repo'], first.tags)
        self.assertEqual(1, len(first.points))

    def test_get_series_for_datadog_2(self):
        # This should throw an exception due to missing metric names and types and return nothing
        series = list(self.collector.get_series_for_datadog({'metrics': {}}, 'test-org', 'test-repo'))

        self.assertEqual(0, len(series))

    