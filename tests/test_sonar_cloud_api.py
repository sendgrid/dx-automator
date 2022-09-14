import unittest
from unittest.mock import patch, Mock

from examples.common.sonar_cloud_api import SonarCloudApi, Metrics, COMPONENT_MEASURES_URL, PROJECT_BRANCHES_URL


class TestSonarCloudApi(unittest.TestCase):
    @patch('examples.common.sonar_cloud_api.requests')
    def test_get_project_branches(self, requests_mock):
        response_mock = Mock()
        response_mock.json.return_value = {
            'branches': [{
                'name': 'main',
                'isMain': True,
            }, {
                'name': '1.0.0-rc',
                'isMain': False,
            }]
        }
        requests_mock.get.return_value = response_mock

        response = SonarCloudApi().get_project_branches('erg', 'goo')

        self.assertEqual('main', response[0].name)
        self.assertEqual(True, response[0].is_main)
        self.assertEqual(False, response[0].is_pre_release)

        self.assertEqual('1.0.0-rc', response[1].name)
        self.assertEqual(False, response[1].is_main)
        self.assertEqual(True, response[1].is_pre_release)

        expected_params = {'project': 'erg_goo'}
        requests_mock.get.assert_called_once_with(PROJECT_BRANCHES_URL, expected_params)

    @patch('examples.common.sonar_cloud_api.requests')
    def test_get_component_measures(self, requests_mock):
        response_mock = Mock()
        response_mock.json.return_value = {
            'component': {
                'measures': 'foo'
            }
        }
        requests_mock.get.return_value = response_mock

        response = SonarCloudApi().get_component_measures('erg', 'goo', 'main',
                                                          [Metrics.LINES_TO_COVER, Metrics.UNCOVERED_LINES])

        self.assertEqual('foo', response)

        expected_params = {'component': 'erg_goo', 'branch': 'main', 'metricKeys': 'lines_to_cover,uncovered_lines'}
        requests_mock.get.assert_called_once_with(COMPONENT_MEASURES_URL, expected_params)

    @patch('examples.common.sonar_cloud_api.requests')
    def test_get_errors(self, requests_mock):
        response_mock = Mock()
        response_mock.json.return_value = {'errors': 'ugh'}
        requests_mock.get.return_value = response_mock

        branches = SonarCloudApi().get_project_branches('erg', 'goo')
        self.assertIsNone(branches)

        measures = SonarCloudApi().get_component_measures('erg', 'goo', 'main',
                                                          [Metrics.LINES_TO_COVER, Metrics.UNCOVERED_LINES])
        self.assertIsNone(measures)
