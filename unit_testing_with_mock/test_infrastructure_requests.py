import AIDMClasses
import unittest
import unit_testing_with_mock.APISessionMock as APISessionMock
import AlgorithmPlatformPyClient as interface_module
from unittest import mock


def get_url_str():
    url_str = 'http://localhost:8080'
    return url_str


class TestGetDirectedSectionTracks(unittest.TestCase):
    class MockedRequestsGetDirectedSectionTracks(APISessionMock.MockedRequestsSessionBaseClass):
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
            return APISessionMock.mocked_requests_response(json_string, 200)

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
        self.assertIsInstance(directed_section_tracks[0], AIDMClasses.AlgorithmSectionTrack)

    def test_get_directed_section_tracks_str_parameters(self):
        with self.assertRaises(AssertionError):
            self.interface_to_viriato.get_directed_section_tracks('A', 'b')


if __name__ == '__main__':
    unittest.main()
