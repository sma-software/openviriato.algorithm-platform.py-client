from datetime import datetime, timedelta
import unittest
from py_client.aidm.aidm_enum_classes import StopStatus
from unittest import mock
from typing import Optional

from py_client.algorithm_interface.algorithm_interface import AlgorithmInterface
from py_client.aidm.aidm_train_simulation_classes import AlgorithmTrainSimulationTrain, AlgorithmTrainSimulationTrainPathNode
import py_client.algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import \
    get_api_url, \
    SessionMockTestBase


class TestGetTrainSimulationTrains(unittest.TestCase):
    class GetTrainSimulationTrainsMockSession(SessionMockTestBase):
        def get(self, request, params):
            self.__last_body = params
            self.__last_request = request

            json_string = (" [ \n"
                           " { \n"
                           "    \"id\": 1000000, \n"
                           "    \"trainPathNodes\": [ \n"
                           "        { \n"
                           "        \"id\": 1000001, \n"
                           "        \"nodeId\": 162, \n"
                           "        \"plannedArrivalTime\": \"2003-05-05T07:30:00\", \n"
                           "        \"plannedDepartureTime\": \"2003-05-05T07:32:00\", \n"
                           "        \"minimumRunTime\": null, \n"
                           "        \"minimumStopTime\": \"PT2M\", \n"
                           "        \"plannedStopStatus\": \"commercialStop\", \n"
                           "        \"arrivalDelay\": \"PT2M\", \n"
                           "        \"departureDelay\": \"PT30S\", \n"
                           "        \"estimatedArrivalTime\": \"2003-05-05T07:32:00\", \n"
                           "        \"estimatedDepartureTime\": \"2003-05-05T07:34:30\", \n"
                           "        \"estimatedStopStatus\": \"commercialStop\" \n"
                           "    }, \n"
                           "    { \n"
                           "        \"id\": 1000002, \n"
                           "        \"nodeId\": 282, \n"
                           "        \"plannedArrivalTime\": \"2003-05-05T07:31:12\", \n"
                           "        \"plannedDepartureTime\": \"2003-05-05T07:31:12\", \n"
                           "        \"minimumRunTime\": \"PT1M12S\", \n"
                           "        \"minimumStopTime\": \"P0D\", \n"
                           "        \"plannedStopStatus\": \"passing\", \n"
                           "        \"arrivalDelay\": \"PT1M\", \n"
                           "        \"departureDelay\": \"P0D\", \n"
                           "        \"estimatedArrivalTime\": \"2003-05-05T07:32:12\", \n"
                           "        \"estimatedDepartureTime\": \"2003-05-05T07:32:12\", \n"
                           "        \"estimatedStopStatus\": \"passing\" \n"
                           "    }, \n"
                           "    { \n"
                           "        \"id\": 1000003, \n"
                           "        \"nodeId\": 322, \n"
                           "        \"plannedArrivalTime\": \"2003-05-05T07:33:54\", \n"
                           "        \"plannedDepartureTime\": \"2003-05-05T07:33:54\", \n"
                           "        \"minimumRunTime\": \"PT2M42S\", \n"
                           "        \"minimumStopTime\": \"P0D\", \n"
                           "        \"plannedStopStatus\": \"passing\", \n"
                           "        \"arrivalDelay\": \"PT1M\", \n"
                           "        \"departureDelay\": \"PT2M\", \n"
                           "        \"estimatedArrivalTime\": \"2003-05-05T07:34:54\", \n"
                           "        \"estimatedDepartureTime\": \"2003-05-05T07:36:54\", \n"
                           "        \"estimatedStopStatus\": \"operationalStop\" \n"
                           "    } \n"
                           "    ] \n"
                           " } \n"
                           " ] \n"
                           )

            return SessionMockFactory.create_response_mock(json_string, 200)

    interface_to_viriato: AlgorithmInterface

    @mock.patch('requests.Session', side_effect=GetTrainSimulationTrainsMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetTrainSimulationTrainsMockSession)
    def test_get_train_simulation_trains(self, mocked_get_obj):

        self.interface_to_viriato.get_train_simulation_trains()

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(
            session_obj._GetTrainSimulationTrainsMockSession__last_request,
            get_api_url() + "/services/trains/simulations/trains")
        self.assertDictEqual(
            session_obj._GetTrainSimulationTrainsMockSession__last_body,
            dict())

    @mock.patch('requests.Session', side_effect=GetTrainSimulationTrainsMockSession)
    def test_get_train_simulation_trains_response(self, mocked_get_obj):

        response = self.interface_to_viriato.get_train_simulation_trains()

        self.assertIsInstance(response, list)
        self.assertIsInstance(
            response[0],
            AlgorithmTrainSimulationTrain)
        self.assertEqual(
            response[0].id,
            1000000
        )
        self.assertIsInstance(
            response[0].train_path_nodes,
            list)
        self.assertIsInstance(
            response[0].train_path_nodes[0],
            AlgorithmTrainSimulationTrainPathNode)
        self.assertEqual(
            response[0].train_path_nodes[0].id,
            1000001
        )
        self.assertEqual(
            response[0].train_path_nodes[0].node_id,
            162
        )
        self.assertIsInstance(
            response[0].train_path_nodes[0].planned_arrival_time,
            datetime
            )
        self.assertEqual(
            response[0].train_path_nodes[0].planned_arrival_time,
            datetime(year=2003, month=5, day=5, hour=7, minute=30)
        )
        self.assertIsInstance(
            response[0].train_path_nodes[0].planned_departure_time,
            datetime
        )
        self.assertEqual(
            response[0].train_path_nodes[0].planned_departure_time,
            datetime(year=2003, month=5, day=5, hour=7, minute=32)
        )
        self.assertIsInstance(
            response[0].train_path_nodes[0].minimum_run_time,
            Optional[timedelta]
        )
        self.assertEqual(
            response[0].train_path_nodes[0].minimum_run_time,
            None
        )
        self.assertIsInstance(
            response[0].train_path_nodes[0].minimum_stop_time,
            timedelta
        )
        self.assertEqual(
            response[0].train_path_nodes[0].minimum_stop_time,
            timedelta(minutes=2)
        )
        self.assertEqual(
            response[0].train_path_nodes[0].planned_stop_status,
            StopStatus.commercial_stop
        )
        self.assertIsInstance(
            response[0].train_path_nodes[0].arrival_delay,
            timedelta
        )
        self.assertEqual(
            response[0].train_path_nodes[0].arrival_delay,
            timedelta(minutes=2)
        )
        self.assertIsInstance(
            response[0].train_path_nodes[0].departure_delay,
            timedelta
        )
        self.assertEqual(
            response[0].train_path_nodes[0].departure_delay,
            timedelta(seconds=30)
        )
        self.assertIsInstance(
            response[0].train_path_nodes[0].estimated_arrival_time,
            datetime
        )
        self.assertEqual(
            response[0].train_path_nodes[0].estimated_arrival_time,
            datetime(year=2003, month=5, day=5, hour=7, minute=32)
        )
        self.assertIsInstance(
            response[0].train_path_nodes[0].estimated_departure_time,
            datetime
        )
        self.assertEqual(
            response[0].train_path_nodes[0].estimated_departure_time,
            datetime(year=2003, month=5, day=5, hour=7, minute=34, second=30)
        )
        self.assertEqual(
            response[0].train_path_nodes[0].estimated_stop_status,
            StopStatus.commercial_stop
        )

        self.assertIsInstance(
            response[0].train_path_nodes[1],
            AlgorithmTrainSimulationTrainPathNode)
        self.assertEqual(
            response[0].train_path_nodes[1].id,
            1000002
        )
        self.assertEqual(
            response[0].train_path_nodes[1].node_id,
            282
        )
        self.assertIsInstance(
            response[0].train_path_nodes[1].planned_arrival_time,
            datetime
        )
        self.assertEqual(
            response[0].train_path_nodes[1].planned_arrival_time,
            datetime(year=2003, month=5, day=5, hour=7, minute=31, second=12)
        )
        self.assertIsInstance(
            response[0].train_path_nodes[1].planned_departure_time,
            datetime
        )
        self.assertEqual(
            response[0].train_path_nodes[1].planned_departure_time,
            datetime(year=2003, month=5, day=5, hour=7, minute=31, second=12)
        )
        self.assertIsInstance(
            response[0].train_path_nodes[1].minimum_run_time,
            Optional[timedelta]
        )
        self.assertEqual(
            response[0].train_path_nodes[1].minimum_run_time,
            timedelta(minutes=1, seconds=12)
        )
        self.assertIsInstance(
            response[0].train_path_nodes[1].minimum_stop_time,
            timedelta
        )
        self.assertEqual(
            response[0].train_path_nodes[1].minimum_stop_time,
            timedelta(0)
        )
        self.assertEqual(
            response[0].train_path_nodes[1].planned_stop_status,
            StopStatus.passing
        )
        self.assertIsInstance(
            response[0].train_path_nodes[1].arrival_delay,
            timedelta
        )
        self.assertEqual(
            response[0].train_path_nodes[1].arrival_delay,
            timedelta(minutes=1)
        )
        self.assertIsInstance(
            response[0].train_path_nodes[1].departure_delay,
            timedelta
        )
        self.assertEqual(
            response[0].train_path_nodes[1].departure_delay,
            timedelta(0)
        )
        self.assertIsInstance(
            response[0].train_path_nodes[1].estimated_arrival_time,
            datetime
        )
        self.assertEqual(
            response[0].train_path_nodes[1].estimated_arrival_time,
            datetime(year=2003, month=5, day=5, hour=7, minute=32, second=12)
        )
        self.assertIsInstance(
            response[0].train_path_nodes[1].estimated_departure_time,
            datetime
        )
        self.assertEqual(
            response[0].train_path_nodes[1].estimated_departure_time,
            datetime(year=2003, month=5, day=5, hour=7, minute=32, second=12)
        )
        self.assertEqual(
            response[0].train_path_nodes[1].estimated_stop_status,
            StopStatus.passing
        )

        self.assertIsInstance(
            response[0].train_path_nodes[2],
            AlgorithmTrainSimulationTrainPathNode)
        self.assertEqual(
            response[0].train_path_nodes[2].id,
            1000003
        )
        self.assertEqual(
            response[0].train_path_nodes[2].node_id,
            322
        )
        self.assertIsInstance(
            response[0].train_path_nodes[2].planned_arrival_time,
            datetime
        )
        self.assertEqual(
            response[0].train_path_nodes[2].planned_arrival_time,
            datetime(year=2003, month=5, day=5, hour=7, minute=33, second=54)
        )
        self.assertIsInstance(
            response[0].train_path_nodes[2].planned_departure_time,
            datetime
        )
        self.assertEqual(
            response[0].train_path_nodes[2].planned_departure_time,
            datetime(year=2003, month=5, day=5, hour=7, minute=33, second=54)
        )
        self.assertIsInstance(
            response[0].train_path_nodes[2].minimum_run_time,
            Optional[timedelta]
        )
        self.assertEqual(
            response[0].train_path_nodes[2].planned_stop_status,
            StopStatus.passing
        )
        self.assertEqual(
            response[0].train_path_nodes[2].minimum_run_time,
            timedelta(minutes=2, seconds=42)
        )
        self.assertIsInstance(
            response[0].train_path_nodes[2].minimum_stop_time,
            timedelta
        )
        self.assertEqual(
            response[0].train_path_nodes[2].minimum_stop_time,
            timedelta(0)
        )
        self.assertIsInstance(
            response[0].train_path_nodes[2].arrival_delay,
            timedelta
        )
        self.assertEqual(
            response[0].train_path_nodes[2].arrival_delay,
            timedelta(minutes=1)
        )
        self.assertIsInstance(
            response[0].train_path_nodes[2].departure_delay,
            timedelta
        )
        self.assertEqual(
            response[0].train_path_nodes[2].departure_delay,
            timedelta(minutes=2)
        )
        self.assertIsInstance(
            response[0].train_path_nodes[2].estimated_arrival_time,
            datetime
        )
        self.assertEqual(
            response[0].train_path_nodes[2].estimated_arrival_time,
            datetime(year=2003, month=5, day=5, hour=7, minute=34, second=54)
        )
        self.assertIsInstance(
            response[0].train_path_nodes[2].estimated_departure_time,
            datetime
        )
        self.assertEqual(
            response[0].train_path_nodes[2].estimated_departure_time,
            datetime(year=2003, month=5, day=5, hour=7, minute=36, second=54)
        )

    @mock.patch('requests.Session', side_effect=GetTrainSimulationTrainsMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
