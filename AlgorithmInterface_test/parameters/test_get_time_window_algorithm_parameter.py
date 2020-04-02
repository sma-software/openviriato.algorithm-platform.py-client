import datetime
import unittest
from unittest import mock

import AIDMClasses.AIDM_TimeWindow_classes
import AlgorithmInterface_test.test_helper.SessionMockFactory as APISessionMock
from AlgorithmInterface import AlgorithmInterfaceFactory
from AlgorithmInterface_test.test_helper.SessionMockTestBase import \
    get_api_url, SessionMockTestBase


class TestGetTimeWindowParameter(unittest.TestCase):
    class GetTimeWindowParameterTestSessionMock(SessionMockTestBase):
        def get(self, request, params):
            self.__last_request = request
            self.__last_body = params

            json__string = ("{\n"
                            "  \"Key\": \"someTimeWindowParameterKey\",\n"
                            "  \"Value\": {\n"
                            "    \"FromTime\": \"2003-01-01T10:20:30\",\n"
                            "    \"ToTime\": \"2003-01-01T11:00:00\"\n"
                            "  }\n"
                            "}")
            return APISessionMock.create_response_mock(json__string, 200)

    @mock.patch('requests.Session', side_effect=GetTimeWindowParameterTestSessionMock)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = AlgorithmInterfaceFactory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetTimeWindowParameterTestSessionMock)
    def test_get_time_window_algorithm_parameter_request(self, mocked_get_obj):
        key = "someTimeWindowParameterKey"

        self.interface_to_viriato.get_time_window_algorithm_parameter(key)

        session_obj = self.interface_to_viriato._AlgorithmicPlatformInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetTimeWindowParameterTestSessionMock__last_request, get_api_url() +
                         '/parameters/someTimeWindowParameterKey')
        self.assertDictEqual(session_obj._GetTimeWindowParameterTestSessionMock__last_body, {})

    @mock.patch('requests.Session', side_effect=GetTimeWindowParameterTestSessionMock)
    def test_get_time_window_algorithm_parameter_response(self, mocked_get_obj):
        key = "someTimeWindowParameterKey"

        time_window_param = self.interface_to_viriato.get_time_window_algorithm_parameter(key)

        self.assertIsInstance(time_window_param, AIDMClasses.AIDM_TimeWindow_classes.TimeWindow)
        self.assertIsInstance(time_window_param.FromTime, datetime.datetime)
        self.assertEqual(time_window_param.FromTime, datetime.datetime(2003, 1, 1, 10, 20, 30))

    @mock.patch('requests.Session', side_effect=GetTimeWindowParameterTestSessionMock)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)


if __name__ == '__main__':
    unittest.main()
