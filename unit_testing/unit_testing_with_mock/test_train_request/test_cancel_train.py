import unittest
from unittest import mock

import unit_testing.unit_testing_with_mock.SessionMockFactory as SessionMockFactory
from AlgorithmInterface import AlgorithmInterfaceFactory
from unit_testing.unit_testing_with_mock.unit_testing_with_mock_helpers import get_api_url, SessionMockTestBase


class TestGetTrainClassifications(unittest.TestCase):
    class CancelTrainTestMockSession(SessionMockTestBase):
        # to replace session.post:
        def post(self, request, json):
            self.__last_body = json
            self.__last_request = request
            return SessionMockFactory.create_response_mock('{ "trainID": 8124 }', 200)

    interface_to_viriato: AlgorithmInterfaceFactory.AlgorithmicPlatformInterface

    @mock.patch('requests.Session', side_effect=CancelTrainTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = AlgorithmInterfaceFactory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=CancelTrainTestMockSession)
    def test_cancel_train_request(self, mocked_get_obj):
        test_dict = dict(trainID=8124)

        self.interface_to_viriato.cancel_train(test_dict['trainID'])

        session_obj = self.interface_to_viriato._AlgorithmicPlatformInterface__communication_layer.currentSession
        self.assertEqual(session_obj._CancelTrainTestMockSession__last_request, get_api_url() + '/cancel-train')
        self.assertDictEqual(session_obj._CancelTrainTestMockSession__last_body, test_dict)

    @mock.patch('requests.Session', side_effect=CancelTrainTestMockSession)
    def test_cancel_train_response(self, mocked_get_obj):
        train_id = 8124

        canceled_train_id = self.interface_to_viriato.cancel_train(train_id)

        self.assertEqual(train_id, canceled_train_id)

    @mock.patch('requests.Session', side_effect=CancelTrainTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
