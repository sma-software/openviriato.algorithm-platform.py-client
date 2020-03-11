import unittest
from unittest import mock

import AlgorithmInterface.AlgorithmInterface
import unit_testing.test_AlgorithmInterface_with_mock.SessionMockFactory as SessionMockFactory
from AIDMClasses import AIDM_classes
from AlgorithmInterface import AlgorithmInterfaceFactory
from unit_testing.test_AlgorithmInterface_with_mock.unit_testing_with_mock_helpers import get_api_url, \
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
                           '                  "NodeID": 15,\n'
                           '                  "NodeTrackID": 16,\n'
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
                           '                  "NodeID": 10,\n'
                           '                  "NodeTrackID": 12,\n'
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

    interface_to_viriato: AlgorithmInterface.AlgorithmInterface.AlgorithmicPlatformInterface

    @mock.patch('requests.Session', side_effect=CancelTrainToTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = AlgorithmInterfaceFactory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=CancelTrainToTestMockSession)
    def test_cancel_train_to_request(self, mocked_get_obj):
        test_dict = dict(trainPathNodeID=8118)

        self.interface_to_viriato.cancel_train_to(test_dict['trainPathNodeID'])

        session_obj = self.interface_to_viriato._AlgorithmicPlatformInterface__communication_layer.currentSession
        self.assertEqual(session_obj._CancelTrainToTestMockSession__last_request, get_api_url() + '/cancel-train-to')
        self.assertDictEqual(session_obj._CancelTrainToTestMockSession__last_body, test_dict)

    @mock.patch('requests.Session', side_effect=CancelTrainToTestMockSession)
    def test_cancel_train_to_response(self, mocked_get_obj):
        train_path_node_id = 0

        test_algorithm_train = self.interface_to_viriato.cancel_train_to(train_path_node_id)

        self.assertIsInstance(test_algorithm_train, AIDM_classes.AlgorithmTrain)
        self.assertEqual(test_algorithm_train.ID, 8120)
        self.assertEqual(test_algorithm_train.DebugString, 'CancelTrainToTestMockSession')
        self.assertIsInstance(test_algorithm_train.TrainPathNodes[0], AIDM_classes.TrainPathNode)
        self.assertEqual(test_algorithm_train.TrainPathNodes[0].ID, 8118)

    @mock.patch('requests.Session', side_effect=CancelTrainToTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
