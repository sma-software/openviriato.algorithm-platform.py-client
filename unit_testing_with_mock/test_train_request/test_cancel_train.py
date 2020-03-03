import unittest
from unittest import mock

import AlgorithmInterfaceFactory
import unit_testing_with_mock.SessionMockFactory as SessionMockFactory
import unit_testing_with_mock.unit_testing_helpers
from unit_testing_with_mock.unit_testing_helpers import get_api_url


class TestGetTrainClassifications(unittest.TestCase):
    class CancelTrainTestMockSession(unit_testing_with_mock.unit_testing_helpers.SessionMockTestBase):
        # to replace session.post:
        def post(self, request, json):
            self.__last_body = json
            self.__last_request = request
            return SessionMockFactory.create_response_mock('{ "trainID": 8124 }', 200)

    interface_to_viriato: AlgorithmInterfaceFactory.AlgorithmicPlatformInterface

    @mock.patch('requests.Session', side_effect=CancelTrainTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = AlgorithmInterfaceFactory.AlgorithmicPlatformInterface(get_api_url())

    @mock.patch('requests.Session', side_effect=CancelTrainTestMockSession)
    def test_cancel_train_request(self, mocked_get_obj):
        test_dict = dict(trainID=8124)
        self.interface_to_viriato.cancel_train(test_dict['trainID'])
        session_obj = self.interface_to_viriato._AlgorithmicPlatformInterface__communication_layer.currentSession
        self.assertEqual(session_obj._CancelTrainTestMockSession__last_request, get_api_url() + '/cancel-train')
        self.assertDictEqual(session_obj._CancelTrainTestMockSession__last_body, test_dict)

    @mock.patch('requests.Session', side_effect=CancelTrainTestMockSession)
    def test_cancel_train_response(self, mocked_get_obj):
        canceled_train_id = self.interface_to_viriato.cancel_train(8124)
        self.assertEqual(8124, canceled_train_id)

    def test_test_cancel_train_wrong_type(self):
        with self.assertRaises(AssertionError):
            with AlgorithmInterfaceFactory.AlgorithmicPlatformInterface(get_api_url()) as interface_to_viriato:
                interface_to_viriato.cancel_train('wrong type')

    @mock.patch('requests.Session', side_effect=CancelTrainTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
