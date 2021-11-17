import datetime
import unittest
from unittest import mock

import py_client.aidm.aidm_train_simulation_classes
import py_client.algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client import algorithm_interface
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import \
    get_api_url, \
    SessionMockTestBase


class TestGetTrainSimulationTrains(unittest.TestCase):
    class GetTrainSimulationTrainsMockSession(SessionMockTestBase):
        def get(self, request, params):
            self.__last_body = params
            self.__last_request = request

            json_string = (" [ \n"
                           " { \n"
                           "    \"id\": 1000000, \n"
                           "    \"trainPathNodes\": [ \n"
                           "        { \n"
                           "        \"id\": 1000001, \n"
                           "        \"nodeId\": 162, \n"
                           "        \"arrivalTime\": \"2003-05-05T07:30:00\", \n"
                           "        \"departureTime\": \"2003-05-05T07:30:00\" \n"
                           "    }, \n"
                           "    { \n"
                           "        \"id\": 1000002, \n"
                           "        \"nodeId\": 282, \n"
                           "        \"arrivalTime\": \"2003-05-05T07:31:12\", \n"
                           "        \"departureTime\": \"2003-05-05T07:31:12\" \n"
                           "    }, \n"
                           "    { \n"
                           "        \"id\": 1000003, \n"
                           "        \"nodeId\": 322, \n"
                           "        \"arrivalTime\": \"2003-05-05T07:33:54\", \n"
                           "        \"departureTime\": \"2003-05-05T07:33:54\" \n"
                           "    } \n"
                           "    ] \n"
                           " } \n"
                           " ] \n"
                           )

            return SessionMockFactory.create_response_mock(json_string, 200)

    interface_to_viriato: py_client.algorithm_interface.algorithm_interface.AlgorithmInterface

    @mock.patch('requests.Session', side_effect=GetTrainSimulationTrainsMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetTrainSimulationTrainsMockSession)
    def test_get_train_simulation_trains(self, mocked_get_obj):

        self.interface_to_viriato.get_train_simulation_trains()

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetTrainSimulationTrainsMockSession__last_request,
                         get_api_url() + "/services/trains/simulations/trains")
        self.assertDictEqual(session_obj._GetTrainSimulationTrainsMockSession__last_body,
                             dict())

    @mock.patch('requests.Session', side_effect=GetTrainSimulationTrainsMockSession)
    def test_get_train_simulation_trains_response(self, mocked_get_obj):

        response = self.interface_to_viriato.get_train_simulation_trains()

        self.assertIsInstance(response, list)
        self.assertIsInstance(
            response[0],
            py_client.aidm.aidm_train_simulation_classes.AlgorithmTrainSimulationTrain)
        self.assertEqual(
            response[0].id,
            1000000
        )
        self.assertIsInstance(
            response[0].train_path_nodes,
            list)
        self.assertIsInstance(
            response[0].train_path_nodes[0],
            py_client.aidm.aidm_train_simulation_classes.AlgorithmTrainSimulationTrainPathNode)
        self.assertEqual(
            response[0].train_path_nodes[0].id,
            1000001
        )
        self.assertEqual(
            response[0].train_path_nodes[0].node_id,
            162
        )
        self.assertIsInstance(
            response[0].train_path_nodes[0].arrival_time,
            datetime.datetime
            )
        self.assertIsInstance(
            response[0].train_path_nodes[0].departure_time,
            datetime.datetime
        )
        self.assertIsInstance(
            response[0].train_path_nodes[1],
            py_client.aidm.aidm_train_simulation_classes.AlgorithmTrainSimulationTrainPathNode)
        self.assertEqual(
            response[0].train_path_nodes[1].id,
            1000002
        )
        self.assertEqual(
            response[0].train_path_nodes[1].node_id,
            282
        )
        self.assertIsInstance(
            response[0].train_path_nodes[1].arrival_time,
            datetime.datetime
        )
        self.assertIsInstance(
            response[0].train_path_nodes[1].departure_time,
            datetime.datetime
        )
        self.assertIsInstance(
            response[0].train_path_nodes[2],
            py_client.aidm.aidm_train_simulation_classes.AlgorithmTrainSimulationTrainPathNode)
        self.assertEqual(
            response[0].train_path_nodes[2].id,
            1000003
        )
        self.assertEqual(
            response[0].train_path_nodes[2].node_id,
            322
        )
        self.assertIsInstance(
            response[0].train_path_nodes[2].arrival_time,
            datetime.datetime
        )
        self.assertIsInstance(
            response[0].train_path_nodes[2].departure_time,
            datetime.datetime
        )



    @mock.patch('requests.Session', side_effect=GetTrainSimulationTrainsMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
