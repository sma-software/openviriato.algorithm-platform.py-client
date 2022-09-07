from datetime import datetime
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
                '   "nextEvent": {'
                '       "id": 2000001, \n'
                '       "trainSimulationTrainPathNodeId": 1000002, \n'
                '       "type": "arrival", \n'
                '       "absoluteTime": "2003-05-05T07:31:12" \n'
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

        self.assertIsInstance(response.next_event, AlgorithmTrainSimulationEvent)

        self.assertEqual(response.next_event.id, 2000001)
        self.assertEqual(response.next_event.train_simulation_train_path_node_id, 1000002)
        self.assertIsInstance(response.next_event.absolute_time, datetime)
        self.assertIsInstance(response.next_event.type, AlgorithmTrainSimulationEventType)

        self.assertEqual(response.unrealizable_events, [])

    @mock.patch("requests.Session", side_effect=PostRealizeNextTrainSimulationEventMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
