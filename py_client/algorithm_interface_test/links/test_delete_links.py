import unittest
from unittest import mock

import py_client.algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import \
    get_api_url, \
    SessionMockTestBase


class TestDeleteLinks(unittest.TestCase):
    class DeleteLinksMockSession(SessionMockTestBase):
        def delete(self, request, json):
            self._last_body = json
            self._last_request = request

            return SessionMockFactory.create_response_mock('', 200)

    @mock.patch('requests.Session', side_effect=DeleteLinksMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=DeleteLinksMockSession)
    def test_delete_links_request(self, mocked_get_obj):
        link_ids = [6748, 6749]

        self.interface_to_viriato.delete_links(link_ids)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj.last_request, get_api_url() + "/links")
        self.assertDictEqual(session_obj.last_body, dict(linkIDs=link_ids))

    @mock.patch('requests.Session', side_effect=DeleteLinksMockSession)
    def test_delete_links_response(self, mocked_get_obj):
        link_ids = [6748, 6749]

        # test and validate
        self.assertIsNone(self.interface_to_viriato.delete_links(link_ids))

    @mock.patch('requests.Session', side_effect=DeleteLinksMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
