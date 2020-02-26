import unittest
from unittest import mock

import AlgorithmPlatformPyClient
import unit_testing_with_mock.SessionMockFactory as APISessionMock
import unit_testing_with_mock.unit_testing_helpers
from unit_testing_with_mock.unit_testing_helpers import get_url_str


class TestUserNotifications(unittest.TestCase):
    class UserNotificationSessionTestMock(unit_testing_with_mock.unit_testing_helpers.SessionMockTestBase):
        def post(self, request, json):
            self.__last_request = request
            self.__last_body = json
            return APISessionMock.create_response_mock('None', 200)

    @mock.patch('requests.Session', side_effect=UserNotificationSessionTestMock)
    def test_user_notification_request_formulation(self, mocked_requests_session):
        interface_to_viriato = AlgorithmPlatformPyClient.AlgorithmicPlatformInterface(get_url_str())
        interface_to_viriato.notify_user('hi', 'it works')
        session_obj = interface_to_viriato._AlgorithmicPlatformInterface__communication_layer.currentSession
        self.assertEqual(session_obj._UserNotificationSessionTestMock__last_request, get_url_str() + '/notifications')
        self.assertEqual(session_obj._UserNotificationSessionTestMock__last_body,
                         {'messageLevel1': 'hi', 'messageLevel2': 'it works'})

    def test_user_notifications_wrong_type(self):
        with self.assertRaises(AssertionError):
            with AlgorithmPlatformPyClient.AlgorithmicPlatformInterface(get_url_str()) as interface_to_viriato:
                interface_to_viriato.notify_user(1, 2)


if __name__ == '__main__':
    unittest.main()
