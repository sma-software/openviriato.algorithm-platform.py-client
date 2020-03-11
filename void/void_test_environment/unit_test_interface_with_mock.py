"""
A test script that requires an REST-API of the VIRIATO-Algorithm Platform
"""

import json
import unittest
from unittest import mock

from AIDMClasses import AIDM_classes
from AlgorithmInterface import AlgorithmInterfaceFactory as interface_module


def get_url_str():
    url_str = 'http://localhost:8080'
    return url_str


# This method will be used by the mock to replace requests.get/post/put
def mocked_requests_response(json_string: str, status_code: int = 200):
    class MockResponse:
        def __init__(self, json_loads_string: str, http_status: int = 200):
            self.json_string = json_loads_string
            self.status_code = http_status

        def raise_for_status(self) -> None:
            if not (self.status_code == 200):
                raise NotImplementedError(self.status_code)

        def json(self) -> dict:
            return json.loads(self.json_string)

    return MockResponse(json_string, status_code)


class MockedRequestsSessionBaseClass:

    def __init__(self):
        print('created a Mocked session')

    def close(self):
        print('closed a Mocked session')


# test which dont need a mock
class TestObjectInitialisation(unittest.TestCase):
    # test for the object creation:
    def test_initialisation_in_with(self):
        with interface_module.AlgorithmicPlatformInterface(get_url_str()) as interface_to_viriato:
            self.assertEqual(interface_to_viriato.base_url, get_url_str())

    # fails on purpose:
    def test_if_initialisation_with_int_fails(self):
        url_nr = 952022
        with self.assertRaises(AssertionError):
            with interface_module.AlgorithmicPlatformInterface(url_nr) as interface_to_viriato:
                var = interface_to_viriato.base_url


class TestUserNotifications(unittest.TestCase):
    class MockedRequestsSessionUserNotification(MockedRequestsSessionBaseClass):
        def post(self, request, json):
            if not (request == (get_url_str() + '/notifications')):
                raise AssertionError('request does not match')
            if not (json == {'messageLevel1': 'hi', 'messageLevel2': 'it works'}):
                raise AssertionError('body does not match')
            return mocked_requests_response(None, 200)

    @mock.patch('requests.Session', side_effect=MockedRequestsSessionUserNotification)
    def test_user_notification_with_str(self, mocked_requests_session):
        interface_to_viriato = interface_module.AlgorithmicPlatformInterface(get_url_str())
        interface_to_viriato.notify_user('hi', 'it works')

    def test_user_notifications_wrong_type(self):
        with self.assertRaises(AssertionError):
            with interface_module.AlgorithmicPlatformInterface(get_url_str()) as interface_to_viriato:
                interface_to_viriato.notify_user(1, 2)


class TestGetDirectedSectionTracks(unittest.TestCase):
    class MockedRequestsGetDirectedSectionTracks(MockedRequestsSessionBaseClass):
        # to replace session.get:
        def get(self, request, params):
            if not (request == (get_url_str() + '/section-tracks-between/20/500')):
                raise AssertionError('request does not match')
            if not (params == {}):
                raise AssertionError('params do not match')

            json_string = ('[\n'
                           '                {\n'
                           '                    "ID": 885,\n'
                           '                    "Code": "838",\n'
                           '                    "SectionCode": "61010",\n'
                           '                    "Weight": 37040,\n'
                           '                    "DebugString": "sectiontrack:s_61010 n_85AR 838"\n'
                           '                },\n'
                           '                {\n'
                           '                    "ID": 886,\n'
                           '                    "Code": "2",\n'
                           '                    "SectionCode": "61010",\n'
                           '                    "Weight": 37040,\n'
                           '                    "DebugString": "sectiontrack:s_61010 n_85AR 2"\n'
                           '                }\n'
                           '            ]')
            return mocked_requests_response(json_string, 200)

    interface_to_viriato: interface_module.AlgorithmicPlatformInterface

    @mock.patch('requests.Session', side_effect=MockedRequestsGetDirectedSectionTracks)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = interface_module.AlgorithmicPlatformInterface(get_url_str())

    @mock.patch('requests.Session', side_effect=MockedRequestsGetDirectedSectionTracks)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)

    @mock.patch('requests.Session', side_effect=MockedRequestsGetDirectedSectionTracks)
    def test_get_directed_section_tracks(self, mocked_get_obj):
        directed_section_tracks = self.interface_to_viriato.get_directed_section_tracks(20, 500)
        self.assertIsInstance(directed_section_tracks[0], AIDM_classes.AlgorithmSectionTrack)

    def test_get_directed_section_tracks_str_parameters(self):
        with self.assertRaises(AssertionError):
            self.interface_to_viriato.get_directed_section_tracks('A', 'b')


if __name__ == '__main__':
    unittest.main()
