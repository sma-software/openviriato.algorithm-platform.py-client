import unittest
from unittest import mock

from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper import SessionMockFactory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import SessionMockTestBase, get_api_url


class TestHasChangedTrains(unittest.TestCase):
    class HasChangedTrainsMockSession(SessionMockTestBase):
        def get(self, request, params):
            self._last_body = params
            self._last_request = request

            json_string = "{\"hasChanged\": false}"

            return SessionMockFactory.create_response_mock(json_string, 200)

    @mock.patch('requests.Session', side_effect=HasChangedTrainsMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=HasChangedTrainsMockSession)
    def test_has_changed_trains_request(self, mocked_get_obj):
        self.interface_to_viriato.has_changed_trains()

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj.last_request, get_api_url() + '/trains:has-changed')
        self.assertDictEqual(session_obj.last_body, dict())

    @mock.patch('requests.Session', side_effect=HasChangedTrainsMockSession)
    def test_has_changed_trains_response(self, mocked_get_obj):
        has_changed_trains = self.interface_to_viriato.has_changed_trains()

        self.assertFalse(has_changed_trains)

    @mock.patch('requests.Session', side_effect=HasChangedTrainsMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
