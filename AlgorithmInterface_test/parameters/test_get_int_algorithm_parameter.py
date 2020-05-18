import unittest
from unittest import mock

import AlgorithmInterface_test.test_helper.SessionMockFactory as APISessionMock
from AlgorithmInterface import AlgorithmInterfaceFactory
from AlgorithmInterface_test.test_helper.SessionMockTestBase import \
    get_api_url, SessionMockTestBase


class TestGetIntAlgorithmParameter(unittest.TestCase):
    class GetIntAlgorithmParameterTestSessionMock(SessionMockTestBase):
        def get(self, request, params):
            self.__last_request = request
            self.__last_body = params

            json__string = ("{\n"
                            "  \"Key\": \"someIntParameterKey\",\n"
                            "  \"Value\": 125\n"
                            "}")
            return APISessionMock.create_response_mock(json__string, 200)

    @mock.patch('requests.Session', side_effect=GetIntAlgorithmParameterTestSessionMock)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = AlgorithmInterfaceFactory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetIntAlgorithmParameterTestSessionMock)
    def test_get_int_algorithm_parameter_request(self, mocked_get_obj):
        key = "someIntParameterKey"

        self.interface_to_viriato.get_int_algorithm_parameter(key)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetIntAlgorithmParameterTestSessionMock__last_request, get_api_url() +
                         '/parameters/someIntParameterKey')
        self.assertDictEqual(session_obj._GetIntAlgorithmParameterTestSessionMock__last_body, {})

    @mock.patch('requests.Session', side_effect=GetIntAlgorithmParameterTestSessionMock)
    def test_get_int_algorithm_parameter_response(self, mocked_get_obj):
        key = "someIntParameterKey"

        int_param = self.interface_to_viriato.get_int_algorithm_parameter(key)

        self.assertIsInstance(int_param, int)
        self.assertEqual(int_param, 125)

    @mock.patch('requests.Session', side_effect=GetIntAlgorithmParameterTestSessionMock)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)


if __name__ == '__main__':
    unittest.main()
