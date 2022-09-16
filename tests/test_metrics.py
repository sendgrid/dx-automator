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
