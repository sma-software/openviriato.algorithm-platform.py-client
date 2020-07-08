import datetime
import unittest
from unittest import mock

import aidm.aidm_time_window_classes
import aidm.aidm_track_closure_classes
import algorithm_interface.algorithm_interface
import algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from algorithm_interface import algorithm_interface_factory
from algorithm_interface_test.test_helper.SessionMockTestBase import \
    get_api_url, \
    SessionMockTestBase


class TestGetSectionTrackClosures(unittest.TestCase):
    class GetSectionTrackClosuresTestMockSession(SessionMockTestBase):
        def get(self, request, params):
            self.__last_body = params
            self.__last_request = request
            json_string = ("[{\n"
                           "    \"DebugString\": \"sectiontrackclosure:s_70011 1 n_85ZMUS 85ZLSTA\",\n"
                           "    \"SectionTrackID\": 1080,\n"
                           "    \"FromNodeID\": 621,\n"
                           "    \"ToNodeID\": 620,\n"
                           "    \"closure_time_window_from_node\": {\n"
                           "      \"from_time\": \"2003-05-01T08:00:00\",\n"
                           "      \"to_time\": \"2003-05-01T09:00:00\"\n"
                           "    },\n"
                           "    \"ClosureTimeWindowToNode\": {\n"
                           "      \"from_time\": \"2003-05-01T08:30:00\",\n"
                           "      \"to_time\": \"2003-05-01T09:30:00\"\n"
                           "    }\n"
                           "  },\n"
                           "  {\n"
                           "    \"DebugString\": \"sectiontrackclosure:s_70011 0 n_85ZMUS 85ZLST A\",\n"
                           "    \"SectionTrackID\": 1079,\n"
                           "    \"FromNodeID\": 621,\n"
                           "    \"ToNodeID\": 620,\n"
                           "    \"closure_time_window_from_node\": {\n"
                           "      \"from_time\": \"2003-05-01T08:00:00\",\n"
                           "      \"to_time\": \"2003-05-01T09:00:00\"\n"
                           "    },\n"
                           "    \"ClosureTimeWindowToNode\": {\n"
                           "      \"from_time\": \"2003-05-01T08:30:00\",\n"
                           "      \"to_time\": \"2003-05-01T09:30:00\"\n"
                           "    }\n"
                           "  }\n"
                           "]"
                           )

            return SessionMockFactory.create_response_mock(json_string, 200)

    interface_to_viriato: algorithm_interface.algorithm_interface.AlgorithmInterface

    @mock.patch('requests.Session', side_effect=GetSectionTrackClosuresTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetSectionTrackClosuresTestMockSession)
    def test_get_section_track_closures_request(self, mocked_get_obj):
        requested_time_window = aidm.aidm_time_window_classes.TimeWindow(
            from_time=datetime.datetime(2003, 5, 1, 0, 0),
            to_time=datetime.datetime(2003, 5, 12, 0, 0))

        self.interface_to_viriato.get_section_track_closures(time_window=requested_time_window)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetSectionTrackClosuresTestMockSession__last_request,
                         get_api_url() + "/possessions/section-track-closures")
        self.assertDictEqual(session_obj._GetSectionTrackClosuresTestMockSession__last_body,
                             dict(FromTime='2003-05-01T00:00:00', ToTime='2003-05-12T00:00:00'))

    @mock.patch('requests.Session', side_effect=GetSectionTrackClosuresTestMockSession)
    def test_get_section_track_closures_response(self, mocked_get_obj):
        requested_time_window = aidm.aidm_time_window_classes.TimeWindow(
            from_time=datetime.datetime(2003, 5, 1, 0, 0),
            to_time=datetime.datetime(2003, 5, 12, 0, 0))

        list_of_section_track_closure = self.interface_to_viriato.get_section_track_closures(requested_time_window)

        self.assertIsInstance(list_of_section_track_closure, list)
        self.assertIsInstance(
            list_of_section_track_closure[0],
            aidm.aidm_track_closure_classes.AlgorithmSectionTrackClosure)
        self.assertIsInstance(
            list_of_section_track_closure[0].closure_time_window_from_node,
            aidm.aidm_time_window_classes.TimeWindow)
        self.assertEqual(list_of_section_track_closure[0].debug_string, 'sectiontrackclosure:s_70011 1 n_85ZMUS 85ZLSTA')
        self.assertEqual(
            list_of_section_track_closure[0].closure_time_window_from_node.from_time,
            datetime.datetime(2003, 5, 1, 8, 0))

    @mock.patch('requests.Session', side_effect=GetSectionTrackClosuresTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
