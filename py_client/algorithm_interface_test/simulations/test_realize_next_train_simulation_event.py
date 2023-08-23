from datetime import datetime, timedelta
import unittest
from unittest import mock

from py_client.algorithm_interface.algorithm_interface import AlgorithmInterface
from py_client.aidm.aidm_train_simulation_classes import (
    AlgorithmTrainSimulationEventType,
    AlgorithmTrainSimulationEvent,
    AlgorithmTrainSimulationRealizationForecast,
)
import py_client.algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestPostRealizeNextTrainSimulationEvent(unittest.TestCase):
    class PostRealizeNextTrainSimulationEventMockSession(SessionMockTestBase):
        def post(self, request, json):
            self.__last_body = json
            self.__last_request = request

            json_string = (
                "{ \n"
                '   "nextRealizableEvent": {'
                '       "id": 2000001, \n'
                '       "type": "arrival", \n'
                '       "plannedTime": "2003-05-05T07:31:00", \n'
                '       "forecastTime": "2003-05-05T07:31:12", \n'
                '       "forecastDelay": "PT12S", \n'
                '       "nodeId": 282, \n'
                '       "fromSectionTrackId": null, \n'
                '       "nodeTrackId": 323, \n'
                '       "toSectionTrackId": 922, \n'
                '       "algorithmTrainId": 1303, \n'
                '       "algorithmTrainPathNodeId": 1301, \n'
                '       "algorithmTrainPathNodeSequenceNumber": 0 \n'
                "    }, \n "
                '    "unrealizableEvents": []'
                " } "
            )

            return SessionMockFactory.create_response_mock(json_string, 200)

    interface_to_viriato: AlgorithmInterface

    @mock.patch("requests.Session", side_effect=PostRealizeNextTrainSimulationEventMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch("requests.Session", side_effect=PostRealizeNextTrainSimulationEventMockSession)
    def test_get_train_simulation_trains(self, mocked_get_obj):
        self.interface_to_viriato.realize_next_train_simulation_event()

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(
            session_obj._PostRealizeNextTrainSimulationEventMockSession__last_request, get_api_url() + "/services/trains/simulations/events/next:realize"
        )
        self.assertDictEqual(session_obj._PostRealizeNextTrainSimulationEventMockSession__last_body, dict())

    @mock.patch("requests.Session", side_effect=PostRealizeNextTrainSimulationEventMockSession)
    def test_get_train_simulation_trains_response(self, mocked_get_obj):
        response = self.interface_to_viriato.realize_next_train_simulation_event()

        self.assertIsInstance(response, AlgorithmTrainSimulationRealizationForecast)

        self.assertIsInstance(response.next_realizable_event, AlgorithmTrainSimulationEvent)

        self.assertEqual(response.next_realizable_event.id, 2000001)
        self.assertEqual(response.next_realizable_event.type, AlgorithmTrainSimulationEventType.arrival)
        self.assertEqual(response.next_realizable_event.planned_time, datetime(year=2003, month=5, day=5, hour=7, minute=31))
        self.assertEqual(response.next_realizable_event.forecast_time, datetime(year=2003, month=5, day=5, hour=7, minute=31, second=12))
        self.assertEqual(response.next_realizable_event.forecast_delay, timedelta(seconds=12))
        self.assertEqual(response.next_realizable_event.node_id, 282)
        self.assertEqual(response.next_realizable_event.algorithm_train_path_node_id, 1301)

        self.assertEqual(response.unrealizable_events, [])

    @mock.patch("requests.Session", side_effect=PostRealizeNextTrainSimulationEventMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
