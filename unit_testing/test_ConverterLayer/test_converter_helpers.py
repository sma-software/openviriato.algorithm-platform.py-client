import datetime
import unittest

import isodate

import ConversionLayer.converter_helpers
from AIDMClasses import AIDM_classes


class TestAllConverterHelpers(unittest.TestCase):

    def test_parse_to_datetime_wrong_format(self):
        test_str = 'sd'

        with self.assertRaises(ValueError) as test_parse_to_datetime_wrong_format:
            ConversionLayer.converter_helpers.parse_to_datetime(test_str)

    def test_parse_to_datetime_proper_format(self):
        test_date_str = "0001-05-01T01:01:00"

        date = ConversionLayer.converter_helpers.parse_to_datetime(test_date_str)

        self.assertIsInstance(date, datetime.datetime)
        self.assertEqual(date, datetime.datetime(1, 5, 1, 1, 1))

    def test_parse_to_timedelta_wrong_format(self):
        test_delta_str = '30Seconds'

        with self.assertRaises(ValueError) as test_parse_to_datetime_wrong_format:
            ConversionLayer.converter_helpers.parse_to_timedelta(test_delta_str)

    def test_parse_to_timedelta_wrong_None(self):
        test_delta_str = None

        with self.assertRaises(TypeError) as test_parse_to_timedelta_wrong_None:
            ConversionLayer.converter_helpers.parse_to_timedelta(test_delta_str)

    def test_parse_to_timedelta_proper_format(self):
        test_delta_str = 'P0D'

        delta = ConversionLayer.converter_helpers.parse_to_timedelta(test_delta_str)

        self.assertIsInstance(delta, datetime.timedelta)
        self.assertEqual(delta, datetime.timedelta(0))

    def test_parse_to_timedelta_or_none_wrong_format(self):
        test_delta_str = 'sd'

        with self.assertRaises(isodate.isoerror.ISO8601Error) as test_parse_to_timedelta_or_none_wrong_format:
            ConversionLayer.converter_helpers.parse_to_timedelta(test_delta_str)

    def test_parse_to_timedelta_or_none_proper_format(self):
        test_delta_str = 'P1D'

        delta = ConversionLayer.converter_helpers.parse_to_timedelta_or_None(test_delta_str)

        self.assertIsInstance(delta, datetime.timedelta)
        self.assertEqual(delta, datetime.timedelta(days=1))

    def test_parse_to_timedelta_or_none_proper_none(self):
        test_delta_str = None

        delta = ConversionLayer.converter_helpers.parse_to_timedelta_or_None(test_delta_str)

        self.assertIsNone(delta)

    def test_check_and_format_any_datetime_to_iso_str_all_cases(self):
        test_case_timedelta = datetime.timedelta(days=1)
        test_case_datetime = datetime.datetime(1, 1, 1, 1, 1)
        test_case_str = 'should stay the same'

        timedelta_str = ConversionLayer.converter_helpers.check_and_format_any_datetime_to_iso_str(test_case_timedelta)
        datetime_str = ConversionLayer.converter_helpers.check_and_format_any_datetime_to_iso_str(test_case_datetime)
        still_str = ConversionLayer.converter_helpers.check_and_format_any_datetime_to_iso_str(test_case_str)

        self.assertEqual(timedelta_str, 'P1D')
        self.assertEqual(datetime_str, '0001-01-01T01:01:00')
        self.assertEqual(still_str, 'should stay the same')

    def test_check_and_format_any_enum_to_str_all_cases(self):
        test_case_enum = AIDM_classes.StopStatus['passing']
        test_case_str = 'should stay the same'

        timedelta_str = ConversionLayer.converter_helpers.check_and_format_any_enum_to_str(test_case_enum)
        still_str = ConversionLayer.converter_helpers.check_and_format_any_enum_to_str(test_case_str)

        self.assertEqual(timedelta_str, 'passing')
        self.assertEqual(still_str, 'should stay the same')