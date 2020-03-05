import unittest
from unittest import mock

import AlgorithmInterfaceFactory
import unit_testing_with_mock.SessionMockFactory as SessionMockFactory
import unit_testing_with_mock.unit_testing_helpers
from AIDM_module import AIDM_classes
from unit_testing_with_mock.unit_testing_helpers import get_api_url


class TestCancelTrainFrom(unittest.TestCase):
    class CancelTrainFromTestMockSession(unit_testing_with_mock.unit_testing_helpers.SessionMockTestBase):
        # to replace session.get:
        def post(self, request, json):
            self.__last_body = json
            self.__last_request = request
            json_string = ''' {"ID": 8116, "TrainPathNodes": [
                        {
                          "ID": 8113,
                          "SectionTrackID": null,
                          "NodeID": 7,
                          "NodeTrackID": 8,
                          "FormationID": 1187,
                          "ArrivalTime": "2003-09-01T00:10:00",
                          "DepartureTime": "2003-09-01T00:10:00",
                          "MinimumRunTime": null,
                          "MinimumStopTime": "P0D",
                          "StopStatus": "commercialStop",
                          "SequenceNumber": 0
                        },
                        {
                          "ID": 8114,
                          "SectionTrackID": 1175,
                          "NodeID": 15,
                          "NodeTrackID": 16,
                          "FormationID": null,
                          "ArrivalTime": "2003-09-01T00:14:00",
                          "DepartureTime": "2003-09-01T00:14:00",
                          "MinimumRunTime": "PT4M",
                          "MinimumStopTime": "P0D",
                          "StopStatus": "passing",
                          "SequenceNumber": 1
                        }
                      ],
                      "DebugString": "CancelTrainFromTestMockSession"
                    }'''
            return SessionMockFactory.create_response_mock(json_string, 200)

    interface_to_viriato: AlgorithmInterfaceFactory.AlgorithmicPlatformInterface

    @mock.patch('requests.Session', side_effect=CancelTrainFromTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = AlgorithmInterfaceFactory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=CancelTrainFromTestMockSession)
    def test_cancel_train_from_request(self, mocked_get_obj):
        test_dict = dict(trainPathNodeID=8114)

        self.interface_to_viriato.cancel_train_from(test_dict['trainPathNodeID'])

        session_obj = self.interface_to_viriato._AlgorithmicPlatformInterface__communication_layer.currentSession
        self.assertEqual(session_obj._CancelTrainFromTestMockSession__last_request,
                         get_api_url() + '/cancel-train-from')
        self.assertEqual(session_obj._CancelTrainFromTestMockSession__last_body, test_dict)

    @mock.patch('requests.Session', side_effect=CancelTrainFromTestMockSession)
    def test_cancel_train_from_response(self, mocked_get_obj):
        train_path_node_id = 0

        test_algorithm_train = self.interface_to_viriato.cancel_train_from(train_path_node_id)

        self.assertIsInstance(test_algorithm_train, AIDM_classes.AlgorithmTrain)
        self.assertEqual(test_algorithm_train.ID, 8116)
        self.assertEqual(test_algorithm_train.DebugString, 'CancelTrainFromTestMockSession')

    @mock.patch('requests.Session', side_effect=CancelTrainFromTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
