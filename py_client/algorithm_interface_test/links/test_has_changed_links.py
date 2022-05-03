import unittest
from unittest import mock

from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper import SessionMockFactory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import SessionMockTestBase, get_api_url


class TestHasChangedLinks(unittest.TestCase):
    class HasChangedLinksMockSession(SessionMockTestBase):
        def get(self, request, params):
            self._last_body = params
            self._last_request = request

            json_string = "{\"hasChanged\": true}"

            return SessionMockFactory.create_response_mock(json_string, 200)

    @mock.patch('requests.Session', side_effect=HasChangedLinksMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=HasChangedLinksMockSession)
    def test_has_changed_links_request(self, mocked_get_obj):
        self.interface_to_viriato.has_changed_links()

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj.last_request, get_api_url() + '/links:has-changed')
        self.assertDictEqual(session_obj.last_body, dict())

    @mock.patch('requests.Session', side_effect=HasChangedLinksMockSession)
    def test_has_changed_links_response(self, mocked_get_obj):
        has_changed_links = self.interface_to_viriato.has_changed_links()

        self.assertTrue(has_changed_links)

    @mock.patch('requests.Session', side_effect=HasChangedLinksMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
