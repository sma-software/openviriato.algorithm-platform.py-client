import unittest
from unittest import mock

import py_client.aidm.aidm_algorithm_classes
from py_client import algorithm_interface
import algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client.aidm import aidm_train_path_node_classes
from py_client.algorithm_interface import algorithm_interface_factory
from algorithm_interface_test.test_helper.SessionMockTestBase import \
    get_api_url, \
    SessionMockTestBase


class TestCancelTrainTo(unittest.TestCase):
    class CancelTrainToTestMockSession(SessionMockTestBase):
        # to replace session.post:
        def post(self, request, json):
            self.__last_body = json
            self.__last_request = request
            json_string = (' {  "ID": 8120,  "TrainPathNodes": [\n'
                           '                {\n'
                           '                  "ID": 8118,\n'
                           '                  "SectionTrackID": null,\n'
                           '                  "node_id": 15,\n'
                           '                  "node_track_id": 16,\n'
                           '                  "FormationID": 1187,\n'
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
    def test_cancel_train_to_request(self, mocked_get_obj):
        test_dict = dict(trainPathNodeID=8118)

        self.interface_to_viriato.cancel_train_to(test_dict['trainPathNodeID'])

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._CancelTrainToTestMockSession__last_request, get_api_url() + '/cancel-train-to')
        self.assertDictEqual(session_obj._CancelTrainToTestMockSession__last_body, test_dict)

    @mock.patch('requests.Session', side_effect=CancelTrainToTestMockSession)
    def test_cancel_train_to_response(self, mocked_get_obj):
        train_path_node_id = 0

        test_algorithm_train = self.interface_to_viriato.cancel_train_to(train_path_node_id)

        self.assertIsInstance(test_algorithm_train, py_client.aidm.aidm_algorithm_classes.AlgorithmTrain)
        self.assertEqual(test_algorithm_train.id, 8120)
        self.assertEqual(test_algorithm_train.debug_string, 'CancelTrainToTestMockSession')
        self.assertIsInstance(test_algorithm_train.train_path_nodes[0],
                              aidm_train_path_node_classes.AlgorithmTrainPathNode)
        self.assertEqual(test_algorithm_train.train_path_nodes[0].id, 8118)

    @mock.patch('requests.Session', side_effect=CancelTrainToTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
