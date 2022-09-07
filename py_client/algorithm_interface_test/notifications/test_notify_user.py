import unittest
from unittest import mock

import py_client.algorithm_interface_test.test_helper.SessionMockFactory as APISessionMock
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestUserNotifications(unittest.TestCase):
    class UserNotificationSessionTestMock(SessionMockTestBase):
        def post(self, request, json):
            self.__last_request = request
            self.__last_body = json
            return APISessionMock.create_response_mock("", 200)

    @mock.patch("requests.Session", side_effect=UserNotificationSessionTestMock)
    def test_user_notification_request_formulation(self, mocked_requests_session):
        interface_to_viriato = algorithm_interface_factory.create(get_api_url())
        message_level_1 = "hi"
        message_level_2 = "it works"

        interface_to_viriato.notify_user(message_level_1, message_level_2)

        session_obj = interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._UserNotificationSessionTestMock__last_request, get_api_url() + "/user-outputs/notifications")
        self.assertDictEqual(session_obj._UserNotificationSessionTestMock__last_body, {"title": "hi", "description": "it works"})

    @mock.patch("requests.Session", side_effect=UserNotificationSessionTestMock)
    def test_user_notification_response(self, mocked_requests_session):
        interface_to_viriato = algorithm_interface_factory.create(get_api_url())
        message_level_1 = "hi"
        message_level_2 = "it works"

        response = interface_to_viriato.notify_user(message_level_1, message_level_2)

        self.assertIsNone(response)


if __name__ == "__main__":
    unittest.main()
