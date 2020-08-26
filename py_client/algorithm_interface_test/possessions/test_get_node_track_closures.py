import datetime
import unittest
from unittest import mock

import py_client.aidm.aidm_time_window_classes
import py_client.aidm.aidm_track_closure_classes
import py_client.algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client import algorithm_interface
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import \
    get_api_url, \
    SessionMockTestBase


class TestGetNodeTrackClosures(unittest.TestCase):
    class GetNodeTrackClosuresTestMockSession(SessionMockTestBase):
        def get(self, request, params):
            self.__last_body = params
            self.__last_request = request
            json_string = ("[\n"
                           "  {\n"
                           "    \"debugString\": \"nodetrackclosure:85ZMUS 24\",\n"
                           "    \"nodeId\": 621,\n"
                           "    \"nodeTrackId\": 622,\n"
                           "    \"closureTimeWindow\": {\n"
                           "      \"fromTime\": \"2003-05-01T08:00:00\",\n"
                           "      \"toTime\": \"2003-05-02T10:00:00\"\n"
                           "    }\n"
                           "  },\n"
                           "  {\n"
                           "    \"debugString\": \"nodetrackclosure:85ZMUS 23\",\n"
                           "    \"nodeId\": 621,\n"
                           "    \"nodeTrackId\": 623,\n"
                           "    \"closureTimeWindow\": {\n"
                           "      \"fromTime\": \"2003-05-01T08:00:00\",\n"
                           "      \"toTime\": \"2003-05-02T10:00:00\"\n"
                           "    }\n"
                           "  }\n"
                           "]")

            return SessionMockFactory.create_response_mock(json_string, 200)

    interface_to_viriato: py_client.algorithm_interface.algorithm_interface.AlgorithmInterface

    @mock.patch('requests.Session', side_effect=GetNodeTrackClosuresTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetNodeTrackClosuresTestMockSession)
    def test_get_node_track_closures_request(self, mocked_get_obj):
        requested_time_window = py_client.aidm.aidm_time_window_classes.TimeWindow(
            from_time=datetime.datetime(2003, 5, 1, 0, 0),
            to_time=datetime.datetime(2003, 5, 12, 0, 0))

        self.interface_to_viriato.get_node_track_closures(time_window=requested_time_window)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetNodeTrackClosuresTestMockSession__last_request,
                         get_api_url() + "/possessions/node-track-closures")
        self.assertDictEqual(session_obj._GetNodeTrackClosuresTestMockSession__last_body,
                             dict(fromTime='2003-05-01T00:00:00', toTime='2003-05-12T00:00:00'))

    @mock.patch('requests.Session', side_effect=GetNodeTrackClosuresTestMockSession)
    def test_get_node_track_closures_response(self, mocked_get_obj):
        requested_time_window = py_client.aidm.aidm_time_window_classes.TimeWindow(
            from_time=datetime.datetime(2003, 5, 1, 0, 0),
            to_time=datetime.datetime(2003, 5, 12, 0, 0))

        list_of_section_track_closure = self.interface_to_viriato.get_node_track_closures(requested_time_window)

        self.assertIsInstance(list_of_section_track_closure, list)
        self.assertIsInstance(list_of_section_track_closure[0],
                              py_client.aidm.aidm_track_closure_classes.AlgorithmNodeTrackClosure)
        self.assertIsInstance(list_of_section_track_closure[0].closure_time_window,
                              py_client.aidm.aidm_time_window_classes.TimeWindow)
        self.assertEqual(list_of_section_track_closure[0].debug_string, "nodetrackclosure:85ZMUS 24")
        self.assertEqual(list_of_section_track_closure[0].closure_time_window.from_time,
                         datetime.datetime(2003, 5, 1, 8, 0))

    @mock.patch('requests.Session', side_effect=GetNodeTrackClosuresTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
