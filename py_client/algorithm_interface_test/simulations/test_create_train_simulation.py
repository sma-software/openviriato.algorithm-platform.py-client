from datetime import datetime
import unittest
from unittest import mock

from py_client.algorithm_interface.algorithm_interface import AlgorithmInterface
from py_client.aidm.aidm_time_window_classes import TimeWindow
import py_client.aidm.aidm_running_time_penalty_classes
import py_client.algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client import algorithm_interface
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestCreateTrainSimulation(unittest.TestCase):
    class PutCreateTrainSimulationMockSession(SessionMockTestBase):
        def put(self, request, json):
            self.__last_body = json
            self.__last_request = request

            return SessionMockFactory.create_response_mock("", 200)

    interface_to_viriato: AlgorithmInterface

    @mock.patch("requests.Session", side_effect=PutCreateTrainSimulationMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch("requests.Session", side_effect=PutCreateTrainSimulationMockSession)
    def test_create_train_simulation(self, mocked_get_obj):
        requested_time_window = TimeWindow(from_time=datetime(2003, 5, 5, 7, 0), to_time=datetime(2003, 5, 5, 9, 0))

        self.interface_to_viriato.create_train_simulation(time_window=requested_time_window)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._PutCreateTrainSimulationMockSession__last_request, get_api_url() + "/services/trains/simulations")
        self.assertDictEqual(session_obj._PutCreateTrainSimulationMockSession__last_body, dict(fromTime="2003-05-05T07:00:00", toTime="2003-05-05T09:00:00"))

    @mock.patch("requests.Session", side_effect=PutCreateTrainSimulationMockSession)
    def test_create_train_simulation_response(self, mocked_get_obj):
        requested_time_window = TimeWindow(from_time=datetime(2003, 5, 5, 7, 0), to_time=datetime(2003, 5, 5, 9, 0))

        response = self.interface_to_viriato.create_train_simulation(time_window=requested_time_window)

        self.assertIsNone(response)

    @mock.patch("requests.Session", side_effect=PutCreateTrainSimulationMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
