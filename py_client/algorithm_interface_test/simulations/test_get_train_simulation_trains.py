from datetime import datetime, timedelta
import unittest
from py_client.aidm.aidm_enum_classes import StopStatus
from unittest import mock
from typing import Optional

from py_client.algorithm_interface.algorithm_interface import AlgorithmInterface
from py_client.aidm.aidm_train_simulation_classes import AlgorithmTrainSimulationTrain, AlgorithmTrainSimulationTrainPathNode
import py_client.algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestGetTrainSimulationTrains(unittest.TestCase):
    class GetTrainSimulationTrainsMockSession(SessionMockTestBase):
        def get(self, request, params):
            self.__last_body = params
            self.__last_request = request

            json_string = (
                " [ \n"
                " { \n"
                '    "id": 1000000, \n'
                '    "debugString": "FV_100_J03 tt_(SZ)", \n'
                '    "algorithm_train_id": 94865, \n'
                '    "trainPathNodes": [ \n'
                "        { \n"
                '        "id": 1000001, \n'
                '        "algorithmTrainPathNodeId": 1658, \n'
                '        "nodeId": 162, \n'
                '        "plannedArrivalTime": "2003-05-05T07:30:00", \n'
                '        "plannedDepartureTime": "2003-05-05T07:32:00", \n'
                '        "minimumRunTime": null, \n'
                '        "minimumStopTime": "PT2M", \n'
                '        "plannedStopStatus": "commercialStop", \n'
                '        "forecastArrivalDelay": "PT2M", \n'
                '        "forecastDepartureDelay": "PT30S", \n'
                '        "forecastArrivalTime": "2003-05-05T07:32:00", \n'
                '        "forecastDepartureTime": "2003-05-05T07:34:30", \n'
                '        "forecastStopStatus": "commercialStop" \n'
                "    }, \n"
                "    { \n"
                '        "id": 1000002, \n'
                '        "algorithmTrainPathNodeId": 1794, \n'
                '        "nodeId": 282, \n'
                '        "plannedArrivalTime": "2003-05-05T07:31:12", \n'
                '        "plannedDepartureTime": "2003-05-05T07:31:12", \n'
                '        "minimumRunTime": "PT1M12S", \n'
                '        "minimumStopTime": "P0D", \n'
                '        "plannedStopStatus": "passing", \n'
                '        "forecastArrivalDelay": "PT1M", \n'
                '        "forecastDepartureDelay": "P0D", \n'
                '        "forecastArrivalTime": "2003-05-05T07:32:12", \n'
                '        "forecastDepartureTime": "2003-05-05T07:32:12", \n'
                '        "forecastStopStatus": "passing" \n'
                "    }, \n"
                "    { \n"
                '        "id": 1000003, \n'
                '        "algorithmTrainPathNodeId": 2379, \n'
                '        "nodeId": 322, \n'
                '        "plannedArrivalTime": "2003-05-05T07:33:54", \n'
                '        "plannedDepartureTime": "2003-05-05T07:33:54", \n'
                '        "minimumRunTime": "PT2M42S", \n'
                '        "minimumStopTime": "P0D", \n'
                '        "plannedStopStatus": "passing", \n'
                '        "forecastArrivalDelay": "PT1M", \n'
                '        "forecastDepartureDelay": "PT2M", \n'
                '        "forecastArrivalTime": "2003-05-05T07:34:54", \n'
                '        "forecastDepartureTime": "2003-05-05T07:36:54", \n'
                '        "forecastStopStatus": "operationalStop" \n'
                "    } \n"
                "    ] \n"
                " } \n"
                " ] \n"
            )

            return SessionMockFactory.create_response_mock(json_string, 200)

    interface_to_viriato: AlgorithmInterface

    @mock.patch("requests.Session", side_effect=GetTrainSimulationTrainsMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch("requests.Session", side_effect=GetTrainSimulationTrainsMockSession)
    def test_get_train_simulation_trains(self, mocked_get_obj):

        self.interface_to_viriato.get_train_simulation_trains()

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetTrainSimulationTrainsMockSession__last_request, get_api_url() + "/services/trains/simulations/trains")
        self.assertDictEqual(session_obj._GetTrainSimulationTrainsMockSession__last_body, dict())

    @mock.patch("requests.Session", side_effect=GetTrainSimulationTrainsMockSession)
    def test_get_train_simulation_trains_response(self, mocked_get_obj):

        response = self.interface_to_viriato.get_train_simulation_trains()

        self.assertIsInstance(response, list)
        self.assertIsInstance(response[0], AlgorithmTrainSimulationTrain)
        self.assertEqual(response[0].id, 1000000)
        self.assertEqual(response[0].debug_string, "FV_100_J03 tt_(SZ)")
        self.assertIsInstance(response[0].train_path_nodes, list)
        self.assertIsInstance(response[0].train_path_nodes[0], AlgorithmTrainSimulationTrainPathNode)
        self.assertEqual(response[0].train_path_nodes[0].id, 1000001)
        self.assertEqual(response[0].train_path_nodes[0].algorithm_train_path_node_id, 1658)
        self.assertEqual(response[0].train_path_nodes[0].node_id, 162)
        self.assertIsInstance(response[0].train_path_nodes[0].planned_arrival_time, datetime)
        self.assertEqual(response[0].train_path_nodes[0].planned_arrival_time, datetime(year=2003, month=5, day=5, hour=7, minute=30))
        self.assertIsInstance(response[0].train_path_nodes[0].planned_departure_time, datetime)
        self.assertEqual(response[0].train_path_nodes[0].planned_departure_time, datetime(year=2003, month=5, day=5, hour=7, minute=32))
        self.assertIsInstance(response[0].train_path_nodes[0].minimum_run_time, Optional[timedelta])
        self.assertEqual(response[0].train_path_nodes[0].minimum_run_time, None)
        self.assertIsInstance(response[0].train_path_nodes[0].minimum_stop_time, timedelta)
        self.assertEqual(response[0].train_path_nodes[0].minimum_stop_time, timedelta(minutes=2))
        self.assertEqual(response[0].train_path_nodes[0].planned_stop_status, StopStatus.commercial_stop)
        self.assertIsInstance(response[0].train_path_nodes[0].forecast_arrival_delay, timedelta)
        self.assertEqual(response[0].train_path_nodes[0].forecast_arrival_delay, timedelta(minutes=2))
        self.assertIsInstance(response[0].train_path_nodes[0].forecast_departure_delay, timedelta)
        self.assertEqual(response[0].train_path_nodes[0].forecast_departure_delay, timedelta(seconds=30))
        self.assertIsInstance(response[0].train_path_nodes[0].forecast_arrival_time, datetime)
        self.assertEqual(response[0].train_path_nodes[0].forecast_arrival_time, datetime(year=2003, month=5, day=5, hour=7, minute=32))
        self.assertIsInstance(response[0].train_path_nodes[0].forecast_departure_time, datetime)
        self.assertEqual(response[0].train_path_nodes[0].forecast_departure_time, datetime(year=2003, month=5, day=5, hour=7, minute=34, second=30))
        self.assertEqual(response[0].train_path_nodes[0].forecast_stop_status, StopStatus.commercial_stop)

        self.assertIsInstance(response[0].train_path_nodes[1], AlgorithmTrainSimulationTrainPathNode)
        self.assertEqual(response[0].train_path_nodes[1].id, 1000002)
        self.assertEqual(response[0].train_path_nodes[1].algorithm_train_path_node_id, 1794)
        self.assertEqual(response[0].train_path_nodes[1].node_id, 282)
        self.assertIsInstance(response[0].train_path_nodes[1].planned_arrival_time, datetime)
        self.assertEqual(response[0].train_path_nodes[1].planned_arrival_time, datetime(year=2003, month=5, day=5, hour=7, minute=31, second=12))
        self.assertIsInstance(response[0].train_path_nodes[1].planned_departure_time, datetime)
        self.assertEqual(response[0].train_path_nodes[1].planned_departure_time, datetime(year=2003, month=5, day=5, hour=7, minute=31, second=12))
        self.assertIsInstance(response[0].train_path_nodes[1].minimum_run_time, Optional[timedelta])
        self.assertEqual(response[0].train_path_nodes[1].minimum_run_time, timedelta(minutes=1, seconds=12))
        self.assertIsInstance(response[0].train_path_nodes[1].minimum_stop_time, timedelta)
        self.assertEqual(response[0].train_path_nodes[1].minimum_stop_time, timedelta(0))
        self.assertEqual(response[0].train_path_nodes[1].planned_stop_status, StopStatus.passing)
        self.assertIsInstance(response[0].train_path_nodes[1].forecast_arrival_delay, timedelta)
        self.assertEqual(response[0].train_path_nodes[1].forecast_arrival_delay, timedelta(minutes=1))
        self.assertIsInstance(response[0].train_path_nodes[1].forecast_departure_delay, timedelta)
        self.assertEqual(response[0].train_path_nodes[1].forecast_departure_delay, timedelta(0))
        self.assertIsInstance(response[0].train_path_nodes[1].forecast_arrival_time, datetime)
        self.assertEqual(response[0].train_path_nodes[1].forecast_arrival_time, datetime(year=2003, month=5, day=5, hour=7, minute=32, second=12))
        self.assertIsInstance(response[0].train_path_nodes[1].forecast_departure_time, datetime)
        self.assertEqual(response[0].train_path_nodes[1].forecast_departure_time, datetime(year=2003, month=5, day=5, hour=7, minute=32, second=12))
        self.assertEqual(response[0].train_path_nodes[1].forecast_stop_status, StopStatus.passing)

        self.assertIsInstance(response[0].train_path_nodes[2], AlgorithmTrainSimulationTrainPathNode)
        self.assertEqual(response[0].train_path_nodes[2].id, 1000003)
        self.assertEqual(response[0].train_path_nodes[2].algorithm_train_path_node_id, 2379)
        self.assertEqual(response[0].train_path_nodes[2].node_id, 322)
        self.assertIsInstance(response[0].train_path_nodes[2].planned_arrival_time, datetime)
        self.assertEqual(response[0].train_path_nodes[2].planned_arrival_time, datetime(year=2003, month=5, day=5, hour=7, minute=33, second=54))
        self.assertIsInstance(response[0].train_path_nodes[2].planned_departure_time, datetime)
        self.assertEqual(response[0].train_path_nodes[2].planned_departure_time, datetime(year=2003, month=5, day=5, hour=7, minute=33, second=54))
        self.assertIsInstance(response[0].train_path_nodes[2].minimum_run_time, Optional[timedelta])
        self.assertEqual(response[0].train_path_nodes[2].planned_stop_status, StopStatus.passing)
        self.assertEqual(response[0].train_path_nodes[2].minimum_run_time, timedelta(minutes=2, seconds=42))
        self.assertIsInstance(response[0].train_path_nodes[2].minimum_stop_time, timedelta)
        self.assertEqual(response[0].train_path_nodes[2].minimum_stop_time, timedelta(0))
        self.assertIsInstance(response[0].train_path_nodes[2].forecast_arrival_delay, timedelta)
        self.assertEqual(response[0].train_path_nodes[2].forecast_arrival_delay, timedelta(minutes=1))
        self.assertIsInstance(response[0].train_path_nodes[2].forecast_departure_delay, timedelta)
        self.assertEqual(response[0].train_path_nodes[2].forecast_departure_delay, timedelta(minutes=2))
        self.assertIsInstance(response[0].train_path_nodes[2].forecast_arrival_time, datetime)
        self.assertEqual(response[0].train_path_nodes[2].forecast_arrival_time, datetime(year=2003, month=5, day=5, hour=7, minute=34, second=54))
        self.assertIsInstance(response[0].train_path_nodes[2].forecast_departure_time, datetime)
        self.assertEqual(response[0].train_path_nodes[2].forecast_departure_time, datetime(year=2003, month=5, day=5, hour=7, minute=36, second=54))

    @mock.patch("requests.Session", side_effect=GetTrainSimulationTrainsMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
