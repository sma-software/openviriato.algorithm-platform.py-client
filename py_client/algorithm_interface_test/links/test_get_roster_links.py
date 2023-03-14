from datetime import datetime
import unittest
from unittest import mock

from py_client.aidm import TimeWindow, AlgorithmRosterLink
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper import SessionMockFactory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import SessionMockTestBase, get_api_url


class TestGetRosterLinks(unittest.TestCase):
    class GetRosterLinksTestMockSession(SessionMockTestBase):
        def get(self, request, params):
            self._last_body = params
            self._last_request = request
            if params["fromTime"] == params["toTime"]:
                json_string = "[]"
            else:
                json_string = (
                    "[\n"
                    "    {\n"
                    '        "fromVehiclePositionInFormation": 0,\n'
                    '        "toVehiclePositionInFormation": 5,\n'
                    '        "fromNodeId": 639,\n'
                    '        "fromTrainId": 11078,\n'
                    '        "fromTrainPathNodeId": 11076,\n'
                    '        "toNodeId": 622,\n'
                    '        "toTrainId": 11083,\n'
                    '        "toTrainPathNodeId": 11079,\n'
                    '        "type": "roster",\n'
                    '        "id": 286,\n'
                    '        "debugString": "DebugString"\n'
                    "    },\n"
                    "    {\n"
                    '        "fromVehiclePositionInFormation": 2,\n'
                    '        "toVehiclePositionInFormation": 3,\n'
                    '        "fromNodeId": 639,\n'
                    '        "fromTrainId": 11078,\n'
                    '        "fromTrainPathNodeId": 11076,\n'
                    '        "toNodeId": 622,\n'
                    '        "toTrainId": 11083,\n'
                    '        "toTrainPathNodeId": 11079,\n'
                    '        "type": "roster",\n'
                    '        "id": 7984,\n'
                    '        "debugString": "link: FV_31_J03, 85ZSTH, planned arrival: '
                    "        30.04.2003 09:05.0 - FV_30_J03, 85ZMUS, "
                    '         planned departure: 30.04.2003 09:20.0, vehicles: from 710 to 710"\n'
                    "    }\n"
                    "]"
                )

            return SessionMockFactory.create_response_mock(json_string, 200)

    @mock.patch("requests.Session", side_effect=GetRosterLinksTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch("requests.Session", side_effect=GetRosterLinksTestMockSession)
    def test_get_roster_links(self, mocked_get_obj):
        time_window = TimeWindow(from_time=datetime(2000, 1, 1, 1, 1), to_time=datetime(2004, 1, 1, 0, 0))

        self.interface_to_viriato.get_roster_links(time_window)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj.last_request, get_api_url() + "/links")
        self.assertDictEqual(session_obj.last_body, dict(fromTime="2000-01-01T01:01:00", toTime="2004-01-01T00:00:00", linkType="roster", nodeFilter=None))

    @mock.patch("requests.Session", side_effect=GetRosterLinksTestMockSession)
    def test_get_roster_links_one_link_as_response(self, mocked_get_obj):
        time_window = TimeWindow(from_time=datetime(2000, 1, 1, 1, 1), to_time=datetime(2004, 1, 1, 0, 0))

        listed_roster_links = self.interface_to_viriato.get_roster_links(time_window)

        self.assertIsInstance(listed_roster_links, list)
        self.assertEqual(listed_roster_links.__len__(), 2)

        self.assertIsInstance(listed_roster_links[0], AlgorithmRosterLink)
        algorithm_roster_link: AlgorithmRosterLink = listed_roster_links[0]
        self.assertEqual(algorithm_roster_link.from_node_id, 639)
        self.assertEqual(algorithm_roster_link.from_train_id, 11078)
        self.assertEqual(algorithm_roster_link.from_train_path_node_id, 11076)
        self.assertEqual(algorithm_roster_link.to_node_id, 622)
        self.assertEqual(algorithm_roster_link.to_train_id, 11083)
        self.assertEqual(algorithm_roster_link.to_train_path_node_id, 11079)
        self.assertEqual(algorithm_roster_link.debug_string, "DebugString")

    @mock.patch("requests.Session", side_effect=GetRosterLinksTestMockSession)
    def test_get_roster_links_empty_list_as_response(self, mocked_get_obj):
        time_window = TimeWindow(from_time=datetime(2000, 1, 1, 1, 1), to_time=datetime(2000, 1, 1, 1, 1))

        listed_algorithm_links = self.interface_to_viriato.get_await_arrival_links(time_window)

        self.assertIsInstance(listed_algorithm_links, list)
        self.assertEqual(listed_algorithm_links.__len__(), 0)

    @mock.patch("requests.Session", side_effect=GetRosterLinksTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
