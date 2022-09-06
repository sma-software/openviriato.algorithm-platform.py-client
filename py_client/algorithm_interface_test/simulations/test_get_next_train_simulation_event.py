
from datetime import datetime
import unittest
from unittest import mock

from py_client.aidm.aidm_train_simulation_classes import AlgorithmTrainSimulationEventType, AlgorithmTrainSimulationRealizationForecast, AlgorithmTrainSimulationEvent
from py_client.algorithm_interface.algorithm_interface import AlgorithmInterface
import py_client.algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import \
    get_api_url, \
    SessionMockTestBase


class TestGetNextTrainSimulationEvent(unittest.TestCase):
    class GetNextTrainSimulationEventMockSession(SessionMockTestBase):
        def get(self, request, params):
            self.__last_body = params
            self.__last_request = request

            json_string = (" { \n"
                           "    \"nextEvent\": { \n"
                           "        \"id\": 2000000, \n"
                           "        \"trainSimulationTrainPathNodeId\": 1000001, \n"
                           "        \"type\": \"departure\", \n"
                           "        \"absoluteTime\": \"2003-05-05T07:30:00\" \n"
                           "    }, \n"
                           "    \"unrealizableEvents\": []"
                           " }"
                           )

            return SessionMockFactory.create_response_mock(json_string, 200)

    interface_to_viriato: AlgorithmInterface

    @mock.patch('requests.Session', side_effect=GetNextTrainSimulationEventMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetNextTrainSimulationEventMockSession)
    def test_get_next_train_simulation_event(self, mocked_get_obj):

        self.interface_to_viriato.get_next_train_simulation_event()

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetNextTrainSimulationEventMockSession__last_request,
                         get_api_url() + "/services/trains/simulations/events/next")
        self.assertDictEqual(session_obj._GetNextTrainSimulationEventMockSession__last_body,
                             dict())

    @mock.patch('requests.Session', side_effect=GetNextTrainSimulationEventMockSession)
    def test_get_next_train_simulation_event_response(self, mocked_get_obj):

        response = self.interface_to_viriato.get_next_train_simulation_event()

        self.assertIsInstance(
            response,
            AlgorithmTrainSimulationRealizationForecast)

        self.assertIsInstance(
            response.next_event,
            AlgorithmTrainSimulationEvent
        )
        self.assertEqual(
            response.next_event.id,
            2000000
        )
        self.assertEqual(
            response.next_event.train_simulation_train_path_node_id,
            1000001
        )
        self.assertIsInstance(
            response.next_event.type,
            AlgorithmTrainSimulationEventType)
        self.assertEqual(
            response.next_event.type,
            AlgorithmTrainSimulationEventType.departure)
        self.assertIsInstance(
            response.next_event.absolute_time,
            datetime)

        self.assertEqual(response.unrealizable_events, [])

    @mock.patch('requests.Session', side_effect=GetNextTrainSimulationEventMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
