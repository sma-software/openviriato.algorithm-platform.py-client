import unittest

from py_client.aidm import Maybe, StopStatus
from py_client.communication.response_processing import AlgorithmPlatformConversionError
from py_client.conversion.algorithm_platform_json_to_aidm_converter import convert_algorithm_parameter_value_to_enum


class TestAllConverterHelpers(unittest.TestCase):

    def test_maybe_get_value(self):
        maybe = Maybe("Value")

        self.assertTrue(maybe.has_value)
        self.assertEqual(maybe.get_value, "Value")

    def test_maybe_has_no_value(self):
        maybe = Maybe(None)

        self.assertFalse(maybe.has_value)
        with self.assertRaises(ValueError) as value_error_instance:
            _ = maybe.get_value

        self.assertEqual(value_error_instance.exception.args[0], "Tried to get a None-value from a Maybe")

    def test_create_from_json_which_is_none(self):
        maybe = Maybe.create_from_json(None, convert_algorithm_parameter_value_to_enum, StopStatus)

        self.assertFalse(maybe.has_value)
        with self.assertRaises(ValueError) as value_error_instance:
            _ = maybe.get_value

        self.assertEqual(value_error_instance.exception.args[0], "Tried to get a None-value from a Maybe")

    def test_create_from_json_which_is_not_none(self):
        maybe = Maybe.create_from_json("operationalStop", convert_algorithm_parameter_value_to_enum, StopStatus)

        self.assertTrue(maybe.has_value)
        self.assertEqual(maybe.get_value, StopStatus["operational_stop"])

    def test_create_from_json_which_raises_conversion_error(self):
        with self.assertRaises(AlgorithmPlatformConversionError) as conversion_error_instance:
            _ = Maybe.create_from_json("operational_stop", convert_algorithm_parameter_value_to_enum, StopStatus)

        self.assertEqual(
            conversion_error_instance.exception.args[0],
            "<enum 'StopStatus'> does not have a value operational_stop")
