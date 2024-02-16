import unittest
from unittest import mock

import py_client.algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client.aidm.aidm_reset_train_classes import ResetSummary
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestResetTrain(unittest.TestCase):
    class TrainResetTestMockSession(SessionMockTestBase):
        def delete(self, request, json):
            self._last_body = json
            self._last_request = request
            response_mock = '{"number_of_deleted_links": 99, "number_of_reset_trains": 299}'
            return SessionMockFactory.create_response_mock(response_mock, 200)

    @mock.patch("requests.Session", side_effect=TrainResetTestMockSession)
    def setUp(self, mocked_delete_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch("requests.Session", side_effect=TrainResetTestMockSession)
    def test_reset_trains_request(self, mocked_delete_obj):
        self.interface_to_viriato.reset_trains()

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj.last_request, get_api_url() + "/services/trains:reset")
        self.assertDictEqual(session_obj.last_body, {})

    @mock.patch("requests.Session", side_effect=TrainResetTestMockSession)
    def test_reset_trains_response(self, mocked_delete_obj):
        response = self.interface_to_viriato.reset_trains()

        # test and validate
        self.assertIsInstance(response, ResetSummary)
        self.assertEqual(response.number_of_deleted_links, 99)
        self.assertEqual(response.number_of_reset_trains, 299)

    @mock.patch("requests.Session", side_effect=TrainResetTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
