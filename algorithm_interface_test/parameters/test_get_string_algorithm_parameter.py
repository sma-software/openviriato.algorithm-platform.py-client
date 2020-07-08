import unittest
from unittest import mock

import algorithm_interface_test.test_helper.SessionMockFactory as APISessionMock
from py_client.algorithm_interface import algorithm_interface_factory
from algorithm_interface_test.test_helper.SessionMockTestBase import \
    get_api_url, SessionMockTestBase


class TestGetStringAlgorithmParameter(unittest.TestCase):
    class GetStringAlgorithmParameterTestSessionMock(SessionMockTestBase):
        def get(self, request, params):
            self.__last_request = request
            self.__last_body = params

            json__string = ("{\n"
                            "  \"Key\": \"someStringParameterKey\",\n"
                            "  \"Value\": \"input of string text field\"\n"
                            "}")
            return APISessionMock.create_response_mock(json__string, 200)

    @mock.patch('requests.Session', side_effect=GetStringAlgorithmParameterTestSessionMock)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetStringAlgorithmParameterTestSessionMock)
    def test_get_string_algorithm_parameter_request(self, mocked_get_obj):
        key = "someStringParameterKey"

        self.interface_to_viriato.get_string_algorithm_parameter(key)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetStringAlgorithmParameterTestSessionMock__last_request, get_api_url() +
                         '/parameters/someStringParameterKey')
        self.assertDictEqual(session_obj._GetStringAlgorithmParameterTestSessionMock__last_body, {})

    @mock.patch('requests.Session', side_effect=GetStringAlgorithmParameterTestSessionMock)
    def test_get_string_algorithm_parameter_response(self, mocked_get_obj):
        key = "someStringParameterKey"

        string_param = self.interface_to_viriato.get_string_algorithm_parameter(key)

        self.assertIsInstance(string_param, str)
        self.assertEqual(string_param, "input of string text field")

    @mock.patch('requests.Session', side_effect=GetStringAlgorithmParameterTestSessionMock)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)


if __name__ == '__main__':
    unittest.main()
