import unittest
from py_client.communication.response_processing import AlgorithmPlatformConversionError

from py_client.conversion.json_to_aidm_converter import TimedeltaProcessor, SingleAttributeProcessor, JsonToAidmConverter, DatetimeProcessor, OptionalProcessor

from parameterized import parameterized
from datetime import datetime, timedelta
from typing import Optional


class TestJsonToAidmConverterProcessorsOrder(unittest.TestCase):
    @parameterized.expand([
            (SingleAttributeProcessor, TimedeltaProcessor, "Error, the SingleAttributeProcessor has to be called before the TimeDeltaProcessor. The TimeDelta is made to perform on strings and not on wrapped dictionaries."),
            (SingleAttributeProcessor, DatetimeProcessor, "Error, the SingleAttributeProcessor has to be called before the DatetimeProcessor. The DatetimeProcessor is made to perform on strings and not on wrapped dictionaries."),
            (SingleAttributeProcessor, OptionalProcessor, "Error, the SingleAttributeProcessor has to be called before the OptionalProcessor. The SingleAttributeProcessor is not created to process None values, but only to unwrap them.")
    ])
    def test_processor_order(self, processor_one: JsonToAidmConverter, processor_two: JsonToAidmConverter, explanation_if_test_fail: str):
        converter = JsonToAidmConverter()
        ordered_list_of_processors = converter._JsonToAidmConverter__processors

        retrieved_processor_one = next(filter(lambda x: isinstance(x, processor_one), ordered_list_of_processors))
        self.assertIsNotNone(retrieved_processor_one, "The processor {} is not present in the list of processors".format(processor_one))

        retrieved_processor_two = next(filter(lambda x: isinstance(x, processor_two), ordered_list_of_processors))
        self.assertIsNotNone(retrieved_processor_two, "The processor {} is not present in the list of processors".format(processor_two))

        self.assertTrue(ordered_list_of_processors.index(retrieved_processor_one) < ordered_list_of_processors.index(retrieved_processor_two), explanation_if_test_fail)

    @parameterized.expand([
        (OptionalProcessor(), SingleAttributeProcessor(), dict(optional_attribute=None), Optional[bool], 'Got a None value for a non-optional type.'),
        (DatetimeProcessor(), SingleAttributeProcessor(), dict(date_time="2022-06-13T17:22:00"), datetime, "Could not parse datetime, invalid datetime format: {'date_time': '2022-06-13T17:22:00'}"),
        (TimedeltaProcessor(), SingleAttributeProcessor(), dict(time_delta="PT3M"), timedelta, "Could not parse duration, invalid duration format: {'time_delta': 'PT3M'}")
    ])
    def test_wrong_processor_order_exceptions(self, instance_of_processor_one: JsonToAidmConverter, instance_of_processor_two: JsonToAidmConverter, attribute_dict: dict, targeted_type: object, expected_error_message: str):
        class JsonToAidmConverterWrongOrder(JsonToAidmConverter):
            def __init__(self):
                self._JsonToAidmConverter__processors = [
                    instance_of_processor_one,
                    instance_of_processor_two
                ]

        processor = JsonToAidmConverterWrongOrder()

        with self.assertRaises(AlgorithmPlatformConversionError) as conversion_error:
            processor.process_json_to_aidm(attribute_dict, targeted_type)
        self.assertEqual(conversion_error.exception.message, expected_error_message)
