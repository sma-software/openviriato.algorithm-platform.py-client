import unittest
from datetime import datetime, timedelta
from unittest import mock

import py_client.algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client.aidm.aidm_train_simulation_classes import (
    AlgorithmTrainSimulationEventType,
    AlgorithmTrainSimulationRealizationForecast,
    AlgorithmTrainSimulationEvent,
)
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestUpdateNodeTrackOfFutureEvent(unittest.TestCase):
    class UpdateNodeTrackOfFutureSimulationEventMockSession(SessionMockTestBase):
        def put(self, request, json):
            self.__last_body = json
            self.__last_request = request

            response_json_string = (
                "{ \n"
                '    "nextRealizableEvent": { \n'
                '       "id": 2000006, \n'
                '       "type": "arrival", \n'
                '       "plannedTime": "2003-05-05T07:05:00", \n'
                '       "forecastTime": "2003-05-05T07:05:42", \n'
                '       "forecastDelay": "PT42S", \n'
                '       "nodeId": 282, \n'
                '       "fromSectionTrackId": null, \n'
                '       "nodeTrackId": 323, \n'
                '       "toSectionTrackId": 922, \n'
                '       "algorithmTrainId": 1303, \n'
                '       "algorithmTrainPathNodeId": 1301, \n'
                '       "algorithmTrainPathNodeSequenceNumber": 0 \n'
                "    }, \n"
                '    "unrealizableEvents": [] \n'
                "}"
            )

            return SessionMockFactory.create_response_mock(response_json_string, 200)

    @mock.patch("requests.Session", side_effect=UpdateNodeTrackOfFutureSimulationEventMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch("requests.Session", side_effect=UpdateNodeTrackOfFutureSimulationEventMockSession)
    def test_(self, mocked_put_obj):
        self.interface_to_viriato.update_node_track_of_future_event(2000006, 324)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(
            session_obj._UpdateNodeTrackOfFutureSimulationEventMockSession__last_request,
            get_api_url() + "/services/trains/simulations/events/2000006:update-node-track",
        )
        self.assertDictEqual(session_obj._UpdateNodeTrackOfFutureSimulationEventMockSession__last_body, {"nodeTrackId": 324})

    @mock.patch("requests.Session", side_effect=UpdateNodeTrackOfFutureSimulationEventMockSession)
    def test_replace_next_train_simulation_event_by_stop_response(self, mocked_put_obj):
        response = self.interface_to_viriato.update_node_track_of_future_event(2000006, 324)

        self.assertIsInstance(response, AlgorithmTrainSimulationRealizationForecast)
        self.assertIsInstance(response.next_realizable_event, AlgorithmTrainSimulationEvent)
        self.assertEqual(response.next_realizable_event.id, 2000006)
        self.assertIsInstance(response.next_realizable_event.type, AlgorithmTrainSimulationEventType)
        self.assertEqual(response.next_realizable_event.type, AlgorithmTrainSimulationEventType.arrival)
        self.assertIsInstance(response.next_realizable_event.planned_time, datetime)
        self.assertEqual(response.next_realizable_event.planned_time, datetime(year=2003, month=5, day=5, hour=7, minute=5))
        self.assertIsInstance(response.next_realizable_event.forecast_time, datetime)
        self.assertEqual(response.next_realizable_event.forecast_time, datetime(year=2003, month=5, day=5, hour=7, minute=5, second=42))
        self.assertIsInstance(response.next_realizable_event.forecast_delay, timedelta)
        self.assertEqual(response.next_realizable_event.forecast_delay, timedelta(seconds=42))
        self.assertEqual(response.next_realizable_event.node_id, 282)
        self.assertEqual(response.next_realizable_event.algorithm_train_id, 1303)
        self.assertEqual(response.next_realizable_event.algorithm_train_path_node_id, 1301)
        self.assertEqual(response.unrealizable_events, [])

    @mock.patch("requests.Session", side_effect=UpdateNodeTrackOfFutureSimulationEventMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
