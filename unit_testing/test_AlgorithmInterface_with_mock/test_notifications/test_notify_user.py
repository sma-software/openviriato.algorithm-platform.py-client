import unittest
from unittest import mock

import unit_testing.test_AlgorithmInterface_with_mock.SessionMockFactory as APISessionMock
from AlgorithmInterface import AlgorithmInterfaceFactory
from unit_testing.test_AlgorithmInterface_with_mock.unit_testing_with_mock_helpers import get_api_url, \
    SessionMockTestBase


class TestUserNotifications(unittest.TestCase):
    class UserNotificationSessionTestMock(SessionMockTestBase):
        def post(self, request, json):
            self.__last_request = request
            self.__last_body = json
            return APISessionMock.create_response_mock('', 200)

    @mock.patch('requests.Session', side_effect=UserNotificationSessionTestMock)
    def test_user_notification_request_formulation(self, mocked_requests_session):
        interface_to_viriato = AlgorithmInterfaceFactory.create(get_api_url())
        message_level_1 = "hi"
        message_level_2 = "it works"

        interface_to_viriato.notify_user(message_level_1, message_level_2)

        session_obj = interface_to_viriato._AlgorithmicPlatformInterface__communication_layer.currentSession
        self.assertEqual(session_obj._UserNotificationSessionTestMock__last_request, get_api_url() + '/notifications')
        self.assertDictEqual(session_obj._UserNotificationSessionTestMock__last_body,
                         {'messageLevel1': 'hi', 'messageLevel2': 'it works'})


if __name__ == '__main__':
    unittest.main()
