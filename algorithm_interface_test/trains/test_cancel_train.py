import unittest
from unittest import mock

import algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client.algorithm_interface import algorithm_interface_factory
from algorithm_interface_test.test_helper.SessionMockTestBase import \
    get_api_url, \
    SessionMockTestBase


class TestGetTrainClassifications(unittest.TestCase):
    class CancelTrainTestMockSession(SessionMockTestBase):
        # to replace session.post:
        def post(self, request, json):
            self.__last_body = json
            self.__last_request = request
            return SessionMockFactory.create_response_mock("8124", 200)

    @mock.patch('requests.Session', side_effect=CancelTrainTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=CancelTrainTestMockSession)
    def test_cancel_train_request(self, mocked_get_obj):
        test_dict = dict(trainID=8124)

        self.interface_to_viriato.cancel_train(test_dict['trainID'])

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
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
