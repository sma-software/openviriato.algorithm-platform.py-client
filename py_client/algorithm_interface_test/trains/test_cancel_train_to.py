import unittest
from unittest import mock

import py_client.aidm.aidm_algorithm_classes
import py_client.algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
import py_client.aidm
from py_client import algorithm_interface
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import \
    get_api_url, \
    SessionMockTestBase


class TestCancelTrainTo(unittest.TestCase):
    class CancelTrainToTestMockSession(SessionMockTestBase):
        def put(self, request, json):
            self.__last_body = json
            self.__last_request = request
            json_string = (' {  "ID": 8120, "code":"123", "TrainPathNodes": [\n'
                           '                {\n'
                           '                  "ID": 8118,\n'
                           '                  "SectionTrackID": null,\n'
                           '                  "node_id": 15,\n'
                           '                  "node_track_id": 16,\n'
                           '                  "FormationID": 1187,\n'
                           '                  "movementTypeId": null,\n'
                           '                  "ArrivalTime": "2003-09-01T00:14:00",\n'
                           '                  "DepartureTime": "2003-09-01T00:14:00",\n'
                           '                  "MinimumRunTime": null,\n'
                           '                  "MinimumStopTime": "P0D",\n'
                           '                  "StopStatus": "passing",\n'
                           '                  "SequenceNumber": 0\n'
                           '                },\n'
                           '                {\n'
                           '                  "ID": 8119,\n'
                           '                  "SectionTrackID": 1174,\n'
                           '                  "node_id": 10,\n'
                           '                  "node_track_id": 12,\n'
                           '                  "FormationID": null,\n'
                           '                  "movementTypeId": null,\n'
                           '                  "ArrivalTime": "2003-09-01T00:19:00",\n'
                           '                  "DepartureTime": "2003-09-01T00:19:00",\n'
                           '                  "MinimumRunTime": "PT5M",\n'
                           '                  "MinimumStopTime": "P0D",\n'
                           '                  "StopStatus": "commercialStop",\n'
                           '                  "SequenceNumber": 1\n'
                           '                }\n'
                           '                ],\n'
                           '                "DebugString": "CancelTrainToTestMockSession"\n'
                           '             }')
            return SessionMockFactory.create_response_mock(json_string, 200)

    interface_to_viriato: py_client.algorithm_interface.algorithm_interface.AlgorithmInterface

    @mock.patch('requests.Session', side_effect=CancelTrainToTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=CancelTrainToTestMockSession)
    def test_cancel_train_before_request(self, mocked_get_obj):
        train_id = 8120
        train_path_node_id = 8118

        self.interface_to_viriato.cancel_train_before(train_id, train_path_node_id)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(
            session_obj._CancelTrainToTestMockSession__last_request,
            get_api_url() + '/trains/8120/train-path-nodes/8118:cancel-before')
        self.assertDictEqual(session_obj._CancelTrainToTestMockSession__last_body, {})

    @mock.patch('requests.Session', side_effect=CancelTrainToTestMockSession)
    def test_cancel_train_before_response(self, mocked_get_obj):
        train_id = 8120
        train_path_node_id = 8118

        test_algorithm_train = self.interface_to_viriato.cancel_train_before(train_id, train_path_node_id)

        self.assertIsInstance(test_algorithm_train, py_client.aidm.AlgorithmTrain)
        self.assertEqual(test_algorithm_train.id, 8120)
        self.assertEqual(test_algorithm_train.debug_string, 'CancelTrainToTestMockSession')
        self.assertEqual(test_algorithm_train.code, '123')

        self.assertIsInstance(test_algorithm_train.train_path_nodes, list)
        self.assertIsInstance(test_algorithm_train.train_path_nodes[0], py_client.aidm.AlgorithmTrainPathNode)
        self.assertEqual(test_algorithm_train.train_path_nodes[0].id, 8118)

    @mock.patch('requests.Session', side_effect=CancelTrainToTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
