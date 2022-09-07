import unittest
from unittest import mock

from py_client.aidm.aidm_update_classes import UpdateTimesTrain, UpdateTimesTrainPathNode
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.aidm.aidm_running_time_calculation_classes import RunningTimeCalculationResult, RunningTimeCalculationStatus
import py_client.algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestCalculateRunTimes(unittest.TestCase):
    class CalculateRunTimesTestMockSession(SessionMockTestBase):
        def get(self, request, params):
            self.__last_body = params
            self.__last_request = request
            json_string = (
                "{\n"
                '  "status": "ok", \n'
                '  "message": null, \n'
                '  "updateTimesTrain": { \n'
                '    "trainId": 2060,\n'
                '    "update_times_train_path_nodes": [\n'
                "        {\n"
                '            "trainPathNodeId": 3880,\n'
                '            "arrivalTime": "2003-05-01T07:00:00",\n'
                '            "departureTime": "2003-05-01T07:00:00",\n'
                '            "minimumRunTime": null,\n'
                '            "minimumStopTime": "P0D",\n'
                '            "stopStatus": "commercialStop"\n'
                "        },\n"
                "        {\n"
                '            "trainPathNodeId": 4246,\n'
                '            "arrivalTime": "2003-05-01T07:01:42",\n'
                '            "departureTime": "2003-05-01T07:01:42",\n'
                '            "minimumRunTime": "PT1M42S",\n'
                '            "minimumStopTime": "P0D",\n'
                '            "stopStatus": "passing"\n'
                "        },\n"
                "        {\n"
                '            "trainPathNodeId": 4610,\n'
                '            "arrivalTime": "2003-05-01T07:04:38",\n'
                '            "departureTime": "2003-05-01T07:04:38",\n'
                '            "minimumRunTime": "PT2M56S",\n'
                '            "minimumStopTime": "P0D",\n'
                '            "stopStatus": "commercialStop"\n'
                "        }\n"
                "    ]\n"
                "  }\n"
                "}"
            )

            return SessionMockFactory.create_response_mock(json_string, 200)

    @mock.patch("requests.Session", side_effect=CalculateRunTimesTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch("requests.Session", side_effect=CalculateRunTimesTestMockSession)
    def test_calculate_run_times_request(self, mocked_get_obj):
        train_id = 2060

        self.interface_to_viriato.calculate_running_times(train_id)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._CalculateRunTimesTestMockSession__last_request, get_api_url() + "/services/trains/2060:calculate-running-times")
        self.assertDictEqual(session_obj._CalculateRunTimesTestMockSession__last_body, {})

    @mock.patch("requests.Session", side_effect=CalculateRunTimesTestMockSession)
    def test_calculate_run_times_response(self, mocked_get_obj):
        train_id = 2060

        updated_train_times = self.interface_to_viriato.calculate_running_times(train_id)

        self.assertIsInstance(updated_train_times, RunningTimeCalculationResult)
        self.assertIsInstance(updated_train_times.status, RunningTimeCalculationStatus)
        self.assertEqual(updated_train_times.status, RunningTimeCalculationStatus.ok)
        self.assertEqual(updated_train_times.message, None)

        self.assertIsInstance(updated_train_times.update_times_train, UpdateTimesTrain)
        self.assertEqual(updated_train_times.update_times_train.train_id, 2060)

        self.assertIsInstance(updated_train_times.update_times_train.update_times_train_path_nodes, list)
        self.assertIsInstance(updated_train_times.update_times_train.update_times_train_path_nodes[0], UpdateTimesTrainPathNode)

    @mock.patch("requests.Session", side_effect=CalculateRunTimesTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
