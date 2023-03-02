import unittest
from unittest import mock

from py_client.algorithm_interface.algorithm_interface import AlgorithmInterface
import py_client.algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestGetTrainSimulationEventsEmpty(unittest.TestCase):
    class GetTrainSimulationEventsMockSession(SessionMockTestBase):
        def get(self, request, params):
            self.__last_body = params
            self.__last_request = request

            json_string = "[]"

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
        self.assertListEqual(response, [])

    @mock.patch("requests.Session", side_effect=GetTrainSimulationEventsMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
