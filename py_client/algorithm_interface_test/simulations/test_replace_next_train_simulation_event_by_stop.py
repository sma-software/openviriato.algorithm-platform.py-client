from datetime import datetime
import unittest
from unittest import mock

from py_client.aidm.aidm_train_simulation_classes import (
    AlgorithmTrainSimulationEventType,
    AlgorithmTrainSimulationRealizationForecast,
    AlgorithmTrainSimulationEvent,
)
import py_client.algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestReplaceNextTrainSimulationEventByStop(unittest.TestCase):
    class ReplaceNextTrainSimulationEventByStopMockSession(SessionMockTestBase):
        def post(self, request, json):
            self.__last_body = json
            self.__last_request = request

            json_string = (
                "{ \n"
                '    "nextEvent": { \n'
                '        "id": 2000006, \n'
                '        "trainSimulationTrainPathNodeId": 1000002, \n'
                '        "type": "arrival", \n'
                '        "forecastTime": "2003-05-05T07:05:42" \n'
                "    }, \n"
                '    "unrealizableEvents": [] \n'
                "}"
            )

            return SessionMockFactory.create_response_mock(json_string, 200)

    @mock.patch("requests.Session", side_effect=ReplaceNextTrainSimulationEventByStopMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch("requests.Session", side_effect=ReplaceNextTrainSimulationEventByStopMockSession)
    def test_replace_next_train_simulation_event_by_stop(self, mocked_post_obj):
        self.interface_to_viriato.replace_next_train_simulation_event_by_stop()

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(
            session_obj._ReplaceNextTrainSimulationEventByStopMockSession__last_request,
            get_api_url() + "/services/trains/simulations/events/next:replace-by-stop",
        )
        self.assertDictEqual(session_obj._ReplaceNextTrainSimulationEventByStopMockSession__last_body, {})

    @mock.patch("requests.Session", side_effect=ReplaceNextTrainSimulationEventByStopMockSession)
    def test_replace_next_train_simulation_event_by_stop_response(self, mocked_post_obj):
        response = self.interface_to_viriato.replace_next_train_simulation_event_by_stop()

        self.assertIsInstance(response, AlgorithmTrainSimulationRealizationForecast)
        self.assertIsInstance(response.next_event, AlgorithmTrainSimulationEvent)
        self.assertEqual(response.next_event.id, 2000006)
        self.assertEqual(response.next_event.train_simulation_train_path_node_id, 1000002)
        self.assertIsInstance(response.next_event.type, AlgorithmTrainSimulationEventType)
        self.assertEqual(response.next_event.type, AlgorithmTrainSimulationEventType.arrival)
        self.assertIsInstance(response.next_event.forecast_time, datetime)
        self.assertEqual(response.next_event.forecast_time, datetime(year=2003, month=5, day=5, hour=7, minute=5, second=42))
        self.assertEqual(response.unrealizable_events, [])

    @mock.patch("requests.Session", side_effect=ReplaceNextTrainSimulationEventByStopMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
