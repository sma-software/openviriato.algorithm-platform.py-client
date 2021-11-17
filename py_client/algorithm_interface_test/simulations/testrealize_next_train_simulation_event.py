
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


class TestPostRealizeNextTrainSimulationEvent(unittest.TestCase):
    class PostRealizeNextTrainSimulationEventMockSession(SessionMockTestBase):
        def post(self, request, json):
            self.__last_body = json
            self.__last_request = request

            json_string = ( "{ \n"
                            "   \"id\": 2000001, \n"
                            "   \"trainSimulationTrainPathNodeId\": 1000002, \n"
                            "   \"type\": \"arrival\", \n"
                            "   \"absoluteTime\": \"2003-05-05T07:31:12\" \n"
                            " } "
                            )

            return SessionMockFactory.create_response_mock(json_string, 200)

    interface_to_viriato: py_client.algorithm_interface.algorithm_interface.AlgorithmInterface

    @mock.patch('requests.Session', side_effect=PostRealizeNextTrainSimulationEventMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=PostRealizeNextTrainSimulationEventMockSession)
    def test_get_train_simulation_trains(self, mocked_get_obj):

        self.interface_to_viriato.realize_next_train_simulation_event()

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._PostRealizeNextTrainSimulationEventMockSession__last_request,
                         get_api_url() + "/services/trains/simulations/events/next:realize")
        self.assertDictEqual(session_obj._PostRealizeNextTrainSimulationEventMockSession__last_body,
                             dict())

    @mock.patch('requests.Session', side_effect=PostRealizeNextTrainSimulationEventMockSession)
    def test_get_train_simulation_trains_response(self, mocked_get_obj):

        response = self.interface_to_viriato.realize_next_train_simulation_event()


        self.assertIsInstance(response,
                              py_client.aidm.aidm_train_simulation_classes.AlgorithmTrainSimulationEvent)
        self.assertEqual(
            response.id,
            2000001
        )
        self.assertEqual(
            response.train_simulation_train_path_node_id,
            1000002
        )
        self.assertIsInstance(
            response.absolute_time,
            datetime.datetime
        )
        self.assertIsInstance(
            response.type,
            py_client.aidm.aidm_train_simulation_classes.AlgorithmTrainSimulationEventType
        )




    @mock.patch('requests.Session', side_effect=PostRealizeNextTrainSimulationEventMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
