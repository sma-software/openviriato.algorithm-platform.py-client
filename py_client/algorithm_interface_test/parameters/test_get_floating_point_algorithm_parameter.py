import unittest
from unittest import mock

import py_client.algorithm_interface_test.test_helper.SessionMockFactory as APISessionMock
from py_client.aidm.aidm_floating_point import FloatingPoint
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import \
    get_api_url, SessionMockTestBase


class TestGetFloatingPointAlgorithmParameter(unittest.TestCase):
    class GetFloatingPointAlgorithmParameterTestSessionMock(SessionMockTestBase):
        def get(self, request, params):
            self._last_request = request
            self._last_body = params

            if "floatingPointParameterWithNoneValueKey" in self._last_request:
                json_string = (
                    "{\n"
                    "  \"value\": null,\n"
                    "  \"key\": \"floatingPointParameter\"\n"
                    "}"
                )
            else:
                json_string = (
                    "{\n"
                    "  \"value\": {\n"
                    "    \"decimalPlaces\": 2,\n"
                    "    \"mantissa\": 4711\n"
                    "  },\n"
                    "  \"key\": \"floatingPointParameter\"\n"
                    "}"
                )

            return APISessionMock.create_response_mock(json_string, 200)

    @mock.patch('requests.Session', side_effect=GetFloatingPointAlgorithmParameterTestSessionMock)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetFloatingPointAlgorithmParameterTestSessionMock)
    def test_get_floating_point_algorithm_parameter_request(self, mocked_get_obj):
        key = "floatingPointParameterKey"

        self.interface_to_viriato.get_floating_point_algorithm_parameter(key)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj.last_request, get_api_url() + '/parameters/floatingPointParameterKey')
        self.assertDictEqual(session_obj.last_body, {})

    @mock.patch('requests.Session', side_effect=GetFloatingPointAlgorithmParameterTestSessionMock)
    def test_get_floating_point_algorithm_parameter_response_with_value(self, mocked_get_obj):
        key = "floatingPointParameterKey"

        floating_point = self.interface_to_viriato.get_floating_point_algorithm_parameter(key)

        self.assertIsInstance(floating_point, FloatingPoint)
        self.assertEqual(floating_point.decimal_places, 2)
        self.assertEqual(floating_point.mantissa, 4711)

    @mock.patch('requests.Session', side_effect=GetFloatingPointAlgorithmParameterTestSessionMock)
    def test_get_floating_point_algorithm_parameter_response_with_none_value(self, mocked_get_obj):
        key = "floatingPointParameterWithNoneValueKey"

        none_floating_point = self.interface_to_viriato.get_floating_point_algorithm_parameter(key)

        self.assertIsNone(none_floating_point)

    @mock.patch('requests.Session', side_effect=GetFloatingPointAlgorithmParameterTestSessionMock)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)


if __name__ == '__main__':
    unittest.main()
