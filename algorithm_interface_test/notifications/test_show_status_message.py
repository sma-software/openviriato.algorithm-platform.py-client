import unittest
from unittest import mock

import algorithm_interface_test.test_helper.SessionMockFactory as APISessionMock
from algorithm_interface import algorithm_interface_factory
from algorithm_interface_test.test_helper.SessionMockTestBase import \
    get_api_url, \
    SessionMockTestBase


class TestShowStatusMessage(unittest.TestCase):
    class ShowStatusMessageSessionTestMock(SessionMockTestBase):
        def post(self, request, json):
            self.__last_request = request
            self.__last_body = json
            return APISessionMock.create_response_mock('', 200)

    @mock.patch('requests.Session', side_effect=ShowStatusMessageSessionTestMock)
    def test_show_status_message_one_str(self, mocked_requests_session):
        with algorithm_interface_factory.create(get_api_url()) as interface_to_viriato:
            message_1 = 'Only One Message Sent';

            interface_to_viriato.show_status_message(message_1)

            session_obj = interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
            self.assertEqual(session_obj._ShowStatusMessageSessionTestMock__last_request,
                             get_api_url() + '/status-message')
            self.assertEqual(session_obj._ShowStatusMessageSessionTestMock__last_body,
                             {'shortMessage': 'Only One Message Sent', 'longMessage': None})

    @mock.patch('requests.Session', side_effect=ShowStatusMessageSessionTestMock)
    def test_show_status_message_two_str(self, mocked_requests_session):
        with algorithm_interface_factory.create(get_api_url()) as interface_to_viriato:
            message_1 = 'this is the short one'
            message_2 = 'long one'

            interface_to_viriato.show_status_message(message_1, message_2)

            session_obj = interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
            self.assertEqual(session_obj._ShowStatusMessageSessionTestMock__last_request,
                             get_api_url() + '/status-message')
            self.assertDictEqual(session_obj._ShowStatusMessageSessionTestMock__last_body,
                             {'shortMessage': 'this is the short one', 'longMessage': 'long one'})


if __name__ == '__main__':
    unittest.main()
