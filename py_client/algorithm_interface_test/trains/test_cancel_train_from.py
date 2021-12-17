import unittest
from unittest import mock

import py_client.aidm
import py_client.algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client import algorithm_interface
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import \
    get_api_url, \
    SessionMockTestBase


class TestCancelTrainAfter(unittest.TestCase):
    class CancelTrainAfterTestMockSession(SessionMockTestBase):
        def put(self, request, json):
            self.__last_body = json
            self.__last_request = request
            json_string = (' {"ID": 8116, "code": "1", "TrainPathNodes": [\n'
                           '                        {\n'
                           '                          "ID": 8113,\n'
                           '                          "SectionTrackID": null,\n'
                           '                          "node_id": 7,\n'
                           '                          "node_track_id": 8,\n'
                           '                          "FormationID": 1187,\n'
                           '                          "movementTypeId": null,\n'
                           '                          "ArrivalTime": "2003-09-01T00:10:00",\n'
                           '                          "DepartureTime": "2003-09-01T00:10:00",\n'
                           '                          "MinimumRunTime": null,\n'
                           '                          "MinimumStopTime": "P0D",\n'
                           '                          "StopStatus": "commercialStop",\n'
                           '                          "SequenceNumber": 0\n'
                           '                        },\n'
                           '                        {\n'
                           '                          "ID": 8114,\n'
                           '                          "SectionTrackID": 1175,\n'
                           '                          "node_id": 15,\n'
                           '                          "node_track_id": 16,\n'
                           '                          "FormationID": null,\n'
                           '                          "movementTypeId": null,\n'
                           '                          "ArrivalTime": "2003-09-01T00:14:00",\n'
                           '                          "DepartureTime": "2003-09-01T00:14:00",\n'
                           '                          "MinimumRunTime": "PT4M",\n'
                           '                          "MinimumStopTime": "P0D",\n'
                           '                          "StopStatus": "passing",\n'
                           '                          "SequenceNumber": 1\n'
                           '                        }\n'
                           '                      ],\n'
                           '                      "DebugString": "CancelTrainFromTestMockSession"\n'
                           '                    }')
            return SessionMockFactory.create_response_mock(json_string, 200)

    interface_to_viriato: py_client.algorithm_interface.algorithm_interface.AlgorithmInterface

    @mock.patch('requests.Session', side_effect=CancelTrainAfterTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=CancelTrainAfterTestMockSession)
    def test_cancel_train_after_request(self, mocked_post_obj):
        train_id = 8116
        train_path_node_id = 8114

        self.interface_to_viriato.cancel_train_after(train_id, train_path_node_id)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._CancelTrainAfterTestMockSession__last_request,
                         get_api_url() + '/trains/8116/train-path-nodes/8114:cancel-after')
        self.assertEqual(session_obj._CancelTrainAfterTestMockSession__last_body, {})

    @mock.patch('requests.Session', side_effect=CancelTrainAfterTestMockSession)
    def test_cancel_train_after_response(self, mocked_post_obj):
        train_id = 8116
        train_path_node_id = 8114

        test_algorithm_train = self.interface_to_viriato.cancel_train_after(train_id, train_path_node_id)

        self.assertIsInstance(test_algorithm_train, py_client.aidm.AlgorithmTrain)
        self.assertEqual(test_algorithm_train.id, 8116)
        self.assertEqual(test_algorithm_train.debug_string, 'CancelTrainFromTestMockSession')
        self.assertEqual(test_algorithm_train.code, "1")

        self.assertIsInstance(test_algorithm_train.train_path_nodes, list)
        self.assertIsInstance(test_algorithm_train.train_path_nodes[0], py_client.aidm.AlgorithmTrainPathNode)
        self.assertEqual(test_algorithm_train.train_path_nodes[0].id, 8113)

    @mock.patch('requests.Session', side_effect=CancelTrainAfterTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
