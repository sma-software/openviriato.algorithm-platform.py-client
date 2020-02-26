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
            json_string = ''' {  "ID": 8120,  "TrainPathNodes": [
    {
      "ID": 8118,
      "SectionTrackID": null,
      "NodeID": 15,
      "NodeTrackID": 16,
      "FormationID": 1187,
      "ArrivalTime": "2003-09-01T00:14:00",
      "DepartureTime": "2003-09-01T00:14:00",
      "MinimumRunTime": null,
      "MinimumStopTime": "P0D",
      "StopStatus": "passing",
      "SequenceNumber": 0
    },
    {
      "ID": 8119,
      "SectionTrackID": 1174,
      "NodeID": 10,
      "NodeTrackID": 12,
      "FormationID": null,
      "ArrivalTime": "2003-09-01T00:19:00",
      "DepartureTime": "2003-09-01T00:19:00",
      "MinimumRunTime": "PT5M",
      "MinimumStopTime": "P0D",
      "StopStatus": "commercialStop",
      "SequenceNumber": 1
    }
  ],
  "DebugString": "CancelTrainToTestMockSession"
}'''
            return SessionMockFactory.create_response_mock(json_string, 200)

    interface_to_viriato: AlgorithmPlatformPyClient.AlgorithmicPlatformInterface

    @mock.patch('requests.Session', side_effect=CancelTrainToTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = AlgorithmPlatformPyClient.AlgorithmicPlatformInterface(get_url_str())

    @mock.patch('requests.Session', side_effect=CancelTrainToTestMockSession)
    def test_cancel_train_from_request(self, mocked_get_obj):
        test_dict = dict(trainPathNodeID=8118)
        self.interface_to_viriato.cancel_train_to(test_dict['trainPathNodeID'])
        session_obj = self.interface_to_viriato._AlgorithmicPlatformInterface__communication_layer.currentSession
        self.assertEqual(session_obj._CancelTrainToTestMockSession__last_request,
                         get_url_str() + '/cancel-train-to')
        self.assertEqual(session_obj._CancelTrainToTestMockSession__last_body, test_dict)

    @mock.patch('requests.Session', side_effect=CancelTrainToTestMockSession)
    def test_cancel_train_from_response(self, mocked_get_obj):
        test_algorithm_train = self.interface_to_viriato.cancel_train_from(1)
        self.assertIsInstance(test_algorithm_train, AIDMClasses.AlgorithmTrain)
        self.assertEqual(test_algorithm_train.ID, 8120)
        self.assertEqual(test_algorithm_train.DebugString, 'CancelTrainToTestMockSession')
        self.assertIsInstance(test_algorithm_train.TrainPathNodes[0], AIDMClasses.TrainPathNode)
        self.assertEqual(test_algorithm_train.TrainPathNodes[0].ID, 8118)

    @mock.patch('requests.Session', side_effect=CancelTrainToTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
