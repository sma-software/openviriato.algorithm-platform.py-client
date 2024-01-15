import unittest
from datetime import datetime
from unittest import mock

import py_client.algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client.aidm import AlgorithmTrainSimulationCreationArguments, AlgorithmTrainSimulationPerimeter
from py_client.aidm.aidm_time_window_classes import TimeWindow
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface.algorithm_interface import AlgorithmInterface
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
    def test_create_train_simulation_full_simulation_arguments(self, mocked_get_obj):
        requested_time_window = TimeWindow(from_time=datetime(2003, 5, 5, 7, 0), to_time=datetime(2003, 5, 5, 9, 0))
        ignore_timetable_conflicts = True
        algorithm_train_simulation_perimeter = AlgorithmTrainSimulationPerimeter(node_ids=[1213, 225, 3658, 489])
        algorithm_train_simulation_creation_arguments = (
            AlgorithmTrainSimulationCreationArguments(time_window=requested_time_window)
            .with_ignore_timetable_conflicts(ignore_timetable_conflicts=ignore_timetable_conflicts)
            .with_perimeter(perimeter=algorithm_train_simulation_perimeter)
        )

        self.interface_to_viriato.create_train_simulation(algorithm_train_simulation_creation_arguments=algorithm_train_simulation_creation_arguments)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        request_body = session_obj._PutCreateTrainSimulationMockSession__last_body
        self.assertEqual(session_obj._PutCreateTrainSimulationMockSession__last_request, get_api_url() + "/services/trains/simulations")
        self.assertDictEqual(request_body["timeWindow"], dict(fromTime="2003-05-05T07:00:00", toTime="2003-05-05T09:00:00"))
        self.assertTrue(request_body["ignoreTimetableConflicts"])
        self.assertEqual(request_body["perimeter"], dict(nodeIds=[1213, 225, 3658, 489]))

    @mock.patch("requests.Session", side_effect=PutCreateTrainSimulationMockSession)
    def test_create_train_simulation_minimal_simulation_arguments(self, mocked_get_obj):
        requested_time_window = TimeWindow(from_time=datetime(2003, 5, 5, 7, 0), to_time=datetime(2003, 5, 5, 9, 0))
        algorithm_train_simulation_creation_arguments = AlgorithmTrainSimulationCreationArguments(time_window=requested_time_window)

        self.interface_to_viriato.create_train_simulation(algorithm_train_simulation_creation_arguments=algorithm_train_simulation_creation_arguments)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        request_body = session_obj._PutCreateTrainSimulationMockSession__last_body
        self.assertEqual(session_obj._PutCreateTrainSimulationMockSession__last_request, get_api_url() + "/services/trains/simulations")
        self.assertDictEqual(request_body["timeWindow"], dict(fromTime="2003-05-05T07:00:00", toTime="2003-05-05T09:00:00"))
        self.assertIsNone(request_body.get("ignoreTimetableConflicts"))
        self.assertIsNone(request_body.get("perimeter"))

    @mock.patch("requests.Session", side_effect=PutCreateTrainSimulationMockSession)
    def test_create_train_simulation_response(self, mocked_get_obj):
        requested_time_window = TimeWindow(from_time=datetime(2003, 5, 5, 7, 0), to_time=datetime(2003, 5, 5, 9, 0))
        ignore_timetable_conflicts = False
        algorithm_train_simulation_creation_arguments = AlgorithmTrainSimulationCreationArguments(time_window=requested_time_window)

        response = self.interface_to_viriato.create_train_simulation(
            algorithm_train_simulation_creation_arguments=algorithm_train_simulation_creation_arguments
        )

        self.assertIsNone(response)

    @mock.patch("requests.Session", side_effect=PutCreateTrainSimulationMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
