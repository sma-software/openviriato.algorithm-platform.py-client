import unittest
from unittest import mock

import py_client.algorithm_interface_test.test_helper.SessionMockFactory as APISessionMock
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import \
    get_api_url, SessionMockTestBase


class TestGetBoolAlgorithmParameter(unittest.TestCase):
    class GetBoolAlgorithmParameterTestSessionMock(SessionMockTestBase):
        def get(self, request, params):
            self.__last_request = request
            self.__last_body = params

            json__string = ("{\n"
                            "  \"Key\": \"someBoolParameterKey\",\n"
                            "  \"Value\": true\n"
                            "}")
            return APISessionMock.create_response_mock(json__string, 200)

    @mock.patch('requests.Session', side_effect=GetBoolAlgorithmParameterTestSessionMock)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetBoolAlgorithmParameterTestSessionMock)
    def test_get_bool_algorithm_parameter_request(self, mocked_get_obj):
        key = "someBoolParameterKey"

        self.interface_to_viriato.get_bool_algorithm_parameter(key)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetBoolAlgorithmParameterTestSessionMock__last_request, get_api_url() +
                         '/parameters/someBoolParameterKey')
        self.assertDictEqual(session_obj._GetBoolAlgorithmParameterTestSessionMock__last_body, {})

    @mock.patch('requests.Session', side_effect=GetBoolAlgorithmParameterTestSessionMock)
    def test_get_bool_algorithm_parameter_response(self, mocked_get_obj):
        key = "someBoolParameterKey"

        bool_param = self.interface_to_viriato.get_bool_algorithm_parameter(key)

        self.assertIsInstance(bool_param, bool)
        self.assertEqual(bool_param, True)

    @mock.patch('requests.Session', side_effect=GetBoolAlgorithmParameterTestSessionMock)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)


if __name__ == '__main__':
    unittest.main()
