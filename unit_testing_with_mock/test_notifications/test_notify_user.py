import unittest
from unittest import mock

import AlgorithmInterfaceFactory
import unit_testing_with_mock.SessionMockFactory as APISessionMock
import unit_testing_with_mock.unit_testing_helpers
from unit_testing_with_mock.unit_testing_helpers import get_api_url


class TestUserNotifications(unittest.TestCase):
    class UserNotificationSessionTestMock(unit_testing_with_mock.unit_testing_helpers.SessionMockTestBase):
        def post(self, request, json):
            self.__last_request = request
            self.__last_body = json
            return APISessionMock.create_response_mock('', 200)

    @mock.patch('requests.Session', side_effect=UserNotificationSessionTestMock)
    def test_user_notification_request_formulation(self, mocked_requests_session):
        interface_to_viriato = AlgorithmInterfaceFactory.AlgorithmicPlatformInterface(get_api_url())
        interface_to_viriato.notify_user('hi', 'it works')
        session_obj = interface_to_viriato._AlgorithmicPlatformInterface__communication_layer.currentSession
        self.assertEqual(session_obj._UserNotificationSessionTestMock__last_request, get_api_url() + '/notifications')
        self.assertEqual(session_obj._UserNotificationSessionTestMock__last_body,
                         {'messageLevel1': 'hi', 'messageLevel2': 'it works'})

    #def test_user_notifications_wrong_type(self):
        # with self.assertRaises(AssertionError):
            #with AlgorithmInterfaceFactory.AlgorithmicPlatformInterface(get_api_url()) as interface_to_viriato:
                # interface_to_viriato.notify_user(1, 2)


if __name__ == '__main__':
    unittest.main()
