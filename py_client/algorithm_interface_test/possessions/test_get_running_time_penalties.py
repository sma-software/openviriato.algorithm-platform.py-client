from datetime import datetime, timedelta
import unittest
from unittest import mock

from py_client.aidm.aidm_time_window_classes import TimeWindow
from py_client.aidm.aidm_running_time_penalty_classes import AlgorithmSectionRunningTimePenaltyTrack, AlgorithmSectionRunningTimePenalty
import py_client.algorithm_interface.algorithm_interface
import py_client.algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client import algorithm_interface
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import \
    get_api_url, \
    SessionMockTestBase


class TestRunningTimePenalties(unittest.TestCase):
    class GetSectionRunningTimePenaltiesMockSession(SessionMockTestBase):
        def get(self, request, params):
            self.__last_body = params
            self.__last_request = request

            json_string = ("[{\n"
                           "    \"debugString\": \"Name: runtimePenaltyName 05/01/2003 00:00:00 - 05/02/2003 00:00:00\",\n"
                           "    \"id\": 6734,\n"
                           "    \"totalPenalty\": \"PT4M6S\",\n"
                           "    \"affectedSectionTracks\": [ \n"
                           "        {\n"
                           "            \"sectionTrackID\": 791, \n"
                           "            \"fromNodeID\": 69, \n"
                           "            \"fromNodeTimeWindow\": { \n"
                           "                \"fromTime\": \"2003-05-01T00:00:00\", \n"
                           "                \"toTime\": \"2003-05-02T00:00:00\" \n"
                            "           }, \n"
                            "           \"toNodeID\": 83, \n"
                            "           \"toNodeTimeWindow\": { \n"
                            "               \"fromTime\": \"2003-05-01T01:00:00\", \n"
                            "               \"toTime\": \"2003-05-01T22:00:00\" \n"
                            "           } \n"
                            "       }, \n"
                            "       { \n"
                            "           \"sectionTrackID\": 792, \n"
                            "           \"fromNodeID\": 83, \n"
                            "           \"fromNodeTimeWindow\": { \n"
                            "               \"fromTime\": \"2003-05-01T01:00:00\", \n"
                            "               \"toTime\": \"2003-05-01T22:00:00\" \n"
                            "           }, \n"
                            "           \"toNodeID\": 112, \n"
                            "           \"toNodeTimeWindow\": { \n"
                            "               \"fromTime\": \"2003-05-01T02:00:00\", \n"
                            "               \"toTime\": \"2003-05-01T20:00:00\" \n"
                           "            }\n"
                           "        }\n"
                           "    ]\n"
                           "}]"
                           )
            return SessionMockFactory.create_response_mock(json_string, 200)

    interface_to_viriato: py_client.algorithm_interface.algorithm_interface.AlgorithmInterface

    @mock.patch('requests.Session', side_effect=GetSectionRunningTimePenaltiesMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetSectionRunningTimePenaltiesMockSession)
    def test_get_section_running_time_penalties(self, mocked_get_obj):
        requested_time_window = TimeWindow(
            from_time=datetime(2003, 4, 30, 18, 0),
            to_time=datetime(2003, 5, 31, 1, 0))

        self.interface_to_viriato.get_section_running_time_penalties(time_window=requested_time_window)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetSectionRunningTimePenaltiesMockSession__last_request,
                         get_api_url() + "/possessions/section-running-time-penalties")
        self.assertDictEqual(session_obj._GetSectionRunningTimePenaltiesMockSession__last_body,
                             dict(fromTime='2003-04-30T18:00:00', toTime='2003-05-31T01:00:00'))

    @mock.patch('requests.Session', side_effect=GetSectionRunningTimePenaltiesMockSession)
    def test_get_section_running_time_penalties_response(self, mocked_get_obj):
        requested_time_window = TimeWindow(
            from_time=datetime(2003, 4, 30, 18, 0),
            to_time=datetime(2003, 5, 31, 1, 0))

        list_of_running_time_penalties = self.interface_to_viriato.get_section_running_time_penalties(requested_time_window)

        self.assertIsInstance(
            list_of_running_time_penalties,
            list)
        self.assertIsInstance(
            list_of_running_time_penalties[0],
            AlgorithmSectionRunningTimePenalty)
        self.assertEqual(
            list_of_running_time_penalties[0].debug_string,
            'Name: runtimePenaltyName 05/01/2003 00:00:00 - 05/02/2003 00:00:00')
        self.assertEqual(
            list_of_running_time_penalties[0].id,
            6734)
        self.assertIsInstance(
            list_of_running_time_penalties[0].total_penalty,
            timedelta)
        self.assertIsInstance(
            list_of_running_time_penalties[0].affected_section_tracks,
            list)
        self.assertIsInstance(
            list_of_running_time_penalties[0].affected_section_tracks[0],
            AlgorithmSectionRunningTimePenaltyTrack)
        self.assertEqual(
            list_of_running_time_penalties[0].affected_section_tracks[0].section_track_id,
            791)
        self.assertEqual(
            list_of_running_time_penalties[0].affected_section_tracks[0].from_node_id,
            69)
        self.assertIsInstance(
            list_of_running_time_penalties[0].affected_section_tracks[0].from_node_time_window,
            TimeWindow)
        self.assertEqual(
            list_of_running_time_penalties[0].affected_section_tracks[0].to_node_id,
            83)
        self.assertIsInstance(
            list_of_running_time_penalties[0].affected_section_tracks[0].to_node_time_window,
            TimeWindow)
        self.assertEqual(
            list_of_running_time_penalties[0].affected_section_tracks[1].section_track_id,
            792)
        self.assertEqual(
            list_of_running_time_penalties[0].affected_section_tracks[1].from_node_id,
            83)
        self.assertIsInstance(
            list_of_running_time_penalties[0].affected_section_tracks[1].from_node_time_window,
            TimeWindow)
        self.assertEqual(
            list_of_running_time_penalties[0].affected_section_tracks[1].to_node_id,
            112)
        self.assertIsInstance(
            list_of_running_time_penalties[0].affected_section_tracks[1].to_node_time_window,
            TimeWindow)


    @mock.patch('requests.Session', side_effect=GetSectionRunningTimePenaltiesMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)


class TestRunningTimePenaltiesEmpty(unittest.TestCase):
    class GetSectionRunningTimePenaltiesEmptyMockSession(SessionMockTestBase):
        def get(self, request, params):
            self.__last_body = params
            self.__last_request = request

            json_string = "[]"

            return SessionMockFactory.create_response_mock(json_string, 200)

    interface_to_viriato: py_client.algorithm_interface.algorithm_interface.AlgorithmInterface

    @mock.patch('requests.Session', side_effect=GetSectionRunningTimePenaltiesEmptyMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetSectionRunningTimePenaltiesEmptyMockSession)
    def test_get_section_running_time_penalties_response_empty(self, mocked_get_obj):
        requested_time_window = TimeWindow(
            from_time=datetime(2003, 5, 2, 18, 0),
            to_time=datetime(2003, 5, 2, 19, 0))

        list_of_running_time_penalties = self.interface_to_viriato.get_section_running_time_penalties(
            requested_time_window)

        self.assertIsInstance(list_of_running_time_penalties, list)
        self.assertEqual(list_of_running_time_penalties.__len__(), 0)

    @mock.patch('requests.Session', side_effect=GetSectionRunningTimePenaltiesEmptyMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
