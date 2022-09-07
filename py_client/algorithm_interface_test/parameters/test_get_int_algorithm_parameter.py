import unittest
from unittest import mock

import py_client.algorithm_interface_test.test_helper.SessionMockFactory as APISessionMock
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestGetIntAlgorithmParameter(unittest.TestCase):
    class GetIntAlgorithmParameterTestSessionMock(SessionMockTestBase):
        def get(self, request, params):
            self._last_request = request
            self._last_body = params

            if "someNullValueIntParameterKey" in request:
                json__string = "{\n" '  "key": "someNullValueIntParameterKey",\n' '  "value": null\n' "}"

            else:
                json__string = "{\n" '  "key": "someIntParameterKey",\n' '  "value": 125\n' "}"
            return APISessionMock.create_response_mock(json__string, 200)

    @mock.patch("requests.Session", side_effect=GetIntAlgorithmParameterTestSessionMock)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch("requests.Session", side_effect=GetIntAlgorithmParameterTestSessionMock)
    def test_get_int_algorithm_parameter_request(self, mocked_get_obj):
        key = "someIntParameterKey"

        self.interface_to_viriato.get_int_algorithm_parameter(key)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj.last_request, get_api_url() + "/parameters/someIntParameterKey")
        self.assertDictEqual(session_obj.last_body, {})

    @mock.patch("requests.Session", side_effect=GetIntAlgorithmParameterTestSessionMock)
    def test_get_int_algorithm_parameter_response_with_value(self, mocked_get_obj):
        key = "someIntParameterKey"

        maybe_with_int_param = self.interface_to_viriato.get_int_algorithm_parameter(key)

        self.assertIsInstance(maybe_with_int_param, int)
        self.assertEqual(maybe_with_int_param, 125)

    @mock.patch("requests.Session", side_effect=GetIntAlgorithmParameterTestSessionMock)
    def test_get_int_algorithm_parameter_response_with_none(self, mocked_get_obj):
        key = "someNullValueIntParameterKey"

        no_value = self.interface_to_viriato.get_int_algorithm_parameter(key)

        self.assertEqual(no_value, None)

    @mock.patch("requests.Session", side_effect=GetIntAlgorithmParameterTestSessionMock)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)


if __name__ == "__main__":
    unittest.main()
