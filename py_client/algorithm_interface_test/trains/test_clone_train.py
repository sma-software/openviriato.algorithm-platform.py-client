import unittest
from unittest import mock

import py_client.aidm.aidm_algorithm_classes
import py_client.algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client import algorithm_interface
from py_client.aidm import aidm_train_path_node_classes
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import \
    get_api_url, \
    SessionMockTestBase


class TestCloneTrain(unittest.TestCase):
    class CloneTrainTestMockSession(SessionMockTestBase):
        # to replace session.post:
        def post(self, request, json):
            self.__last_body = json
            self.__last_request = request
            json_string = ('{  "ID": 11037,  "TrainPathNodes": [\n'
                           '    {\n'
                           '      "ID": 11038,\n'
                           '      "SectionTrackID": null,\n'
                           '      "node_id": 18,\n'
                           '      "node_track_id": null,\n'
                           '      "FormationID": 1187,\n'
                           '      "ArrivalTime": "2003-05-01T00:05:00",\n'
                           '      "DepartureTime": "2003-05-01T00:05:00",\n'
                           '      "MinimumRunTime": null,\n'
                           '      "MinimumStopTime": "P0D",\n'
                           '      "StopStatus": "commercialStop",\n'
                           '      "SequenceNumber": 0\n'
                           '    },\n'
                           '    {\n'
                           '      "ID": 11039,\n'
                           '      "SectionTrackID": 1171,\n'
                           '      "node_id": 10,\n'
                           '      "node_track_id": null,\n'
                           '      "FormationID": null,\n'
                           '      "ArrivalTime": "2003-05-01T00:10:00",\n'
                           '      "DepartureTime": "2003-05-01T00:10:00",\n'
                           '      "MinimumRunTime": "PT5M",\n'
                           '      "MinimumStopTime": "P0D",\n'
                           '      "StopStatus": "commercialStop",\n'
                           '      "SequenceNumber": 1\n'
                           '    }\n'
                           '  ],\n'
                           '  "DebugString": "CloneTrainTestMockSession"\n'
                           '}')
            return SessionMockFactory.create_response_mock(json_string, 200)

    interface_to_viriato: py_client.algorithm_interface.algorithm_interface.AlgorithmInterface

    @mock.patch('requests.Session', side_effect=CloneTrainTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=CloneTrainTestMockSession)
    def test_clone_train_request(self, mocked_get_obj):
        train_id = 2060

        self.interface_to_viriato.clone_train(train_id)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._CloneTrainTestMockSession__last_request, get_api_url() + '/clone-train')
        self.assertDictEqual(session_obj._CloneTrainTestMockSession__last_body, dict(TrainID=2060))

    @mock.patch('requests.Session', side_effect=CloneTrainTestMockSession)
    def test_clone_train_response(self, mocked_get_obj):
        train_id = 0

        test_cloned_algorithm_train = self.interface_to_viriato.clone_train(train_id)

        self.assertIsInstance(test_cloned_algorithm_train, py_client.aidm.aidm_algorithm_classes.AlgorithmTrain)
        self.assertEqual(11037, test_cloned_algorithm_train.id)
        self.assertEqual('CloneTrainTestMockSession', test_cloned_algorithm_train.debug_string)
        self.assertIsInstance(
            test_cloned_algorithm_train.train_path_nodes[0],
            aidm_train_path_node_classes.AlgorithmTrainPathNode)
        self.assertEqual(11038, test_cloned_algorithm_train.train_path_nodes[0].id)

    @mock.patch('requests.Session', side_effect=CloneTrainTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
