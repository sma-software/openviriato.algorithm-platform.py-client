import datetime
import unittest
from unittest import mock

import py_client.algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestGetDefaultHeadwayTime(unittest.TestCase):
    class GetDefaultHeadwayTimeTestMockSession(SessionMockTestBase):
        def get(self, request, params):
            self.__last_body = params
            self.__last_request = request
            json_string = """{ "headwayTime": "PT3M30S"}"""

            return SessionMockFactory.create_response_mock(json_string, 200)

    @mock.patch('requests.Session', side_effect=GetDefaultHeadwayTimeTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetDefaultHeadwayTimeTestMockSession)
    def test_get_default_headway_time_request_section_track_only(self, mocked_get_obj):
        section_track_id = 5332
        from_node_id = None
        to_node_id = None

        self.interface_to_viriato.get_default_headway_time(section_track_id, from_node_id, to_node_id)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetDefaultHeadwayTimeTestMockSession__last_request,
                         get_api_url() + "/section-tracks/5332/headway-times")

        self.assertDictEqual(session_obj._GetDefaultHeadwayTimeTestMockSession__last_body, dict())

    @mock.patch('requests.Session', side_effect=GetDefaultHeadwayTimeTestMockSession)
    def test_get_default_headway_time_request_section_track_and_from_node_id(self, mocked_get_obj):
        section_track_id = 5332
        from_node_id = 15
        to_node_id = None

        self.interface_to_viriato.get_default_headway_time(section_track_id, from_node_id, to_node_id)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetDefaultHeadwayTimeTestMockSession__last_request,
                         get_api_url() + "/section-tracks/5332/headway-times")

        self.assertDictEqual(session_obj._GetDefaultHeadwayTimeTestMockSession__last_body, dict(fromNodeId=15))

    @mock.patch('requests.Session', side_effect=GetDefaultHeadwayTimeTestMockSession)
    def test_get_default_headway_time_request_section_track_and_to_node_id(self, mocked_get_obj):
        section_track_id = 5332
        from_node_id = None
        to_node_id = 50

        self.interface_to_viriato.get_default_headway_time(section_track_id, from_node_id, to_node_id)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetDefaultHeadwayTimeTestMockSession__last_request,
                         get_api_url() + "/section-tracks/5332/headway-times")

        self.assertDictEqual(session_obj._GetDefaultHeadwayTimeTestMockSession__last_body, dict(toNodeId=50))

    @mock.patch('requests.Session', side_effect=GetDefaultHeadwayTimeTestMockSession)
    def test_get_default_headway_time_request_all_parameters_defined(self, mocked_get_obj):
        section_track_id = 5332
        from_node_id = 125
        to_node_id = 50

        self.interface_to_viriato.get_default_headway_time(section_track_id, from_node_id, to_node_id)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetDefaultHeadwayTimeTestMockSession__last_request,
                         get_api_url() + "/section-tracks/5332/headway-times")

        self.assertDictEqual(session_obj._GetDefaultHeadwayTimeTestMockSession__last_body,
                             dict(fromNodeId=125, toNodeId=50))

    @mock.patch('requests.Session', side_effect=GetDefaultHeadwayTimeTestMockSession)
    def test_get_default_headway_time_response(self, mocked_get_obj):
        section_track_id = 5332
        from_node_id = 125
        to_node_id = 50

        headway_time = self.interface_to_viriato.get_default_headway_time(section_track_id, from_node_id, to_node_id)

        self.assertIsInstance(headway_time, datetime.timedelta)
        self.assertEqual(headway_time, datetime.timedelta(minutes=3, seconds=30))

    @mock.patch('requests.Session', side_effect=GetDefaultHeadwayTimeTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
