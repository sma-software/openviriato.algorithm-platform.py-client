import unittest
from unittest import mock

import AIDMClasses.AIDM_Update_classes
import AlgorithmInterface.AlgorithmInterface
import AlgorithmInterface_test.test_helper.SessionMockFactory as SessionMockFactory
from AlgorithmInterface import AlgorithmInterfaceFactory
from AlgorithmInterface_test.test_helper.SessionMockTestBase import \
    get_api_url, SessionMockTestBase


class TestCalculateRunTimes(unittest.TestCase):
    class CalculateRunTimesTestMockSession(SessionMockTestBase):
        def get(self, request, params):
            self.__last_body = params
            self.__last_request = request
            json_string = ("{\n"
                           "  \"TrainID\": 2060,\n"
                           "  \"Times\": [\n"
                           "    {\n"
                           "      \"TrainPathNodeID\": 3880,\n"
                           "      \"ArrivalTime\": \"2003-05-01T07:00:00\",\n"
                           "      \"DepartureTime\": \"2003-05-01T07:00:00\",\n"
                           "      \"MinimumRunTime\": null,\n"
                           "      \"MinimumStopTime\": \"P0D\",\n"
                           "      \"StopStatus\": \"commercialStop\"\n"
                           "    },\n"
                           "    {\n"
                           "      \"TrainPathNodeID\": 4246,\n"
                           "      \"ArrivalTime\": \"2003-05-01T07:01:42\",\n"
                           "      \"DepartureTime\": \"2003-05-01T07:01:42\",\n"
                           "      \"MinimumRunTime\": \"PT1M42S\",\n"
                           "      \"MinimumStopTime\": \"P0D\",\n"
                           "      \"StopStatus\": \"passing\"\n"
                           "    },\n"
                           "    {\n"
                           "      \"TrainPathNodeID\": 4610,\n"
                           "      \"ArrivalTime\": \"2003-05-01T07:04:38\",\n"
                           "      \"DepartureTime\": \"2003-05-01T07:04:38\",\n"
                           "      \"MinimumRunTime\": \"PT2M56S\",\n"
                           "      \"MinimumStopTime\": \"P0D\",\n"
                           "      \"StopStatus\": \"commercialStop\"\n"
                           "    }\n"
                           "  ]\n"
                           "}")

            return SessionMockFactory.create_response_mock(json_string, 200)

    interface_to_viriato: AlgorithmInterface.AlgorithmInterface.AlgorithmicPlatformInterface

    @mock.patch('requests.Session', side_effect=CalculateRunTimesTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = AlgorithmInterfaceFactory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=CalculateRunTimesTestMockSession)
    def test_calculate_run_times_request(self, mocked_get_obj):
        train_id = 2060

        self.interface_to_viriato.calculate_run_times(train_id)

        session_obj = self.interface_to_viriato._AlgorithmicPlatformInterface__communication_layer.currentSession
        self.assertEqual(session_obj._CalculateRunTimesTestMockSession__last_request,
                         get_api_url() + '/calculate-run-times/2060')
        self.assertDictEqual(session_obj._CalculateRunTimesTestMockSession__last_body, {})

    @mock.patch('requests.Session', side_effect=CalculateRunTimesTestMockSession)
    def test_calculate_run_times_response(self, mocked_get_obj):
        train_id = 2060

        updated_train_times = self.interface_to_viriato.calculate_run_times(train_id)

        self.assertIsInstance(updated_train_times, AIDMClasses.AIDM_Update_classes.UpdateTrainTimes)
        self.assertEqual(updated_train_times.TrainID, 2060)
        self.assertIsInstance(updated_train_times.Times, list)
        self.assertIsInstance(updated_train_times.Times[0], AIDMClasses.AIDM_Update_classes.UpdateTrainTimesNode)

    @mock.patch('requests.Session', side_effect=CalculateRunTimesTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
