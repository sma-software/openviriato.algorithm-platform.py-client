from datetime import timedelta
import unittest
from unittest import mock

import py_client.algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client.aidm import CrossingRoutingEdge
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestGetSeparationTimeInJunctionForRoutes(unittest.TestCase):
    class GetSeparationTimeInJunctionForRoutesTestMockSession(SessionMockTestBase):
        def get(self, request, params):
            self.__last_body = params
            self.__last_request = request

            one_day_case_parameters = dict(
                precedingFromSectionTrackId=80, precedingToSectionTrackId=324, succeedingFromSectionTrackId=178, succeedingToSectionTrackId=12740
            )
            null_case_parameters = dict(
                precedingFromSectionTrackId=1, precedingToSectionTrackId=1, succeedingFromSectionTrackId=1, succeedingToSectionTrackId=1
            )

            if self.__last_body == one_day_case_parameters:
                json_string = """{ "separationTime": "P1D"}"""
                return SessionMockFactory.create_response_mock(json_string, 200)
            elif self.__last_body == null_case_parameters:
                json_string = """{ "separationTime": null }"""
                return SessionMockFactory.create_response_mock(json_string, 200)

    @mock.patch("requests.Session", side_effect=GetSeparationTimeInJunctionForRoutesTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch("requests.Session", side_effect=GetSeparationTimeInJunctionForRoutesTestMockSession)
    def test_get_separation_time_in_junction_for_routes_request(self, mocked_get_obj):
        preceding_edge = CrossingRoutingEdge(node_id=123, start_section_track_id=80, end_section_track_id=324)
        succeeding_edge = CrossingRoutingEdge(node_id=123, start_section_track_id=178, end_section_track_id=12740)

        self.interface_to_viriato.get_separation_time_in_junction_for_routes(preceding_edge, succeeding_edge)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetSeparationTimeInJunctionForRoutesTestMockSession__last_request, get_api_url() + "/nodes/123/separation-times")

        expected_query_parameters = dict(
            precedingFromSectionTrackId=80, precedingToSectionTrackId=324, succeedingFromSectionTrackId=178, succeedingToSectionTrackId=12740
        )
        self.assertDictEqual(session_obj._GetSeparationTimeInJunctionForRoutesTestMockSession__last_body, expected_query_parameters)

    @mock.patch("requests.Session", side_effect=GetSeparationTimeInJunctionForRoutesTestMockSession)
    def test_get_separation_time_in_junction_for_routes_response_timedelta(self, mocked_get_obj):
        preceding_edge = CrossingRoutingEdge(node_id=123, start_section_track_id=80, end_section_track_id=324)
        succeeding_edge = CrossingRoutingEdge(node_id=123, start_section_track_id=178, end_section_track_id=12740)

        separation_time = self.interface_to_viriato.get_separation_time_in_junction_for_routes(preceding_edge, succeeding_edge)

        self.assertIsInstance(separation_time, timedelta)
        self.assertEqual(separation_time, timedelta(days=1))

    @mock.patch("requests.Session", side_effect=GetSeparationTimeInJunctionForRoutesTestMockSession)
    def test_get_separation_time_in_junction_for_routes_response_None(self, mocked_get_obj):
        preceding_edge = CrossingRoutingEdge(node_id=123, start_section_track_id=1, end_section_track_id=1)
        succeeding_edge = CrossingRoutingEdge(node_id=123, start_section_track_id=1, end_section_track_id=1)

        separation_time = self.interface_to_viriato.get_separation_time_in_junction_for_routes(preceding_edge, succeeding_edge)

        self.assertIsNone(separation_time)

    @mock.patch("requests.Session", side_effect=GetSeparationTimeInJunctionForRoutesTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
