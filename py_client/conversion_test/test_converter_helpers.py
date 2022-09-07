import datetime
import unittest

import isodate
from typing import List, Optional, Union
import py_client.conversion.converter_helpers as converter_helpers
from py_client.aidm.aidm_conflict import ConflictType


class TestAllConverterHelpers(unittest.TestCase):
    def test_parse_to_datetime_wrong_format(self):
        test_str = "sd"

        with self.assertRaises(ValueError) as test_parse_to_datetime_wrong_format:
            converter_helpers.parse_to_datetime(test_str)

    def test_parse_to_datetime_wrong_none(self):
        test_none = None

        with self.assertRaises(TypeError) as test_parse_to_datetime_wrong_format:
            converter_helpers.parse_to_datetime(test_none)

    def test_parse_to_datetime_proper_format(self):
        test_date_str = "0001-05-01T01:01:00"

        date = converter_helpers.parse_to_datetime(test_date_str)

        self.assertIsInstance(date, datetime.datetime)
        self.assertEqual(date, datetime.datetime(1, 5, 1, 1, 1))

    def test_parse_to_timedelta_wrong_format(self):
        test_delta_str = "30Seconds"

        with self.assertRaises(ValueError) as test_parse_to_datetime_wrong_format:
            converter_helpers.parse_to_timedelta(test_delta_str)

    def test_parse_to_timedelta_wrong_none(self):
        test_delta_str = None

        with self.assertRaises(TypeError) as test_parse_to_timedelta_wrong_None:
            converter_helpers.parse_to_timedelta(test_delta_str)

    def test_parse_to_timedelta_proper_format(self):
        test_delta_str = "P0D"

        delta = converter_helpers.parse_to_timedelta(test_delta_str)

        self.assertIsInstance(delta, datetime.timedelta)
        self.assertEqual(delta, datetime.timedelta(0))

    def test_parse_to_timedelta_or_none_wrong_format(self):
        test_delta_str = "sd"

        with self.assertRaises(isodate.isoerror.ISO8601Error) as test_parse_to_timedelta_or_none_wrong_format:
            converter_helpers.parse_to_timedelta(test_delta_str)

    def test_parse_to_timedelta_or_none_proper_format(self):
        test_delta_str = "P1D"

        delta = converter_helpers.parse_to_timedelta_or_none(test_delta_str)

        self.assertIsInstance(delta, datetime.timedelta)
        self.assertEqual(delta, datetime.timedelta(days=1))

    def test_parse_to_timedelta_or_none_proper_none(self):
        test_delta_str = None

        delta = converter_helpers.parse_to_timedelta_or_none(test_delta_str)

        self.assertIsNone(delta)

    def test_check_and_format_any_datetime_to_iso_str_all_cases(self):
        test_case_timedelta = datetime.timedelta(days=1)
        test_case_datetime = datetime.datetime(1, 1, 1, 1, 1)
        test_case_str = "should stay the same"

        timedelta_str = converter_helpers.convert_to_datetime_format_or_return_self(test_case_timedelta)
        datetime_str = converter_helpers.convert_to_datetime_format_or_return_self(test_case_datetime)
        still_str = converter_helpers.convert_to_datetime_format_or_return_self(test_case_str)

        self.assertEqual(timedelta_str, "P1D")
        self.assertEqual(datetime_str, "0001-01-01T01:01:00")
        self.assertEqual(still_str, "should stay the same")

    def test_convert_to_snake_case_key(self):
        test_dict = dict(ID=1, nodeID=2, SectionTrackID=123, algorithmSectionTrack=4, AlgorithmNode="test", debugstring="lower", vehicleTypeIDs=124)

        converted_dict = converter_helpers.convert_keys_to_snake_case(test_dict)

        expected_dict = dict(id=1, node_id=2, section_track_id=123, algorithm_section_track=4, algorithm_node="test", debugstring="lower", vehicle_type_ids=124)

        self.assertIsInstance(converted_dict, dict)
        self.assertDictEqual(converted_dict, expected_dict)

    def test_is_optional(self):
        self.assertTrue(converter_helpers.is_optional(Optional[str]))
        self.assertFalse(converter_helpers.is_optional(str))
        self.assertFalse(converter_helpers.is_optional(List[str]))

    def test_is_list_type(self):
        self.assertTrue(converter_helpers.is_list_type(List[int]))
        self.assertFalse(converter_helpers.is_list_type(list))
        self.assertFalse(converter_helpers.is_list_type(Optional[int]))
        self.assertFalse(converter_helpers.is_list_type(int))

    def test_get_type_of_list_element(self):
        self.assertEqual(converter_helpers.get_type_of_list_element(List[int]), int)
        self.assertEqual(converter_helpers.get_type_of_list_element(List[str]), str)

        with self.assertRaises(TypeError) as type_error:
            converter_helpers.get_type_of_list_element(str)
        self.assertEqual(str(type_error.exception), "The targeted type is not a list.")

        with self.assertRaises(TypeError) as type_error:
            converter_helpers.get_type_of_list_element(Optional[str])
        self.assertEqual(str(type_error.exception), "The targeted type is not a list.")

    def test_get_type_of_optional_element(self):
        self.assertEqual(converter_helpers.get_type_of_optional_element(Optional[bool]), bool)
        self.assertEqual(converter_helpers.get_type_of_optional_element(Optional[str]), str)

        with self.assertRaises(TypeError) as type_error:
            converter_helpers.get_type_of_optional_element(List[str])
        self.assertEqual(str(type_error.exception), "The targeted type is not optional.")

        with self.assertRaises(TypeError) as type_error:
            converter_helpers.get_type_of_optional_element(str)
        self.assertEqual(str(type_error.exception), "The targeted type is not optional.")

    def test_is_single_attribute(self):
        self.assertTrue(converter_helpers.is_single_attribute(dict(integer=3), int))
        self.assertTrue(converter_helpers.is_single_attribute(dict(boolean=False), bool))
        self.assertTrue(converter_helpers.is_single_attribute(dict(string="string"), str))
        self.assertTrue(converter_helpers.is_single_attribute(dict(duration=datetime.timedelta(minutes=3)), datetime.timedelta))
        self.assertTrue(converter_helpers.is_single_attribute(dict(date=datetime.datetime(year=2022, month=6, day=13, hour=8, minute=57)), datetime.datetime))

        self.assertFalse(converter_helpers.is_single_attribute(False, bool))
        self.assertFalse(converter_helpers.is_single_attribute(dict(first_attribute=3, second_attribute="str"), Union[bool, str]))
        self.assertFalse(converter_helpers.is_single_attribute(ConflictType.Trafficability, ConflictType))
