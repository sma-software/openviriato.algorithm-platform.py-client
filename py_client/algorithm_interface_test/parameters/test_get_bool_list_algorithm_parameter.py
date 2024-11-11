import unittest
from typing import List
from unittest import mock

import py_client.algorithm_interface_test.test_helper.SessionMockFactory as APISessionMock
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestGetBoolListAlgorithmParameter(unittest.TestCase):
    class GetBoolListAlgorithmParameterTestSessionMock(SessionMockTestBase):
        def get(self, request, params):
            self.__last_request = request
            self.__last_body = params

            json__string = '{"value":[true,true,false],"key":"booleanListParameter"}'
            return APISessionMock.create_response_mock(json__string, 200)

    @mock.patch("requests.Session", side_effect=GetBoolListAlgorithmParameterTestSessionMock)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch("requests.Session", side_effect=GetBoolListAlgorithmParameterTestSessionMock)
    def test_get_bool_algorithm_parameter_request(self, mocked_get_obj):
        key = "someBoolListParameterKey"

        self.interface_to_viriato.get_bool_list_algorithm_parameter(key)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetBoolListAlgorithmParameterTestSessionMock__last_request, get_api_url() + "/parameters/someBoolListParameterKey")
        self.assertDictEqual(session_obj._GetBoolListAlgorithmParameterTestSessionMock__last_body, {})

    @mock.patch("requests.Session", side_effect=GetBoolListAlgorithmParameterTestSessionMock)
    def test_get_bool_algorithm_parameter_response(self, mocked_get_obj):
        key = "someBoolListParameterKey"

        bool_param = self.interface_to_viriato.get_bool_list_algorithm_parameter(key)

        self.assertIsInstance(bool_param, List)
        self.assertEqual(len(bool_param), 3)
        self.assertIsInstance(bool_param[0], bool)

    @mock.patch("requests.Session", side_effect=GetBoolListAlgorithmParameterTestSessionMock)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)


if __name__ == "__main__":
    unittest.main()
