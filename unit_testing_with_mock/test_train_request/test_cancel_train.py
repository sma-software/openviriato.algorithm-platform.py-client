import unittest
from unittest import mock

import AIDMClasses
import AlgorithmPlatformPyClient
import unit_testing_with_mock.SessionMockFactory as SessionMockFactory
import unit_testing_with_mock.unit_testing_helpers
from unit_testing_with_mock.unit_testing_helpers import get_url_str


class TestGetTrainClassifications(unittest.TestCase):
    class CancelTrainTestMockSession(unit_testing_with_mock.unit_testing_helpers.SessionMockTestBase):
        # to replace session.get:
        def post(self, request, json):
            self.__last_body = json
            self.__last_request = request
            return SessionMockFactory.create_response_mock('{ "trainID": 8124 }', 200)

    interface_to_viriato: AlgorithmPlatformPyClient.AlgorithmicPlatformInterface

    @mock.patch('requests.Session', side_effect=CancelTrainTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = AlgorithmPlatformPyClient.AlgorithmicPlatformInterface(get_url_str())

    @mock.patch('requests.Session', side_effect=CancelTrainTestMockSession)
    def test_cancel_train_to_request(self, mocked_get_obj):
        test_dict = dict(trainID=8124)
        self.interface_to_viriato.cancel_train(test_dict['trainID'])
        session_obj = self.interface_to_viriato._AlgorithmicPlatformInterface__communication_layer.currentSession
        self.assertEqual(session_obj._CancelTrainTestMockSession__last_request, get_url_str() + '/cancel-train')
        self.assertDictEqual(session_obj._CancelTrainTestMockSession__last_body, test_dict)

    @mock.patch('requests.Session', side_effect=CancelTrainTestMockSession)
    def test_cancel_train_from_response(self, mocked_get_obj):
        test_algorithm_train = self.interface_to_viriato.cancel_train_to(1)
        self.assertIsInstance(test_algorithm_train, AIDMClasses.AlgorithmTrain)
        self.assertEqual(test_algorithm_train.ID, 8120)
        self.assertEqual(test_algorithm_train.DebugString, 'CancelTrainToTestMockSession')
        self.assertIsInstance(test_algorithm_train.TrainPathNodes[0], AIDMClasses.TrainPathNode)
        self.assertEqual(test_algorithm_train.TrainPathNodes[0].ID, 8118)

    @mock.patch('requests.Session', side_effect=CancelTrainTestMockSession)
    def test_cancel_train_from_response_when_broken(self, mocked_get_obj):
        test_algorithm_train = self.interface_to_viriato.cancel_train_to(1)

    @mock.patch('requests.Session', side_effect=CancelTrainTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
