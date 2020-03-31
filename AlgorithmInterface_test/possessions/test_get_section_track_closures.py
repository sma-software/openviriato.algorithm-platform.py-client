import datetime
import unittest
from unittest import mock

import AIDMClasses.AIDM_classes as AIDM_classes
import AlgorithmInterface.AlgorithmInterface
import AlgorithmInterface_test.test_helper.SessionMockFactory as SessionMockFactory
from AlgorithmInterface import AlgorithmInterfaceFactory
from AlgorithmInterface_test.test_helper.SessionMockTestBase import \
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
                           "    \"ClosureTimeWindowFromNode\": {\n"
                           "      \"FromTime\": \"2003-05-01T08:00:00\",\n"
                           "      \"ToTime\": \"2003-05-01T09:00:00\"\n"
                           "    },\n"
                           "    \"ClosureTimeWindowToNode\": {\n"
                           "      \"FromTime\": \"2003-05-01T08:30:00\",\n"
                           "      \"ToTime\": \"2003-05-01T09:30:00\"\n"
                           "    }\n"
                           "  },\n"
                           "  {\n"
                           "    \"DebugString\": \"sectiontrackclosure:s_70011 0 n_85ZMUS 85ZLST A\",\n"
                           "    \"SectionTrackID\": 1079,\n"
                           "    \"FromNodeID\": 621,\n"
                           "    \"ToNodeID\": 620,\n"
                           "    \"ClosureTimeWindowFromNode\": {\n"
                           "      \"FromTime\": \"2003-05-01T08:00:00\",\n"
                           "      \"ToTime\": \"2003-05-01T09:00:00\"\n"
                           "    },\n"
                           "    \"ClosureTimeWindowToNode\": {\n"
                           "      \"FromTime\": \"2003-05-01T08:30:00\",\n"
                           "      \"ToTime\": \"2003-05-01T09:30:00\"\n"
                           "    }\n"
                           "  }\n"
                           "]"
                           )

            return SessionMockFactory.create_response_mock(json_string, 200)

    interface_to_viriato: AlgorithmInterface.AlgorithmInterface.AlgorithmicPlatformInterface

    @mock.patch('requests.Session', side_effect=GetSectionTrackClosuresTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = AlgorithmInterfaceFactory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetSectionTrackClosuresTestMockSession)
    def test_get_section_track_closures_request(self, mocked_get_obj):
        requested_time_window = AIDM_classes.TimeWindow(FromTime=datetime.datetime(2003, 5, 1, 0, 0),
                                                        ToTime=datetime.datetime(2003, 5, 12, 0, 0))

        self.interface_to_viriato.get_section_track_closures(time_window=requested_time_window)

        session_obj = self.interface_to_viriato._AlgorithmicPlatformInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetSectionTrackClosuresTestMockSession__last_request,
                         get_api_url() + "/possessions/section-track-closures")
        self.assertDictEqual(session_obj._GetSectionTrackClosuresTestMockSession__last_body,
                             dict(FromTime='2003-05-01T00:00:00', ToTime='2003-05-12T00:00:00'))

    @mock.patch('requests.Session', side_effect=GetSectionTrackClosuresTestMockSession)
    def test_get_section_track_closures_response(self, mocked_get_obj):
        requested_time_window = AIDM_classes.TimeWindow

        list_of_section_track_closure = self.interface_to_viriato.get_section_track_closures(requested_time_window)

        self.assertIsInstance(list_of_section_track_closure, list)
        self.assertIsInstance(list_of_section_track_closure[0], AIDM_classes.AlgorithmSectionTrackClosure)
        self.assertIsInstance(list_of_section_track_closure[0].ClosureTimeWindowFromNode, AIDM_classes.TimeWindow)
        self.assertEqual(list_of_section_track_closure[0].DebugString, 'sectiontrackclosure:s_70011 1 n_85ZMUS 85ZLSTA')
        self.assertEqual(list_of_section_track_closure[0].ClosureTimeWindowFromNode.FromTime,
                         datetime.datetime(2003, 5, 1, 8, 0))

    @mock.patch('requests.Session', side_effect=GetSectionTrackClosuresTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
