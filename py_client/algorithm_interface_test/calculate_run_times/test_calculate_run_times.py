import unittest
from unittest import mock

import py_client.aidm.aidm_update_classes
import py_client.algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client import algorithm_interface
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import \
    get_api_url, SessionMockTestBase


class TestCalculateRunTimes(unittest.TestCase):
    class CalculateRunTimesTestMockSession(SessionMockTestBase):
        def get(self, request, params):
            self.__last_body = params
            self.__last_request = request
            json_string = ("{\n"
                           "  \"trainId\": 2060,\n"
                           "  \"times\": [\n"
                           "    {\n"
                           "      \"trainPathNodeId\": 3880,\n"
                           "      \"arrivalTime\": \"2003-05-01T07:00:00\",\n"
                           "      \"departureTime\": \"2003-05-01T07:00:00\",\n"
                           "      \"minimumRunTime\": null,\n"
                           "      \"minimumStopTime\": \"P0D\",\n"
                           "      \"stopStatus\": \"commercialStop\"\n"
                           "    },\n"
                           "    {\n"
                           "      \"trainPathNodeId\": 4246,\n"
                           "      \"arrivalTime\": \"2003-05-01T07:01:42\",\n"
                           "      \"departureTime\": \"2003-05-01T07:01:42\",\n"
                           "      \"minimumRunTime\": \"PT1M42S\",\n"
                           "      \"minimumStopTime\": \"P0D\",\n"
                           "      \"stopStatus\": \"passing\"\n"
                           "    },\n"
                           "    {\n"
                           "      \"trainPathNodeId\": 4610,\n"
                           "      \"arrivalTime\": \"2003-05-01T07:04:38\",\n"
                           "      \"departureTime\": \"2003-05-01T07:04:38\",\n"
                           "      \"minimumRunTime\": \"PT2M56S\",\n"
                           "      \"minimumStopTime\": \"P0D\",\n"
                           "      \"stopStatus\": \"commercialStop\"\n"
                           "    }\n"
                           "  ]\n"
                           "}")

            return SessionMockFactory.create_response_mock(json_string, 200)

    interface_to_viriato: py_client.algorithm_interface.algorithm_interface.AlgorithmInterface

    @mock.patch('requests.Session', side_effect=CalculateRunTimesTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=CalculateRunTimesTestMockSession)
    def test_calculate_run_times_request(self, mocked_get_obj):
        train_id = 2060

        self.interface_to_viriato.calculate_run_times(train_id)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._CalculateRunTimesTestMockSession__last_request,
                         get_api_url() + '/calculate-run-times/2060')
        self.assertDictEqual(session_obj._CalculateRunTimesTestMockSession__last_body, {})

    @mock.patch('requests.Session', side_effect=CalculateRunTimesTestMockSession)
    def test_calculate_run_times_response(self, mocked_get_obj):
        train_id = 2060

        updated_train_times = self.interface_to_viriato.calculate_run_times(train_id)

        self.assertIsInstance(updated_train_times, py_client.aidm.aidm_update_classes.UpdateTrainTimes)
        self.assertEqual(updated_train_times.train_id, 2060)
        self.assertIsInstance(updated_train_times.times, list)
        self.assertIsInstance(updated_train_times.times[0], py_client.aidm.aidm_update_classes.UpdateTrainTimesNode)

    @mock.patch('requests.Session', side_effect=CalculateRunTimesTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
