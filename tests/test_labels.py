import unittest

from examples.common.labels import ALL_LABELS, Label, get_labels


class TestLabels(unittest.TestCase):

    def test_get_labels(self):
        total_labels_length = len(ALL_LABELS)
        self.assertEqual(total_labels_length, len(get_labels()))

        ALL_LABELS.append(Label('status: duplicate', '', ''))

        try:
            self.assertRaises(KeyError, get_labels)
        finally:
            ALL_LABELS.pop()
