import unittest
from unittest.mock import patch, Mock

from examples.common.sonar_cloud_api import SonarCloudApi, Metrics, COMPONENT_MEASURES_URL


class TestSonarCloudApi(unittest.TestCase):
    @patch('examples.common.sonar_cloud_api.requests')
    def test_get_component_measures(self, requests_mock):
        response_mock = Mock()
        response_mock.json.return_value = {
            'component': {
                'measures': 'foo'
            }
        }
        requests_mock.get.return_value = response_mock

        response = SonarCloudApi().get_component_measures('erg', 'goo',
                                                          [Metrics.LINES_TO_COVER, Metrics.UNCOVERED_LINES])

        self.assertEqual('foo', response)

        expected_params = {'component': 'erg_goo', 'metricKeys': 'lines_to_cover,uncovered_lines'}
        requests_mock.get.assert_called_once_with(COMPONENT_MEASURES_URL, expected_params)

    @patch('examples.common.sonar_cloud_api.requests')
    def test_get_component_measures_error(self, requests_mock):
        response_mock = Mock()
        response_mock.json.return_value = {'errors': 'ugh'}
        requests_mock.get.return_value = response_mock

        response = SonarCloudApi().get_component_measures('erg', 'goo',
                                                          [Metrics.LINES_TO_COVER, Metrics.UNCOVERED_LINES])

        self.assertIsNone(response)
