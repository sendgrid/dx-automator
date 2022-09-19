import unittest

from examples.metrics import MetricCollector


class TestMetrics(unittest.TestCase):

    def test_aggregate(self):
        metrics = {}
        MetricCollector().aggregate({
            'metrics': metrics,
            'nodes': {
                'twilio-node/issues/10': {
                    'category': 'bug',
                    'metrics': {
                        'time_open': 10,
                        'time_to_respond': [1, 2],
                    }
                },
                'twilio-node/issues/100': {
                    'category': 'bug',
                    'metrics': {
                        'time_open': 90,
                        'time_to_respond': {
                            'values': [3, 4]
                        }
                    }
                }
            }
        })

        time_open = metrics['time_open']['bug']
        time_to_respond = metrics['time_to_respond']['bug']

        self.assertEqual(2, time_open['count'])
        self.assertEqual(100, time_open['sum'])
        self.assertEqual(10, time_open['min'])
        self.assertEqual(90, time_open['max'])

        self.assertEqual(4, time_to_respond['count'])
        self.assertEqual(10, time_to_respond['sum'])
        self.assertEqual(1, time_to_respond['min'])
        self.assertEqual(4, time_to_respond['max'])

    def test_get_series_for_datadog(self):
        metrics = {
            'issue_count': {
                'bug': {
                    'count': 1,
                    'sum': 5,
                    'min': 5,
                    'max': 5,
                },
                'enhancement': {
                    'count': 2,
                    'sum': 10,
                    'min': 1,
                    'max': 9,
                }
            },
            'time_open': {
                'support': {
                    'count': 10,
                    'sum': 20,
                    'min': 1,
                    'max': 10,
                }
            }
        }
        series = list(MetricCollector().get_series_for_datadog({'metrics': metrics}, 'twilio', 'twilio-node'))

        self.assertEqual(3, len(series))
        self.assertEqual('library.issue_count.count', series[0].metric)
        self.assertEqual('library.issue_count.count', series[1].metric)
        self.assertEqual('library.time_open.max', series[2].metric)

        self.assertEqual(1, series[0].points[0].value[1])
        self.assertEqual(2, series[1].points[0].value[1])
        self.assertEqual(10, series[2].points[0].value[1])

        self.assertTrue('category:bug' in series[0].tags)
        self.assertTrue('category:enhancement' in series[1].tags)
        self.assertTrue('category:support' in series[2].tags)
