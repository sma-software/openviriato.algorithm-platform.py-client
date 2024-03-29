from datetime import datetime
import unittest
from unittest import mock

import py_client.aidm.aidm_time_window_classes
import py_client.aidm.aidm_track_closure_classes
import py_client.algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client import algorithm_interface
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestGetSectionTrackClosures(unittest.TestCase):
    class GetSectionTrackClosuresTestMockSession(SessionMockTestBase):
        def get(self, request, params):
            self.__last_body = params
            self.__last_request = request
            json_string = (
                "[{\n"
                '    "debugString": "sectiontrackclosure:s_70011 1 n_85ZMUS 85ZLSTA",\n'
                '    "sectionTrackId": 1080,\n'
                '    "FromNodeId": 621,\n'
                '    "toNodeId": 620,\n'
                '    "closureTimeWindowFromNode": {\n'
                '      "fromTime": "2003-05-01T08:00:00",\n'
                '      "toTime": "2003-05-01T09:00:00"\n'
                "    },\n"
                '    "closureTimeWindowToNode": {\n'
                '      "fromTime": "2003-05-01T08:30:00",\n'
                '      "toTime": "2003-05-01T09:30:00"\n'
                "    }\n"
                "  },\n"
                "  {\n"
                '    "debugString": "sectiontrackclosure:s_70011 0 n_85ZMUS 85ZLST A",\n'
                '    "sectionTrackId": 1079,\n'
                '    "FromNodeId": 621,\n'
                '    "toNodeId": 620,\n'
                '    "closureTimeWindowFromNode": {\n'
                '      "fromTime": "2003-05-01T08:00:00",\n'
                '      "toTime": "2003-05-01T09:00:00"\n'
                "    },\n"
                '    "closureTimeWindowToNode": {\n'
                '      "fromTime": "2003-05-01T08:30:00",\n'
                '      "toTime": "2003-05-01T09:30:00"\n'
                "    }\n"
                "  }\n"
                "]"
            )

            return SessionMockFactory.create_response_mock(json_string, 200)

    interface_to_viriato: py_client.algorithm_interface.algorithm_interface.AlgorithmInterface

    @mock.patch("requests.Session", side_effect=GetSectionTrackClosuresTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch("requests.Session", side_effect=GetSectionTrackClosuresTestMockSession)
    def test_get_section_track_closures_request(self, mocked_get_obj):
        requested_time_window = py_client.aidm.aidm_time_window_classes.TimeWindow(from_time=datetime(2003, 5, 1, 0, 0), to_time=datetime(2003, 5, 12, 0, 0))

        self.interface_to_viriato.get_section_track_closures(time_window=requested_time_window)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetSectionTrackClosuresTestMockSession__last_request, get_api_url() + "/possessions/section-track-closures")
        self.assertDictEqual(session_obj._GetSectionTrackClosuresTestMockSession__last_body, dict(fromTime="2003-05-01T00:00:00", toTime="2003-05-12T00:00:00"))

    @mock.patch("requests.Session", side_effect=GetSectionTrackClosuresTestMockSession)
    def test_get_section_track_closures_response(self, mocked_get_obj):
        requested_time_window = py_client.aidm.aidm_time_window_classes.TimeWindow(from_time=datetime(2003, 5, 1, 0, 0), to_time=datetime(2003, 5, 12, 0, 0))

        list_of_section_track_closure = self.interface_to_viriato.get_section_track_closures(requested_time_window)

        self.assertIsInstance(list_of_section_track_closure, list)
        self.assertIsInstance(list_of_section_track_closure[0], py_client.aidm.aidm_track_closure_classes.AlgorithmSectionTrackClosure)
        self.assertIsInstance(list_of_section_track_closure[0].closure_time_window_from_node, py_client.aidm.aidm_time_window_classes.TimeWindow)
        self.assertEqual(list_of_section_track_closure[0].debug_string, "sectiontrackclosure:s_70011 1 n_85ZMUS 85ZLSTA")
        self.assertEqual(list_of_section_track_closure[0].closure_time_window_from_node.from_time, datetime(2003, 5, 1, 8, 0))

    @mock.patch("requests.Session", side_effect=GetSectionTrackClosuresTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
