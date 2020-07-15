import unittest
from End_to_end_tests_tool.test_case_execution.test_case import EndToEndTestCase
from End_to_end_tests_tool.test_case_execution import test_case_reader
import os


def assemble_test_file_names(json_file_name: str):
    test_case_directory = os.path.dirname(__file__)
    test_case_data_directory = os.path.join(test_case_directory, 'test_data')
    call_path = os.path.join(test_case_data_directory, 'calls', json_file_name)
    py_call_file_path = os.path.join(test_case_data_directory, 'py_calls', json_file_name)
    expected_file_path = os.path.join(test_case_data_directory, 'expected', json_file_name)
    return call_path, py_call_file_path, expected_file_path


class TestCase(unittest.TestCase):
    def test_test_case_reader_without_arguments(self):
        call_path, py_call_file_path, expected_file_path = assemble_test_file_names('00_TestWithNoArguments.json')

        test_case = test_case_reader.read_test_cases_from_calls_py_calls_and_expected(
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

    def test_test_case_reader_wit_one_argument(self):
        call_path, py_call_file_path, expected_file_path = assemble_test_file_names('01_TestWithOneArgument.json')

        test_case = test_case_reader.read_test_cases_from_calls_py_calls_and_expected(
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

    def test_test_case_reader_with_two_arguments(self):
        call_path, py_call_file_path, expected_file_path = assemble_test_file_names('02_TestWithTwoArguments.json')

        test_case = test_case_reader.read_test_cases_from_calls_py_calls_and_expected(
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

    def test_test_case_reader_with_one_argument_and_an_extra_parameter(self):
        call_path, py_call_file_path, expected_file_path = assemble_test_file_names(
            '03_TestWithOneArgumentAndOneExtraMapping.json')

        test_case = test_case_reader.read_test_cases_from_calls_py_calls_and_expected(
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
            'Extra mapping parameter: to_node_id')
        self.assertEqual(test_case.name_of_method_to_test, "test_one_mapping_extra")
        self.assertDictEqual(test_case.expected_response_as_json, expected_json)

    def test_test_case_reader_with_unmapped_path_expressions(self):
        call_path, py_call_file_path, expected_file_path = assemble_test_file_names(
            '04_TestUnmappedPathExpressions.json')

        test_case = test_case_reader.read_test_cases_from_calls_py_calls_and_expected(
            call_path=call_path,
            py_call_file_path=py_call_file_path,
            expected_file_path=expected_file_path)

        expected_json = {'Key': 'Value'}

        self.assertIsInstance(test_case, EndToEndTestCase)
        self.assertFalse(test_case.arguments_for_py_client_method_result.is_success)
        self.assertEqual(
            test_case.arguments_for_py_client_method_result.error_message,
            "No argument found for jpath $.queryParameters.[0].value")
        self.assertEqual(test_case.name_of_method_to_test, "get_section_track")
        self.assertDictEqual(test_case.expected_response_as_json, expected_json)

    def test_test_case_reader_with_defective_path_expressions(self):
        call_path, py_call_file_path, expected_file_path = assemble_test_file_names(
            '05_TestDefectivePathExpressions.json')

        test_case = test_case_reader.read_test_cases_from_calls_py_calls_and_expected(
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
            "No argument found for jpath NotAValidPathExpression")
        self.assertEqual(test_case.name_of_method_to_test, "get_section_track")
        self.assertDictEqual(test_case.expected_response_as_json, expected_json)

    def test_test_case_reader_with_ambiguous_path_expressions(self):
        call_path, py_call_file_path, expected_file_path = assemble_test_file_names(
            '06_TestAmbiguousPathExpressions.json')

        test_case = test_case_reader.read_test_cases_from_calls_py_calls_and_expected(
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