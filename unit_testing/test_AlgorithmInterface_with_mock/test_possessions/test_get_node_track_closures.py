import datetime
import unittest
from unittest import mock

import AIDMClasses.AIDM_classes as AIDM_classes
import AlgorithmInterface.AlgorithmInterface
import unit_testing.test_AlgorithmInterface_with_mock.SessionMockFactory as SessionMockFactory
from AlgorithmInterface import AlgorithmInterfaceFactory
from unit_testing.test_AlgorithmInterface_with_mock.unit_testing_with_mock_helpers import get_api_url, \
    SessionMockTestBase


class TestGetNodeTrackClosures(unittest.TestCase):
    class GetNodeTrackClosuresTestMockSession(SessionMockTestBase):
        def get(self, request, params):
            self.__last_body = params
            self.__last_request = request
            json_string = ("[\n"
                           "  {\n"
                           "    \"DebugString\": \"nodetrackclosure:85ZMUS 24\",\n"
                           "    \"NodeID\": 621,\n"
                           "    \"NodeTrackID\": 622,\n"
                           "    \"ClosureTimeWindow\": {\n"
                           "      \"FromTime\": \"2003-05-01T08:00:00\",\n"
                           "      \"ToTime\": \"2003-05-02T10:00:00\"\n"
                           "    }\n"
                           "  },\n"
                           "  {\n"
                           "    \"DebugString\": \"nodetrackclosure:85ZMUS 23\",\n"
                           "    \"NodeID\": 621,\n"
                           "    \"NodeTrackID\": 623,\n"
                           "    \"ClosureTimeWindow\": {\n"
                           "      \"FromTime\": \"2003-05-01T08:00:00\",\n"
                           "      \"ToTime\": \"2003-05-02T10:00:00\"\n"
                           "    }\n"
                           "  }\n"
                           "]")

            return SessionMockFactory.create_response_mock(json_string, 200)

    interface_to_viriato: AlgorithmInterface.AlgorithmInterface.AlgorithmicPlatformInterface

    @mock.patch('requests.Session', side_effect=GetNodeTrackClosuresTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = AlgorithmInterfaceFactory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetNodeTrackClosuresTestMockSession)
    def test_get_node_track_closures_request(self, mocked_get_obj):
        requested_time_window = AIDM_classes.TimeWindow(FromTime=datetime.datetime(2003, 5, 1, 0, 0),
                                                        ToTime=datetime.datetime(2003, 5, 12, 0, 0))

        self.interface_to_viriato.get_node_track_closures(time_window=requested_time_window)

        session_obj = self.interface_to_viriato._AlgorithmicPlatformInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetNodeTrackClosuresTestMockSession__last_request,
                         get_api_url() + "/possessions/node-track-closures")
        self.assertDictEqual(session_obj._GetNodeTrackClosuresTestMockSession__last_body,
                             dict(FromTime='2003-05-01T00:00:00', ToTime='2003-05-12T00:00:00'))

    @mock.patch('requests.Session', side_effect=GetNodeTrackClosuresTestMockSession)
    def test_get_node_track_closures_response(self, mocked_get_obj):
        requested_time_window = AIDM_classes.TimeWindow

        list_of_section_track_closure = self.interface_to_viriato.get_node_track_closures(requested_time_window)

        self.assertIsInstance(list_of_section_track_closure, list)
        self.assertIsInstance(list_of_section_track_closure[0], AIDM_classes.AlgorithmNodeTrackClosure)
        self.assertIsInstance(list_of_section_track_closure[0].ClosureTimeWindow, AIDM_classes.TimeWindow)
        self.assertEqual(list_of_section_track_closure[0].DebugString, "nodetrackclosure:85ZMUS 24")
        self.assertEqual(list_of_section_track_closure[0].ClosureTimeWindow.FromTime,
                         datetime.datetime(2003, 5, 1, 8, 0))

    @mock.patch('requests.Session', side_effect=GetNodeTrackClosuresTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
