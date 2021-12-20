import unittest
from unittest import mock
from datetime import datetime, timedelta

from py_client.algorithm_interface.algorithm_interface import AlgorithmInterface
from py_client.algorithm_interface import algorithm_interface_factory
import py_client.algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase
from py_client.aidm import AlgorithmTrain, AlgorithmTrainPathNode, StopStatus

class TestUpdateMovementType(unittest.TestCase):
    class PutUpdateMovementTypeMockSession(SessionMockTestBase):
        def put(self, request, json):
            self.__last_body = json
            self.__last_request = request

            json_string = ( "{ \n"
                            "   \"id\": 6736, \n"
                            "   \"trainPathNodes\": [\n"
                            "       { \n"
                            "           \"id\": 6732, \n"
                            "           \"sectionTrackId\": null, \n"
                            "           \"nodeId\": 162, \n"
                            "           \"nodeTrackId\": null, \n"
                            "           \"formationId\": 1223, \n"
                            "           \"movementTypeId\": null, \n"
                            "           \"arrivalTime\": \"2003-05-12T06:03:54\", \n"
                            "           \"departureTime\": \"2003-05-12T06:03:54\", \n"
                            "           \"minimumRunTime\": null, \n"
                            "           \"minimumStopTime\": \"P0D\", \n"
                            "           \"stopStatus\": \"commercialStop\", \n"
                            "           \"sequenceNumber\": 0\n"
                            "       },\n"
                            "       {\n"
                            "           \"id\": 6733, \n"
                            "           \"sectionTrackId\": 921, \n"
                            "           \"nodeId\": 282, \n"
                            "           \"nodeTrackId\": null, \n"
                            "           \"formationId\": 1223, \n"
                            "           \"movementTypeId\": 1220, \n"
                            "           \"arrivalTime\": \"2003-05-12T06:13:54\", \n"
                            "           \"departureTime\": \"2003-05-12T06:13:54\", \n"
                            "           \"minimumRunTime\": \"PT10M\", \n"
                            "           \"minimumStopTime\": \"P0D\", \n"
                            "           \"stopStatus\": \"passing\", \n"
                            "           \"sequenceNumber\": 1 \n"
                            "       }, \n"
                            "       { \n"
                            "           \"id\": 6734, \n"
                            "           \"sectionTrackId\": 922, \n"
                            "           \"nodeId\": 322, \n"
                            "           \"nodeTrackId\": null, \n"
                            "           \"formationId\": 1223, \n"
                            "           \"movementTypeId\": 1220, \n"
                            "           \"arrivalTime\": \"2003-05-12T06:23:54\", \n"
                            "           \"departureTime\": \"2003-05-12T06:23:54\", \n"
                            "           \"minimumRunTime\": \"PT10M\", \n"
                            "           \"minimumStopTime\": \"P0D\", \n"
                            "           \"stopStatus\": \"passing\", \n"
                            "           \"sequenceNumber\": 2 \n"
                            "       }, \n"
                            "       {\n"
                            "           \"id\": 6735, \n"
                            "           \"sectionTrackId\": 923, \n"
                            "           \"nodeId\": 436, \n"
                            "           \"nodeTrackId\": null, \n"
                            "           \"formationId\": null, \n"
                            "           \"movementTypeId\": null, \n"
                            "           \"arrivalTime\": \"2003-05-12T06:33:54\", \n"
                            "           \"departureTime\": \"2003-05-12T06:33:54\", \n"
                            "           \"minimumRunTime\": \"PT10M\", \n"
                            "           \"minimumStopTime\": \"P0D\", \n"
                            "           \"stopStatus\": \"commercialStop\", \n"
                            "           \"sequenceNumber\": 3 \n"
                            "       }\n"
                            "],\n"
                            "\"code\": \"FV_200_J03\", \n"
                            "\"debugString\": \"FV_200_J03 tt_(SZ)\" \n"
                            "}")

            return SessionMockFactory.create_response_mock(json_string, 200)

        interface_to_viriato: AlgorithmInterface

    @mock.patch('requests.Session', side_effect=PutUpdateMovementTypeMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=PutUpdateMovementTypeMockSession)
    def test_update_movement_type(self, mocked_get_obj):
        train_id = 6736
        movement_type_id = 1220,
        from_train_path_node_id = 6733,
        to_train_path_node_id = None

        self.interface_to_viriato.update_movement_type(movement_type_id, train_id, from_train_path_node_id, to_train_path_node_id)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession

        self.assertEqual(session_obj._PutUpdateMovementTypeMockSession__last_request,
                         get_api_url() + "/trains/{}/train-path-nodes:update-movement-type".format(train_id))

        self.assertDictEqual(session_obj._PutUpdateMovementTypeMockSession__last_body,
                             dict(movementTypeId = movement_type_id,
                                  fromTrainPathNodeId = from_train_path_node_id,
                                  toTrainPathNodeId = to_train_path_node_id))


    @mock.patch('requests.Session', side_effect=PutUpdateMovementTypeMockSession)
    def test_update_movement_type_response(self, mocked_get_obj):
        train_id = 6736
        movement_type_id = 1220,
        from_train_path_node_id = 6733,
        to_train_path_node_id = None

        movement_type = self.interface_to_viriato.update_movement_type(movement_type_id, train_id, from_train_path_node_id, to_train_path_node_id)

        self.assertIsInstance(movement_type, AlgorithmTrain)
        self.assertEqual(movement_type.id, 6736)
        self.assertIsInstance(movement_type.train_path_nodes, list)

        self.assertIsInstance(movement_type.train_path_nodes[0], AlgorithmTrainPathNode)
        self.assertEqual(movement_type.train_path_nodes[0].id, 6732)
        self.assertEqual(movement_type.train_path_nodes[0].movement_type_id, None)

        self.assertIsInstance(movement_type.train_path_nodes[2], AlgorithmTrainPathNode)
        self.assertEqual(movement_type.train_path_nodes[2].id, 6734)
        self.assertEqual(movement_type.train_path_nodes[2].movement_type_id, 1220)

        self.assertIsInstance(movement_type.train_path_nodes[3], AlgorithmTrainPathNode)
        self.assertEqual(movement_type.train_path_nodes[3].id, 6735)
        self.assertEqual(movement_type.train_path_nodes[3].movement_type_id, None)

    @mock.patch('requests.Session', side_effect=PutUpdateMovementTypeMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)