import unittest
from unittest import mock

import py_client.aidm.aidm_algorithm_classes
import py_client.algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client.aidm import aidm_train_path_node_classes
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import \
    get_api_url, \
    SessionMockTestBase


class TestCreateFromTrain(unittest.TestCase):
    class CreateFromTrainTestMockSession(SessionMockTestBase):
        def post(self, request, json):
            self._last_body = json
            self._last_request = request
            json_string = ('{  "ID": 11037, "code": "Test",  "TrainPathNodes": [\n'
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
                           '  "DebugString": "CreateFromTrainTestMockSession"\n'
                           '}')
            return SessionMockFactory.create_response_mock(json_string, 200)

    @mock.patch('requests.Session', side_effect=CreateFromTrainTestMockSession)
    def setUp(self, mocked_post_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=CreateFromTrainTestMockSession)
    def test_create_from_train_request(self, mocked_post_obj):
        train_id = 2060
        node_ids = [11039]

        self.interface_to_viriato.copy_train_and_replace_route(train_id, node_ids)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj.last_request, get_api_url() + '/trains/2060:copy-and-replace-route')
        self.assertDictEqual(session_obj.last_body, dict(routeViaNodeIds=[11039]))

    @mock.patch('requests.Session', side_effect=CreateFromTrainTestMockSession)
    def test_create_from_train_response(self, mocked_post_obj):
        train_id = 2060
        node_ids = [11039]

        created_algorithm_train = self.interface_to_viriato.copy_train_and_replace_route(train_id, node_ids)

        self.assertIsInstance(created_algorithm_train, py_client.aidm.aidm_algorithm_classes.AlgorithmTrain)
        self.assertEqual(11037, created_algorithm_train.id)
        self.assertEqual('CreateFromTrainTestMockSession', created_algorithm_train.debug_string)
        self.assertEqual('Test', created_algorithm_train.code)
        self.assertEqual(len(created_algorithm_train.train_path_nodes), 2)
        self.assertIsInstance(
            created_algorithm_train.train_path_nodes[0],
            aidm_train_path_node_classes.AlgorithmTrainPathNode)
        self.assertEqual(11038, created_algorithm_train.train_path_nodes[0].id)
        self.assertIsNone(created_algorithm_train.train_path_nodes[0].node_track_id)

    @mock.patch('requests.Session', side_effect=CreateFromTrainTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
