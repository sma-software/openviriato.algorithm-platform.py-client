from datetime import datetime, timedelta
import unittest
from unittest import mock

from py_client.aidm.aidm_train_simulation_classes import (
    AlgorithmTrainSimulationEventType,
    AlgorithmTrainSimulationEvent,
)
from py_client.algorithm_interface.algorithm_interface import AlgorithmInterface
import py_client.algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestGetTrainSimulationEvents(unittest.TestCase):
    class GetTrainSimulationEventsMockSession(SessionMockTestBase):
        def get(self, request, params):
            self.__last_body = params
            self.__last_request = request

            json_string = (
                "[ \n"
                "   { \n"
                '        "id": 2000000, \n'
                '        "type": "arrival", \n'
                '        "plannedTime": "2003-05-05T07:00:00", \n'
                '        "forecastDelay": "P0D", \n'
                '        "forecastTime": "2003-05-05T07:00:00", \n'
                '        "nodeId": 322, \n'
                '        "algorithmTrainId": 1303, \n'
                '        "algorithmTrainPathNodeId": 1300 \n'
                "   }, \n"
                "   { \n"
                '        "id": 2000001, \n'
                '        "type": "departure", \n'
                '        "plannedTime": "2003-05-05T07:02:00", \n'
                '        "forecastDelay": "PT1M", \n'
                '        "forecastTime": "2003-05-05T07:03:00", \n'
                '        "nodeId": 322, \n'
                '        "algorithmTrainId": 1303, \n'
                '        "algorithmTrainPathNodeId": 1300 \n'
                "   }, \n"
                "   { \n"
                '        "id": 2000002, \n'
                '        "type": "passing", \n'
                '        "plannedTime": "2003-05-05T07:04:42", \n'
                '        "forecastDelay": "PT30S", \n'
                '        "forecastTime": "2003-05-05T07:05:12", \n'
                '        "nodeId": 282, \n'
                '        "algorithmTrainId": 1303, \n'
                '        "algorithmTrainPathNodeId": 1301 \n'
                "   } \n"
                "]"
            )

            return SessionMockFactory.create_response_mock(json_string, 200)

    interface_to_viriato: AlgorithmInterface

    @mock.patch("requests.Session", side_effect=GetTrainSimulationEventsMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch("requests.Session", side_effect=GetTrainSimulationEventsMockSession)
    def test_get_train_simulation_events(self, mocked_get_obj):

        self.interface_to_viriato.get_train_simulation_events()

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetTrainSimulationEventsMockSession__last_request, get_api_url() + "/services/trains/simulations/events")
        self.assertDictEqual(session_obj._GetTrainSimulationEventsMockSession__last_body, dict())

    @mock.patch("requests.Session", side_effect=GetTrainSimulationEventsMockSession)
    def test_get_train_simulation_events_response(self, mocked_get_obj):

        response = self.interface_to_viriato.get_train_simulation_events()

        self.assertIsInstance(response, list)

        self.assertIsInstance(response[0], AlgorithmTrainSimulationEvent)
        self.assertEqual(response[0].id, 2000000)
        self.assertIsInstance(response[0].type, AlgorithmTrainSimulationEventType)
        self.assertEqual(response[0].type, AlgorithmTrainSimulationEventType.arrival)
        self.assertIsInstance(response[0].planned_time, datetime)
        self.assertEqual(response[0].planned_time, datetime(year=2003, month=5, day=5, hour=7))
        self.assertIsInstance(response[0].forecast_delay, timedelta)
        self.assertEqual(response[0].forecast_delay, timedelta(0))
        self.assertIsInstance(response[0].forecast_time, datetime)
        self.assertEqual(response[0].forecast_time, datetime(year=2003, month=5, day=5, hour=7))
        self.assertEqual(response[0].node_id, 322)
        self.assertEqual(response[0].algorithm_train_id, 1303)
        self.assertEqual(response[0].algorithm_train_path_node_id, 1300)

        self.assertIsInstance(response[1], AlgorithmTrainSimulationEvent)
        self.assertEqual(response[1].id, 2000001)
        self.assertIsInstance(response[1].type, AlgorithmTrainSimulationEventType)
        self.assertEqual(response[1].type, AlgorithmTrainSimulationEventType.departure)
        self.assertIsInstance(response[1].planned_time, datetime)
        self.assertEqual(response[1].planned_time, datetime(year=2003, month=5, day=5, hour=7, minute=2))
        self.assertIsInstance(response[1].forecast_delay, timedelta)
        self.assertEqual(response[1].forecast_delay, timedelta(minutes=1))
        self.assertIsInstance(response[1].forecast_time, datetime)
        self.assertEqual(response[1].forecast_time, datetime(year=2003, month=5, day=5, hour=7, minute=3))
        self.assertEqual(response[1].node_id, 322)
        self.assertEqual(response[1].algorithm_train_id, 1303)
        self.assertEqual(response[1].algorithm_train_path_node_id, 1300)

        self.assertIsInstance(response[2], AlgorithmTrainSimulationEvent)
        self.assertEqual(response[2].id, 2000002)
        self.assertIsInstance(response[2].type, AlgorithmTrainSimulationEventType)
        self.assertEqual(response[2].type, AlgorithmTrainSimulationEventType.passing)
        self.assertIsInstance(response[2].planned_time, datetime)
        self.assertEqual(response[2].planned_time, datetime(year=2003, month=5, day=5, hour=7, minute=4, second=42))
        self.assertIsInstance(response[2].forecast_delay, timedelta)
        self.assertEqual(response[2].forecast_delay, timedelta(seconds=30))
        self.assertIsInstance(response[2].forecast_time, datetime)
        self.assertEqual(response[2].forecast_time, datetime(year=2003, month=5, day=5, hour=7, minute=5, second=12))
        self.assertEqual(response[2].node_id, 282)
        self.assertEqual(response[2].algorithm_train_id, 1303)
        self.assertEqual(response[2].algorithm_train_path_node_id, 1301)

    @mock.patch("requests.Session", side_effect=GetTrainSimulationEventsMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
