import unittest
from typing import List
from unittest import mock

import py_client.algorithm_interface_test.test_helper.SessionMockFactory as APISessionMock
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestGetStringListAlgorithmParameter(unittest.TestCase):
    class GetStringListAlgorithmParameterTestSessionMock(SessionMockTestBase):
        def get(self, request, params):
            self.__last_request = request
            self.__last_body = params

            json__string = '{"value":["input","string","list"],"key":"stringListParameter"}'
            return APISessionMock.create_response_mock(json__string, 200)

    @mock.patch("requests.Session", side_effect=GetStringListAlgorithmParameterTestSessionMock)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch("requests.Session", side_effect=GetStringListAlgorithmParameterTestSessionMock)
    def test_get_string_algorithm_parameter_request(self, mocked_get_obj):
        key = "someStringParameterKey"

        self.interface_to_viriato.get_string_list_algorithm_parameter(key)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetStringListAlgorithmParameterTestSessionMock__last_request, get_api_url() + "/parameters/someStringParameterKey")

    @mock.patch("requests.Session", side_effect=GetStringListAlgorithmParameterTestSessionMock)
    def test_get_string_list_algorithm_parameter_response(self, mocked_get_obj):
        key = "someStringParameterKey"

        string_list_param = self.interface_to_viriato.get_string_list_algorithm_parameter(key)

        self.assertIsInstance(string_list_param, List)
        self.assertIsInstance(string_list_param[0], str)
        self.assertEqual(len(string_list_param), 3)
        self.assertEqual(string_list_param[0], "input")
        self.assertEqual(string_list_param[1], "string")
        self.assertEqual(string_list_param[2], "list")

    @mock.patch("requests.Session", side_effect=GetStringListAlgorithmParameterTestSessionMock)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)


if __name__ == "__main__":
    unittest.main()
