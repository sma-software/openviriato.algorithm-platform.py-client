import unittest
import AlgorithmPlatformPyClient
import unit_testing_with_mock.APISessionMock as APISessionMock
from unittest import mock


def get_url_str():
    url_str = 'http://localhost:8080'
    return url_str


class TestUserNotifications(unittest.TestCase):
    class MockedRequestsSessionUserNotification(APISessionMock.MockedRequestsSessionBaseClass):
        def post(self, request, json):
            if not (request == (get_url_str() + '/notifications')):
                raise AssertionError('request does not match')
            if not (json == {'messageLevel1': 'hi', 'messageLevel2': 'it works'}):
                raise AssertionError('body does not match')
            return APISessionMock.mocked_requests_response(None, 200)

    @mock.patch('requests.Session', side_effect=MockedRequestsSessionUserNotification)
    def test_user_notification_with_str(self, mocked_requests_session):
        interface_to_viriato = AlgorithmPlatformPyClient.AlgorithmicPlatformInterface(get_url_str())
        interface_to_viriato.notify_user('hi', 'it works')

    def test_user_notifications_wrong_type(self):
        with self.assertRaises(AssertionError):
            with AlgorithmPlatformPyClient.AlgorithmicPlatformInterface(get_url_str()) as interface_to_viriato:
                interface_to_viriato.notify_user(1, 2)


class TestShowStatusMessage(unittest.TestCase):
    class MockedRequestsSessionShowStatusMessage(APISessionMock.MockedRequestsSessionBaseClass):
        def post(self, request, json):
            if not (request == (get_url_str() + '/status-message')):
                raise AssertionError('request does not match')
            if not (json == {'shortMessage': 'Only One Message Sent', 'longMessage': None}):
                if not (json == {'shortMessage': 'this is the short one', 'longMessage': 'long one'}):
                    raise AssertionError('body does not match')
            return APISessionMock.mocked_requests_response('null', 200)

    @mock.patch('requests.Session', side_effect=MockedRequestsSessionShowStatusMessage)
    def test_show_status_message_one_str(self, mocked_requests_session):
        with AlgorithmPlatformPyClient.AlgorithmicPlatformInterface(get_url_str()) as interface_to_viriato:
            interface_to_viriato.show_status_message('Only One Message Sent')

    @mock.patch('requests.Session', side_effect=MockedRequestsSessionShowStatusMessage)
    def test_show_status_message_two_str(self, mocked_requests_session):
        with AlgorithmPlatformPyClient.AlgorithmicPlatformInterface(get_url_str()) as interface_to_viriato:
            interface_to_viriato.show_status_message('this is the short one', 'long one')

    def test_user_notifications_wrong_type_one_param(self):
        with self.assertRaises(AssertionError):
            with AlgorithmPlatformPyClient.AlgorithmicPlatformInterface(get_url_str()) as interface_to_viriato:
                interface_to_viriato.show_status_message(1)

    def test_user_notifications_wrong_type_two_param(self):
        with self.assertRaises(AssertionError):
            with AlgorithmPlatformPyClient.AlgorithmicPlatformInterface(get_url_str()) as interface_to_viriato:
                interface_to_viriato.show_status_message('one', 1)


if __name__ == '__main__':
    unittest.main()
