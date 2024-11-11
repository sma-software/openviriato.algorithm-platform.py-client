import unittest
from typing import List
from unittest import mock

import py_client.algorithm_interface_test.test_helper.SessionMockFactory as APISessionMock
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestGetIntListAlgorithmParameter(unittest.TestCase):
    class GetIntListAlgorithmParameterTestSessionMock(SessionMockTestBase):
        def get(self, request, params):
            self._last_request = request
            self._last_body = params

            json_string = '{"value":[4211,4711],"key":"integerListParameter"}'
            return APISessionMock.create_response_mock(json_string, 200)

    @mock.patch("requests.Session", side_effect=GetIntListAlgorithmParameterTestSessionMock)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch("requests.Session", side_effect=GetIntListAlgorithmParameterTestSessionMock)
    def test_get_int_algorithm_parameter_request(self, mocked_get_obj):
        key = "someIntParameterKey"

        self.interface_to_viriato.get_int_algorithm_parameter(key)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj.last_request, get_api_url() + "/parameters/someIntParameterKey")
        self.assertDictEqual(session_obj.last_body, {})

    @mock.patch("requests.Session", side_effect=GetIntListAlgorithmParameterTestSessionMock)
    def test_get_int_algorithm_parameter_response_with_value(self, mocked_get_obj):
        key = "someIntListParameterKey"

        response = self.interface_to_viriato.get_int_list_algorithm_parameter(key)

        self.assertIsInstance(response, List)
        self.assertIsInstance(response[0], int)
        self.assertEqual(len(response), 2)

    @mock.patch("requests.Session", side_effect=GetIntListAlgorithmParameterTestSessionMock)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)


if __name__ == "__main__":
    unittest.main()
