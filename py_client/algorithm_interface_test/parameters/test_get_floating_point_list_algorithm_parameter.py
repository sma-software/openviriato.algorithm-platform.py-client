import unittest
from typing import List
from unittest import mock

import py_client.algorithm_interface_test.test_helper.SessionMockFactory as APISessionMock
from py_client.aidm.aidm_floating_point import FloatingPoint
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestGetFloatingPointListAlgorithmParameter(unittest.TestCase):
    class GetFloatingPointListAlgorithmParameterTestSessionMock(SessionMockTestBase):
        def get(self, request, params):
            self._last_request = request
            self._last_body = params

            json_string = '{"value":[{"decimalPlaces":1,"mantissa":4711},{"decimalPlaces":1,"mantissa":4712}],"key":"floatingPointListParameter"}'

            return APISessionMock.create_response_mock(json_string, 200)

    @mock.patch("requests.Session", side_effect=GetFloatingPointListAlgorithmParameterTestSessionMock)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch("requests.Session", side_effect=GetFloatingPointListAlgorithmParameterTestSessionMock)
    def test_get_floating_point_algorithm_parameter_request(self, mocked_get_obj):
        key = "floatingPointListParameterKey"

        self.interface_to_viriato.get_floating_point_list_algorithm_parameter(key)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj.last_request, get_api_url() + "/parameters/floatingPointListParameterKey")
        self.assertDictEqual(session_obj.last_body, {})

    @mock.patch("requests.Session", side_effect=GetFloatingPointListAlgorithmParameterTestSessionMock)
    def test_get_floating_point_algorithm_parameter_response_with_value(self, mocked_get_obj):
        key = "floatingPointListParameterKey"

        floating_point_list = self.interface_to_viriato.get_floating_point_list_algorithm_parameter(key)

        self.assertIsInstance(floating_point_list, List)
        self.assertIsInstance(floating_point_list[0], FloatingPoint)
        self.assertEqual(len(floating_point_list), 2)

    @mock.patch("requests.Session", side_effect=GetFloatingPointListAlgorithmParameterTestSessionMock)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)


if __name__ == "__main__":
    unittest.main()
