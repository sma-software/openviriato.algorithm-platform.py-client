import unittest
from unittest import mock

import py_client.algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestDeleteTrain(unittest.TestCase):
    class DeleteTrainTestMockSession(SessionMockTestBase):
        def delete(self, request, json):
            self._last_body = json
            self._last_request = request
            return SessionMockFactory.create_response_mock("8124", 200)

    @mock.patch("requests.Session", side_effect=DeleteTrainTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch("requests.Session", side_effect=DeleteTrainTestMockSession)
    def test_delete_train_request(self, mocked_get_obj):
        train_id = 8124
        self.interface_to_viriato.delete_train(train_id)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj.last_request, get_api_url() + "/trains/" + str(train_id) + ":delete")
        self.assertDictEqual(session_obj.last_body, {})

    @mock.patch("requests.Session", side_effect=DeleteTrainTestMockSession)
    def test_cancel_train_response(self, mocked_get_obj):
        train_id = 8124

        # test and validate
        self.assertIsNone(self.interface_to_viriato.delete_train(train_id))

    @mock.patch("requests.Session", side_effect=DeleteTrainTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
