import unittest
from unittest import mock

import py_client.algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client.aidm import UserOutputSettings
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestGetUserSettings(unittest.TestCase):
    class GetUserSettingsTestMockSession(SessionMockTestBase):
        def get(self, request, params):
            self.__last_body = params
            self.__last_request = request
            json_string = "{ \n" '    "preferredCulture": "en-US" \n' "}"

            return SessionMockFactory.create_response_mock(json_string, 200)

    @mock.patch("requests.Session", side_effect=GetUserSettingsTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch("requests.Session", side_effect=GetUserSettingsTestMockSession)
    def test_get_user_settings_request(self, mocked_get_obj):
        output_settings = self.interface_to_viriato.get_user_output_settings()

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetUserSettingsTestMockSession__last_request, get_api_url() + "/user-outputs/settings")
        self.assertDictEqual(session_obj._GetUserSettingsTestMockSession__last_body, dict())

        self.assertIsInstance(output_settings, UserOutputSettings)
        self.assertIsInstance(output_settings.preferred_culture, str)
        self.assertEqual(output_settings.preferred_culture, "en-US")
