import unittest

from pyflot import Flot, MissingDataException, \
        DuplicateLabelException


SERIES = (
    ((1, 1), (2, 2), (3, 3)),
)
S1, = SERIES

class TestFlot(unittest.TestCase):

    def setUp(self):
        self.flot = Flot()

    def check_add_series(self, raw, label=None):
        count = len(self.flot._series)
        self.flot.add_series(raw, label)
        self.assertEqual(count+1, len(self.flot._series))
        series = self.flot._series[count]
        self.assertEqual(raw, series['data'])
        if label:
            self.assertEqual(label, series['label'])
        else:
            self.assertFalse('label' in series)

    def test_basic_add_series(self):
        "make sure a series can be added with no label or options"
        self.check_add_series(S1)

    def test_reject_empty_series(self):
        """don't accept empty series"""
        self.assertRaises(MissingDataException, self.flot.add_series, [])
        self.assertEqual(len(self.flot._series), 0)

    def test_add_series_with_label(self):
        """make sure a label can be associated with a series"""
        self.flot.add_series(S1, "as_arg")
        self.flot._series = []
        self.flot.add_series(S1, label="as_kwarg")

    def test_reject_duplicate_label(self):
        "make sure a series is not added if it has a duplicate label"
        self.check_add_series(S1, "label1")
        self.assertRaises(DuplicateLabelException, self.flot.add_series, S1, "label1")

    def test_add_multiple_series(self):
        "make sure multiple series can be added"
        self.check_add_series(S1)
        self.check_add_series(S1)
