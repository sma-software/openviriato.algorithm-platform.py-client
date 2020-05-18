import unittest
from unittest import mock

import AIDMClasses.AIDM_Algorithm_classes
import AlgorithmInterface.AlgorithmInterface
import AlgorithmInterface_test.test_helper.SessionMockFactory as SessionMockFactory
from AlgorithmInterface import AlgorithmInterfaceFactory
from AlgorithmInterface_test.test_helper.SessionMockTestBase import \
    get_api_url, \
    SessionMockTestBase


class TestCancelTrainFrom(unittest.TestCase):
    class CancelTrainFromTestMockSession(SessionMockTestBase):
        # to replace session.get:
        def post(self, request, json):
            self.__last_body = json
            self.__last_request = request
            json_string = (' {"ID": 8116, "TrainPathNodes": [\n'
                           '                        {\n'
                           '                          "ID": 8113,\n'
                           '                          "SectionTrackID": null,\n'
                           '                          "NodeID": 7,\n'
                           '                          "NodeTrackID": 8,\n'
                           '                          "FormationID": 1187,\n'
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
                           '                          "NodeID": 15,\n'
                           '                          "NodeTrackID": 16,\n'
                           '                          "FormationID": null,\n'
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

    interface_to_viriato: AlgorithmInterface.AlgorithmInterface.AlgorithmInterface

    @mock.patch('requests.Session', side_effect=CancelTrainFromTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = AlgorithmInterfaceFactory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=CancelTrainFromTestMockSession)
    def test_cancel_train_from_request(self, mocked_post_obj):
        test_dict = dict(trainPathNodeID=8114)

        self.interface_to_viriato.cancel_train_from(test_dict['trainPathNodeID'])

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._CancelTrainFromTestMockSession__last_request,
                         get_api_url() + '/cancel-train-from')
        self.assertEqual(session_obj._CancelTrainFromTestMockSession__last_body, test_dict)

    @mock.patch('requests.Session', side_effect=CancelTrainFromTestMockSession)
    def test_cancel_train_from_response(self, mocked_post_obj):
        train_path_node_id = 0

        test_algorithm_train = self.interface_to_viriato.cancel_train_from(train_path_node_id)

        self.assertIsInstance(test_algorithm_train, AIDMClasses.AIDM_Algorithm_classes.AlgorithmTrain)
        self.assertEqual(test_algorithm_train.ID, 8116)
        self.assertEqual(test_algorithm_train.DebugString, 'CancelTrainFromTestMockSession')

    @mock.patch('requests.Session', side_effect=CancelTrainFromTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
