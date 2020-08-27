import os
import unittest
from datetime import datetime

from End_to_end_tests_tool.test_case_execution.test_case_reader import TestCaseReader
from End_to_end_tests_tool.test_case_execution.test_case import EndToEndTestCase
from py_client.aidm.aidm_update_classes import UpdateTrainTimesNode


def assemble_test_file_names(json_file_name: str):
    test_case_directory = os.path.dirname(__file__)
    test_case_data_directory = os.path.join(test_case_directory, 'test_data')
    call_path = os.path.join(test_case_data_directory, 'calls', json_file_name)
    py_call_file_path = os.path.join(test_case_data_directory, 'py_calls', json_file_name)
    expected_file_path = os.path.join(test_case_data_directory, 'expected', json_file_name)
    return call_path, py_call_file_path, expected_file_path


class TestCase(unittest.TestCase):
    __test_case_reader: TestCaseReader

    def setUp(self) -> None:
        self.__test_case_reader = TestCaseReader("dummyUrl")

    def test_test_case_reader_without_arguments(self):
        call_path, py_call_file_path, expected_file_path = assemble_test_file_names(
            '00_TestWithNoArguments.json')

        test_case = self.__test_case_reader.read_test_cases_from_calls_py_calls_and_expected(
            call_path=call_path,
            py_call_file_path=py_call_file_path,
            expected_file_path=expected_file_path)

        expected_json = [{
            "ID": 1,
            "Code": "0085AAT",
            "DebugString": "station:0085AAT",
            "NodeTracks": [
                {
                    "ID": 2,
                    "Code": "1",
                    "DebugString": "stationtrack:0085AAT_1"
                },
                {
                    "ID": 3,
                    "Code": "2",
                    "DebugString": "stationtrack:0085AAT_2"
                }
            ]
        }]

        self.assertIsInstance(test_case, EndToEndTestCase)
        self.assertTrue(test_case.arguments_for_py_client_method_result.is_success)
        self.assertListEqual(test_case.arguments_for_py_client_method_result.result_value, [])
        self.assertEqual(test_case.name_of_method_to_test, "get_all_nodes")
        self.assertListEqual(test_case.expected_response_as_json, expected_json)

    def test_test_case_reader_wit_one_argument_in_parameter_mapping(self):
        call_path, py_call_file_path, expected_file_path = assemble_test_file_names(
            '01_TestWithOneArgumentPythonParameterMapping.json')

        test_case = self.__test_case_reader.read_test_cases_from_calls_py_calls_and_expected(
            call_path=call_path,
            py_call_file_path=py_call_file_path,
            expected_file_path=expected_file_path)

        expected_json = {
            "ID": 161,
            "Code": "0085HEDN",
            "DebugString": "station:0085HEDN",
            "NodeTracks": []
        }

        self.assertIsInstance(test_case, EndToEndTestCase)
        self.assertTrue(test_case.arguments_for_py_client_method_result.is_success)
        self.assertListEqual(test_case.arguments_for_py_client_method_result.result_value, ["161"])
        self.assertEqual(test_case.name_of_method_to_test, "get_node")
        self.assertDictEqual(test_case.expected_response_as_json, expected_json)

    def test_test_case_reader_with_two_arguments_in_parameter_mapping(self):
        call_path, py_call_file_path, expected_file_path = assemble_test_file_names(
            '02_TestWithTwoArgumentsInPythonParameterMapping.json')

        test_case = self.__test_case_reader.read_test_cases_from_calls_py_calls_and_expected(
            call_path=call_path,
            py_call_file_path=py_call_file_path,
            expected_file_path=expected_file_path)

        expected_json = {
            'Code': '900',
            'DebugString': 'sectiontrack:s_70015 n_85ZHDB 900',
            'ID': 1082,
            'SectionCode': '70015',
            'Weight': 10000}

        self.assertIsInstance(test_case, EndToEndTestCase)
        self.assertTrue(test_case.arguments_for_py_client_method_result.is_success)
        self.assertListEqual(test_case.arguments_for_py_client_method_result.result_value, ['161', '348'])
        self.assertEqual(test_case.name_of_method_to_test, "get_section_tracks_between")
        self.assertDictEqual(test_case.expected_response_as_json, expected_json)

    def test_test_case_reader_with_one_argument_and_an_extra_parameter_in_parameter_mapping(self):
        call_path, py_call_file_path, expected_file_path = assemble_test_file_names(
            '03_TestWithOneArgumentAndOneExtraMappingInPythonParameterMapping.json')

        test_case = self.__test_case_reader.read_test_cases_from_calls_py_calls_and_expected(
            call_path=call_path,
            py_call_file_path=py_call_file_path,
            expected_file_path=expected_file_path)

        expected_json = {
            'Code': 'ZUE',
            'DebugString': 'station:0085HEDN',
            'ID': 161,
            'NodeTracks': []
        }

        self.assertIsInstance(test_case, EndToEndTestCase)
        self.assertFalse(test_case.arguments_for_py_client_method_result.is_success)
        self.assertEqual(
            test_case.arguments_for_py_client_method_result.error_message,
            'Extra mapping python_parameter_names: to_node_id')
        self.assertEqual(test_case.name_of_method_to_test, "test_one_mapping_extra")
        self.assertDictEqual(test_case.expected_response_as_json, expected_json)

    def test_test_case_reader_with_unmapped_path_expressions_in_parameter_mapping(self):
        call_path, py_call_file_path, expected_file_path = assemble_test_file_names(
            '04_TestUnmappedPathExpressionsInPythonParameterMapping.json')

        test_case = self.__test_case_reader.read_test_cases_from_calls_py_calls_and_expected(
            call_path=call_path,
            py_call_file_path=py_call_file_path,
            expected_file_path=expected_file_path)

        expected_json = {'Key': 'Value'}

        self.assertIsInstance(test_case, EndToEndTestCase)
        self.assertFalse(test_case.arguments_for_py_client_method_result.is_success)
        self.assertEqual(
            test_case.arguments_for_py_client_method_result.error_message,
            "No value found for jpath $.queryParameters.[0].value")
        self.assertEqual(test_case.name_of_method_to_test, "get_section_track")
        self.assertDictEqual(test_case.expected_response_as_json, expected_json)

    def test_test_case_reader_with_defective_path_expressions_in_parameter_mapping(self):
        call_path, py_call_file_path, expected_file_path = assemble_test_file_names(
            '05_TestDefectivePathExpressionsInPythonParameterMapping.json')

        test_case = self.__test_case_reader.read_test_cases_from_calls_py_calls_and_expected(
            call_path=call_path,
            py_call_file_path=py_call_file_path,
            expected_file_path=expected_file_path)

        expected_json = {
            "ID": 1082,
            "Code": "900",
            "SectionCode": "70015",
            "Weight": 10000,
            "DebugString": "sectiontrack:s_70015 n_85ZHDB 900"
        }

        self.assertIsInstance(test_case, EndToEndTestCase)
        self.assertFalse(test_case.arguments_for_py_client_method_result.is_success)
        self.assertEqual(
            test_case.arguments_for_py_client_method_result.error_message,
            "Can not parse jpath: ?NotAValidPathExpression")
        self.assertEqual(test_case.name_of_method_to_test, "get_section_track")
        self.assertDictEqual(test_case.expected_response_as_json, expected_json)

    def test_test_case_reader_with_ambiguous_path_expressions_in_parameter_mapping(self):
        call_path, py_call_file_path, expected_file_path = assemble_test_file_names(
            '06_TestAmbiguousPathExpressionsInPythonParameterMapping.json')

        test_case = self.__test_case_reader.read_test_cases_from_calls_py_calls_and_expected(
            call_path=call_path,
            py_call_file_path=py_call_file_path,
            expected_file_path=expected_file_path)

        expected_json = {
            "ID": 1588,
            "Code": "9012",
            "SectionCode": "2334",
            "Weight": 9,
            "DebugString": "DebugString"
        }

        self.assertIsInstance(test_case, EndToEndTestCase)
        self.assertFalse(test_case.arguments_for_py_client_method_result.is_success)
        self.assertEqual(
            test_case.arguments_for_py_client_method_result.error_message,
            "Ambiguous jpath: $.queryParameters[*].value")
        self.assertEqual(test_case.name_of_method_to_test, "get_section_tracks_to")
        self.assertDictEqual(test_case.expected_response_as_json, expected_json)

    def test_test_case_reader_with_python_object_mapping(self):
        call_path, py_call_file_path, expected_file_path = assemble_test_file_names('07_TestWithRoutingPoint.json')

        test_case = self.__test_case_reader.read_test_cases_from_calls_py_calls_and_expected(
            call_path=call_path,
            py_call_file_path=py_call_file_path,
            expected_file_path=expected_file_path)

        expected_json = {
            "RoutingEdges":
                [
                    {
                        "NodeID": 161,
                        "EndNodeTrackID": 162,
                        "StartSectionTrackID": 885
                    },
                    {
                        "NodeID": 161,
                        "EndNodeTrackID": 163,
                        "StartSectionTrackID": 887
                    }
                ]
        }

        self.assertIsInstance(test_case, EndToEndTestCase)
        self.assertTrue(test_case.arguments_for_py_client_method_result.is_success)
        self.assertEqual(test_case.name_of_method_to_test, "get_incoming_routing_edges")
        self.assertDictEqual(test_case.expected_response_as_json, expected_json)

    def test_test_case_reader_with_unmapped_path_expressions_in_object_mapping(self):
        call_path, py_call_file_path, expected_file_path = assemble_test_file_names(
            '08_TestUnmappedPathExpressionInPythonObjectMapping.json')

        test_case = self.__test_case_reader.read_test_cases_from_calls_py_calls_and_expected(
            call_path=call_path,
            py_call_file_path=py_call_file_path,
            expected_file_path=expected_file_path)

        expected_json = {'Integer': 1, 'String': '2'}

        self.assertIsInstance(test_case, EndToEndTestCase)
        self.assertFalse(test_case.arguments_for_py_client_method_result.is_success)
        self.assertEqual(
            test_case.arguments_for_py_client_method_result.error_message,
            "No value found for jpath $.urlParameter.[0]")
        self.assertEqual(test_case.name_of_method_to_test, "get_incoming_routing_edges")
        self.assertDictEqual(test_case.expected_response_as_json, expected_json)

    def test_test_case_reader_with_defective_path_expressions_in_object_mapping(self):
        call_path, py_call_file_path, expected_file_path = assemble_test_file_names(
            '09_TestDefectivePathExpressionInPythonObjectMapping.json')

        test_case = self.__test_case_reader.read_test_cases_from_calls_py_calls_and_expected(
            call_path=call_path,
            py_call_file_path=py_call_file_path,
            expected_file_path=expected_file_path)

        expected_json = {"Weight": 10000, "DebugString": "sectiontrack:s_70015 n_85ZHDB 900"}

        self.assertIsInstance(test_case, EndToEndTestCase)
        self.assertFalse(test_case.arguments_for_py_client_method_result.is_success)
        self.assertEqual(
            test_case.arguments_for_py_client_method_result.error_message,
            "Can not parse jpath: $.queryParameter=[0]")
        self.assertEqual(test_case.name_of_method_to_test, "get_incoming_routing_edges")
        self.assertDictEqual(test_case.expected_response_as_json, expected_json)

    def test_test_case_reader_with_ambiguous_path_expressions_in_object_mapping(self):
        call_path, py_call_file_path, expected_file_path = assemble_test_file_names(
            '10_TestAmbiguousPathExpressionInPythonObjectMapping.json')

        test_case = self.__test_case_reader.read_test_cases_from_calls_py_calls_and_expected(
            call_path=call_path,
            py_call_file_path=py_call_file_path,
            expected_file_path=expected_file_path)

        expected_json = {"ID": 1588, "Code": "9012"}

        self.assertIsInstance(test_case, EndToEndTestCase)
        self.assertFalse(test_case.arguments_for_py_client_method_result.is_success)
        self.assertEqual(
            test_case.arguments_for_py_client_method_result.error_message,
            "Ambiguous jpath: $.queryParameters[*].value")
        self.assertEqual(test_case.name_of_method_to_test, "get_incoming_routing_edges")
        self.assertDictEqual(test_case.expected_response_as_json, expected_json)

    def test_test_case_reader_with_missing_class_name_in_object_mapping(self):
        call_path, py_call_file_path, expected_file_path = assemble_test_file_names(
            '11_TestMissingClassNameInPythonObjectMapping.json')

        test_case = self.__test_case_reader.read_test_cases_from_calls_py_calls_and_expected(
            call_path=call_path,
            py_call_file_path=py_call_file_path,
            expected_file_path=expected_file_path)

        expected_json = {"ID": 1588, "Code": "9012"}

        self.assertIsInstance(test_case, EndToEndTestCase)
        self.assertFalse(test_case.arguments_for_py_client_method_result.is_success)
        self.assertEqual(
            test_case.arguments_for_py_client_method_result.error_message,
            "Missing class name for parameter: routing_point")
        self.assertEqual(test_case.name_of_method_to_test, "get_incoming_routing_edges")
        self.assertDictEqual(test_case.expected_response_as_json, expected_json)

    def test_test_case_reader_with_non_convertible_class_in_object_mapping(self):
        call_path, py_call_file_path, expected_file_path = assemble_test_file_names(
            '12_TestNonConvertibleClassInPythonObjectMapping.json')

        test_case = self.__test_case_reader.read_test_cases_from_calls_py_calls_and_expected(
            call_path=call_path,
            py_call_file_path=py_call_file_path,
            expected_file_path=expected_file_path)

        expected_json = {"ID": 1588, "Code": "9012"}

        self.assertIsInstance(test_case, EndToEndTestCase)
        self.assertFalse(test_case.arguments_for_py_client_method_result.is_success)
        self.assertEqual(
            test_case.arguments_for_py_client_method_result.error_message,
            "Class RoutingPointers is not defined for routing_point")
        self.assertEqual(test_case.name_of_method_to_test, "get_incoming_routing_edges")
        self.assertDictEqual(test_case.expected_response_as_json, expected_json)

    def test_test_case_reader_with_test_missing_mapping_in_object_mapping(self):
        call_path, py_call_file_path, expected_file_path = assemble_test_file_names(
            '13_TestMissingMappingForRoutingPointInPythonObjectMapping.json')

        test_case = self.__test_case_reader.read_test_cases_from_calls_py_calls_and_expected(
            call_path=call_path,
            py_call_file_path=py_call_file_path,
            expected_file_path=expected_file_path)

        expected_json = {}

        self.assertIsInstance(test_case, EndToEndTestCase)
        self.assertFalse(test_case.arguments_for_py_client_method_result.is_success)
        self.assertEqual(
            test_case.arguments_for_py_client_method_result.error_message,
            "Missing object mapping for parameter: routing_point")
        self.assertEqual(test_case.name_of_method_to_test, "get_incoming_routing_edges")
        self.assertDictEqual(test_case.expected_response_as_json, expected_json)

    def test_test_case_reader_with_test_multiple_mappings_in_object_mapping(self):
        call_path, py_call_file_path, expected_file_path = assemble_test_file_names(
            '14_TestMultipleMappingsForRoutingPointInPythonObjectMapping.json')

        test_case = self.__test_case_reader.read_test_cases_from_calls_py_calls_and_expected(
            call_path=call_path,
            py_call_file_path=py_call_file_path,
            expected_file_path=expected_file_path)

        expected_json = {"Key": "Value"}

        self.assertIsInstance(test_case, EndToEndTestCase)
        self.assertFalse(test_case.arguments_for_py_client_method_result.is_success)
        self.assertEqual(
            test_case.arguments_for_py_client_method_result.error_message,
            "Multiple object mappings for parameter: routing_point")
        self.assertEqual(test_case.name_of_method_to_test, "get_incoming_routing_edges")
        self.assertDictEqual(test_case.expected_response_as_json, expected_json)

    def test_test_case_reader_with_conversion_failed_in_object_mapping(self):
        call_path, py_call_file_path, expected_file_path = assemble_test_file_names(
            '15_TestConversionFailsInMappingForRoutingPointInPythonObjectMapping.json')

        test_case = self.__test_case_reader.read_test_cases_from_calls_py_calls_and_expected(
            call_path=call_path,
            py_call_file_path=py_call_file_path,
            expected_file_path=expected_file_path)

        expected_json = {"Key": "Value"}

        self.assertIsInstance(test_case, EndToEndTestCase)
        self.assertFalse(test_case.arguments_for_py_client_method_result.is_success)
        self.assertEqual(
            test_case.arguments_for_py_client_method_result.error_message,
            "Conversion failed for class TimeWindow in parameter routing_point")
        self.assertEqual(test_case.name_of_method_to_test, "get_incoming_routing_edges")
        self.assertDictEqual(test_case.expected_response_as_json, expected_json)

    def test_test_case_reader_with_python_parameter_from_json(self):
        call_path, py_call_file_path, expected_file_path = assemble_test_file_names(
            '16_TestPythonParameterFromJson.json')

        test_case = self.__test_case_reader.read_test_cases_from_calls_py_calls_and_expected(
            call_path=call_path,
            py_call_file_path=py_call_file_path,
            expected_file_path=expected_file_path)

        expected_json = {
            "ID": 2060,
            "DebugString": "RVZH_1_1_J03 tt_(G)",
            "TrainPathNodes":
                [
                    {"ID": 1332,
                     "ArrivalTime": "2003-05-01T00:04:00",
                     "DepartureTime": "2003-05-01T00:05:00",
                     "SectionTrackID": None,
                     "NodeID": 18,
                     "NodeTrackID": None,
                     "FormationID": 1187,
                     "MinimumRunTime": None,
                     "MinimumStopTime": "P0D",
                     "StopStatus": "CommercialStop",
                     "SequenceNumber": 0
                     },
                    {
                        "ID": 1696,
                        "ArrivalTime": "2003-05-01T00:10:00",
                        "DepartureTime": "2003-05-01T00:10:00",
                        "SectionTrackID": 1171,
                        "NodeID": 10,
                        "NodeTrackID": None,
                        "FormationID": None,
                        "MinimumRunTime": "PT5M",
                        "MinimumStopTime": "P0D",
                        "StopStatus": "CommercialStop",
                        "SequenceNumber": 1
                    }
                ]
        }

        self.assertIsInstance(test_case, EndToEndTestCase)
        self.assertTrue(test_case.arguments_for_py_client_method_result.is_success)
        self.assertEqual(len(test_case.arguments_for_py_client_method_result.result_value), 2)
        self.assertEqual(test_case.arguments_for_py_client_method_result.result_value[0], "2060")
        self.assertIsInstance(test_case.arguments_for_py_client_method_result.result_value[1], list)
        self.assertEqual(len(test_case.arguments_for_py_client_method_result.result_value[1]), 1)
        self.assertIsInstance(test_case.arguments_for_py_client_method_result.result_value[1][0], UpdateTrainTimesNode)
        self.assertEqual(test_case.arguments_for_py_client_method_result.result_value[1][0].train_path_node_id, 1332)
        self.assertEqual(
            test_case.arguments_for_py_client_method_result.result_value[1][0].arrival_time,
            datetime(2003, 5, 1, 00, 4, 0))
        self.assertEqual(
            test_case.arguments_for_py_client_method_result.result_value[1][0].departure_time,
            datetime(2003, 5, 1, 00, 5, 0))
        self.assertEqual(test_case.name_of_method_to_test, "update_train_times")
        self.assertDictEqual(test_case.expected_response_as_json, expected_json)

    def test_test_case_reader_with_python_parameter_from_json_invalid_class(self):
        call_path, py_call_file_path, expected_file_path = assemble_test_file_names(
            '17_TestPythonParameterFromJsonInvalidClass.json')

        test_case = self.__test_case_reader.read_test_cases_from_calls_py_calls_and_expected(
            call_path=call_path,
            py_call_file_path=py_call_file_path,
            expected_file_path=expected_file_path)

        expected_json = {"some_list": ["an_item"]}

        self.assertIsInstance(test_case, EndToEndTestCase)
        self.assertFalse(test_case.arguments_for_py_client_method_result.is_success)
        self.assertEqual(test_case.arguments_for_py_client_method_result.error_message, 'Factory method ont not found ')
        self.assertDictEqual(test_case.expected_response_as_json, expected_json)

    def test_test_case_reader_with_python_parameter_from_json_misspelled_property(self):
        call_path, py_call_file_path, expected_file_path = assemble_test_file_names(
            '18_TestPythonParameterFromJsonMisspelledProperty.json')

        test_case = self.__test_case_reader.read_test_cases_from_calls_py_calls_and_expected(
            call_path=call_path,
            py_call_file_path=py_call_file_path,
            expected_file_path=expected_file_path)

        expected_json = {"some_list": ["an_item"]}

        self.assertIsInstance(test_case, EndToEndTestCase)
        self.assertFalse(test_case.arguments_for_py_client_method_result.is_success)
        self.assertEqual(
            test_case.arguments_for_py_client_method_result.error_message,
            "Could not convert object json with factory method convert_list_of_json_to_update_train_times_node, "
            "KeyError 'arrival_time'")
        self.assertDictEqual(test_case.expected_response_as_json, expected_json)

    def test_test_case_reader_with_python_parameter_from_json_missing_object_json(self):
        call_path, py_call_file_path, expected_file_path = assemble_test_file_names(
            '20_TestPythonParameterFromJsonMissingObjectJson.json')

        test_case = self.__test_case_reader.read_test_cases_from_calls_py_calls_and_expected(
            call_path=call_path,
            py_call_file_path=py_call_file_path,
            expected_file_path=expected_file_path)

        expected_json = {"some_list": ["an_item"]}

        self.assertIsInstance(test_case, EndToEndTestCase)
        self.assertFalse(test_case.arguments_for_py_client_method_result.is_success)
        self.assertEqual(test_case.arguments_for_py_client_method_result.error_message, "No object json defined")
        self.assertDictEqual(test_case.expected_response_as_json, expected_json)

    def test_test_case_reader_with_python_parameter_from_json_missing_aidm_factory(self):
        call_path, py_call_file_path, expected_file_path = assemble_test_file_names(
            '21_TestPythonParameterFromJsonMissingAIDMFactory.json')

        test_case = self.__test_case_reader.read_test_cases_from_calls_py_calls_and_expected(
            call_path=call_path,
            py_call_file_path=py_call_file_path,
            expected_file_path=expected_file_path)

        expected_json = {"some_list": ["an_item"]}

        self.assertIsInstance(test_case, EndToEndTestCase)
        self.assertFalse(test_case.arguments_for_py_client_method_result.is_success)
        self.assertEqual(test_case.arguments_for_py_client_method_result.error_message, "No aidm_factory defined")
        self.assertDictEqual(test_case.expected_response_as_json, expected_json)

    def test_test_case_reader_with_python_parameter_from_json_non_convertible_class(self):
        call_path, py_call_file_path, expected_file_path = assemble_test_file_names(
            '22_TestPythonParameterFromJsonNonConvertibleClass.json')

        test_case = self.__test_case_reader.read_test_cases_from_calls_py_calls_and_expected(
            call_path=call_path,
            py_call_file_path=py_call_file_path,
            expected_file_path=expected_file_path)

        expected_json = {"some_list": ["an_item"]}

        self.assertIsInstance(test_case, EndToEndTestCase)
        self.assertFalse(test_case.arguments_for_py_client_method_result.is_success)
        self.assertEqual(
            test_case.arguments_for_py_client_method_result.error_message,
            "Could not convert object json with factory method convert_list_of_json_to_update_train_times_node")
        self.assertDictEqual(test_case.expected_response_as_json, expected_json)
