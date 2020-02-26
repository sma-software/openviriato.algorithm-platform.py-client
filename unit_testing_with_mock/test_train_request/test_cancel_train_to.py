import unittest
from unittest import mock

import AIDMClasses
import AlgorithmPlatformPyClient
import unit_testing_with_mock.SessionMockFactory as SessionMockFactory
import unit_testing_with_mock.unit_testing_helpers
from unit_testing_with_mock.unit_testing_helpers import get_url_str


class TestGetTrainClassifications(unittest.TestCase):
    class CancelTrainToTestMockSession(unit_testing_with_mock.unit_testing_helpers.SessionMockTestBase):
        # to replace session.get:
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

    interface_to_viriato: AlgorithmPlatformPyClient.AlgorithmicPlatformInterface

    @mock.patch('requests.Session', side_effect=CancelTrainToTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = AlgorithmPlatformPyClient.AlgorithmicPlatformInterface(get_url_str())

    @mock.patch('requests.Session', side_effect=CancelTrainToTestMockSession)
    def test_cancel_train_to_request(self, mocked_get_obj):
        test_dict = dict(trainPathNodeID=8118)
        self.interface_to_viriato.cancel_train_to(test_dict['trainPathNodeID'])
        session_obj = self.interface_to_viriato._AlgorithmicPlatformInterface__communication_layer.currentSession
        self.assertEqual(session_obj._CancelTrainToTestMockSession__last_request, get_url_str() + '/cancel-train-to')
        self.assertEqual(session_obj._CancelTrainToTestMockSession__last_body, test_dict)

    @mock.patch('requests.Session', side_effect=CancelTrainToTestMockSession)
    def test_cancel_train_from_response(self, mocked_get_obj):
        test_algorithm_train = self.interface_to_viriato.cancel_train_to(1)
        self.assertIsInstance(test_algorithm_train, AIDMClasses.AlgorithmTrain)
        self.assertEqual(test_algorithm_train.ID, 8120)
        self.assertEqual(test_algorithm_train.DebugString, 'CancelTrainToTestMockSession')
        self.assertIsInstance(test_algorithm_train.TrainPathNodes[0], AIDMClasses.TrainPathNode)
        self.assertEqual(test_algorithm_train.TrainPathNodes[0].ID, 8118)

    @mock.patch('requests.Session', side_effect=CancelTrainToTestMockSession)
    def test_cancel_train_from_response_when_broken(self, mocked_get_obj):
        test_algorithm_train = self.interface_to_viriato.cancel_train_to(1)
        self.assertIsInstance(test_algorithm_train, AIDMClasses.AlgorithmTrain)
        self.assertEqual(test_algorithm_train.ID, 8120)
        self.assertEqual(test_algorithm_train.DebugString, 'CancelTrainToTestMockSession')
        self.assertIsInstance(test_algorithm_train.TrainPathNodes[0], AIDMClasses.TrainPathNode)
        self.assertEqual(test_algorithm_train.TrainPathNodes[0].ID, 8118)

    @mock.patch('requests.Session', side_effect=CancelTrainToTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)