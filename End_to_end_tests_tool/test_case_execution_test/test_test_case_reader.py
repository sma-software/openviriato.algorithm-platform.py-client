import unittest
from End_to_end_tests_tool.test_case_execution.test_case import EndToEndTestCase
from End_to_end_tests_tool.test_case_execution import test_case_reader
import os


class TestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.unittest_working_directory = os.getcwd()
        file_directory = os.path.dirname(__file__)
        os.chdir(file_directory)

    def test_test_case_reader_without_arguments(self):
        call_path = 'test_data/calls/00_TestWithNoArguments.json'
        py_call_file_path = 'test_data/py_calls/00_TestWithNoArguments.json'
        expected_file_path = 'test_data/expected/00_TestWithNoArguments.json'

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
        self.assertListEqual(test_case.arguments_for_py_client_method, [])
        self.assertEqual(test_case.name_of_method_to_test, "get_all_nodes")
        self.assertListEqual(test_case.extra_mapping_parameters, [])
        self.assertListEqual(test_case.expected_response_as_json, expected_json)

    def test_test_case_reader_wit_one_argument(self):
        call_path = 'test_data/calls/01_TestWithOneArgument.json'
        py_call_file_path = 'test_data/py_calls/01_TestWithOneArgument.json'
        expected_file_path = 'test_data/expected/01_TestWithOneArgument.json'

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
        self.assertListEqual(test_case.arguments_for_py_client_method, ["161"])
        self.assertEqual(test_case.name_of_method_to_test, "get_node")
        self.assertListEqual(test_case.extra_mapping_parameters, [])
        self.assertDictEqual(test_case.expected_response_as_json, expected_json)

    def test_test_case_reader_with_two_arguments(self):
        call_path = 'test_data/calls/02TestWithTwoArguments.json'
        py_call_file_path = 'test_data/py_calls/02_TestWithTwoArguments.json'
        expected_file_path = 'test_data/expected/02_TestWithTwoArguments.json'

        test_case = test_case_reader.read_test_cases_from_calls_py_calls_and_expected(
            call_path=call_path,
            py_call_file_path=py_call_file_path,
            expected_file_path=expected_file_path)

        expected_json = {'NotAnAIDM': 'True'}

        self.assertIsInstance(test_case, EndToEndTestCase)
        self.assertListEqual(test_case.arguments_for_py_client_method, ['161', '348'])
        self.assertEqual(test_case.name_of_method_to_test, "get_section_tracks_between")
        self.assertListEqual(test_case.extra_mapping_parameters, [])
        self.assertDictEqual(test_case.expected_response_as_json, expected_json)

    def test_test_case_reader_with_one_argument_and_an_extra_parameter(self):
        call_path = 'test_data/calls/03_TestWithOneArgumentAndAnExtraMapping.json'
        py_call_file_path = 'test_data/py_calls/03_TestWithOneArgumentAndAnExtraMapping.json'
        expected_file_path = 'test_data/expected/03_TestWithOneArgumentAndOneExtraMapping.json'

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
        self.assertListEqual(test_case.arguments_for_py_client_method, ["161"])
        self.assertEqual(test_case.name_of_method_to_test, "test_one_mapping_extra")
        self.assertListEqual(test_case.extra_mapping_parameters, ['to_node_id'])
        self.assertDictEqual(test_case.expected_response_as_json, expected_json)

    def test_test_case_reader_with_wrong_path_expressions(self):
        call_path = 'test_data/calls/04_TestWithWrongPathExpressions.json'
        py_call_file_path = 'test_data/py_calls/04_TestWithWrongPathExpressions.json'
        expected_file_path = 'test_data/expected/04_TestWithWrongPathExpressions.json'

        with self.assertRaises(IndexError):
            test_case_reader.read_test_cases_from_calls_py_calls_and_expected(
                call_path=call_path,
                py_call_file_path=py_call_file_path,
                expected_file_path=expected_file_path)

    def tearDown(self) -> None:
        os.chdir(self.unittest_working_directory)
