from datetime import datetime, timedelta
import unittest
from unittest import mock

from py_client.aidm.aidm_train_simulation_classes import (
    AlgorithmTrainSimulationEvent,
    AlgorithmTrainSimulationEventType,
    AlgorithmTrainSimulationRealizationForecast,
)
import py_client.algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestPostponeNextEvent(unittest.TestCase):
    class PostponeNextEventMockSession(SessionMockTestBase):
        def post(self, request, json):
            self.__last_body = json
            self.__last_request = request

            json_string = (
                "{"
                '    "nextRealizableEvent": {'
                '        "id": 2000002, \n'
                '        "type": "passing", \n'
                '        "plannedTime": "2003-05-05T07:34:00", \n'
                '        "forecastDelay": "PT1M", \n'
                '        "forecastTime": "2003-05-05T07:35:00", \n'
                '        "nodeId": 282, \n'
                '        "algorithmTrainId": 1303, \n'
                '        "algorithmTrainPathNodeId": 1301 \n'
                "    }, \n"
                '    "unrealizableEvents": [] \n'
                "}"
            )

            return SessionMockFactory.create_response_mock(json_string, 200)

    @mock.patch("requests.Session", side_effect=PostponeNextEventMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch("requests.Session", side_effect=PostponeNextEventMockSession)
    def test_postpone_next_event(self, mocked_post_obj):
        additional_delay = timedelta(minutes=3)

        self.interface_to_viriato.postpone_next_train_simulation_event(additional_delay)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._PostponeNextEventMockSession__last_request, get_api_url() + "/services/trains/simulations/events/next:postpone")
        self.assertDictEqual(session_obj._PostponeNextEventMockSession__last_body, dict(additionalDelay="PT3M"))

    @mock.patch("requests.Session", side_effect=PostponeNextEventMockSession)
    def test_postpone_next_event_response(self, mocked_post_obj):
        additional_delay = timedelta(minutes=3)
        response = self.interface_to_viriato.postpone_next_train_simulation_event(additional_delay)

        self.assertIsInstance(response, AlgorithmTrainSimulationRealizationForecast)
        self.assertIsInstance(response.next_realizable_event, AlgorithmTrainSimulationEvent)
        self.assertEqual(response.next_realizable_event.id, 2000002)
        self.assertEqual(response.next_realizable_event.type, AlgorithmTrainSimulationEventType.passing)
        self.assertEqual(response.next_realizable_event.planned_time, datetime(year=2003, month=5, day=5, hour=7, minute=34))
        self.assertEqual(response.next_realizable_event.forecast_delay, timedelta(minutes=1))
        self.assertEqual(response.next_realizable_event.forecast_time, datetime(year=2003, month=5, day=5, hour=7, minute=35))
        self.assertEqual(response.next_realizable_event.node_id, 282)
        self.assertEqual(response.next_realizable_event.algorithm_train_id, 1303)
        self.assertEqual(response.next_realizable_event.algorithm_train_path_node_id, 1301)
        self.assertEqual(response.unrealizable_events, [])

    @mock.patch("requests.Session", side_effect=PostponeNextEventMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
