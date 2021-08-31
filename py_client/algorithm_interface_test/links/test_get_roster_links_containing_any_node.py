import datetime
import unittest
from unittest import mock

from py_client.aidm import TimeWindow, AlgorithmRosterLink
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper import SessionMockFactory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import SessionMockTestBase, get_api_url


class TestGetRosterLinksContainingAnyNode(unittest.TestCase):
    class GetRosterLinksContainingAnyNodeTestMockSession(SessionMockTestBase):
        def get(self, request, params):
            self._last_body = params
            self._last_request = request
            if params["fromTime"] == params["toTime"]:
                json_string = "[]"
            else:
                json_string = (
                    "[\n"
                    "    {\n"
                    "        \"fromVehiclePositionInFormation\": 0,\n"
                    "        \"toVehiclePositionInFormation\": 5,\n"
                    "        \"fromNodeId\": 639,\n"
                    "        \"fromTrainId\": 11078,\n"
                    "        \"fromTrainPathNodeId\": 11076,\n"
                    "        \"toNodeId\": 622,\n"
                    "        \"toTrainId\": 11083,\n"
                    "        \"toTrainPathNodeId\": 11079,\n"
                    "        \"type\": \"roster\",\n"
                    "        \"debugString\": \"string\"\n"
                    "    },\n"
                    "    {\n"
                    "        \"fromVehiclePositionInFormation\": 2,\n"
                    "        \"toVehiclePositionInFormation\": 3,\n"
                    "        \"fromNodeId\": 639,\n"
                    "        \"fromTrainId\": 11078,\n"
                    "        \"fromTrainPathNodeId\": 11076,\n"
                    "        \"toNodeId\": 622,\n"
                    "        \"toTrainId\": 11083,\n"
                    "        \"toTrainPathNodeId\": 11079,\n"
                    "        \"type\": \"roster\",\n"
                    "        \"debugString\": \"string\"\n"
                    "    }\n"
                    "]"
                )

            return SessionMockFactory.create_response_mock(json_string, 200)

    @mock.patch('requests.Session', side_effect=GetRosterLinksContainingAnyNodeTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetRosterLinksContainingAnyNodeTestMockSession)
    def test_get_roster_links_containing_any_node_request(self, mocked_get_obj):
        time_window = TimeWindow(
            from_time=datetime.datetime(2000, 1, 1, 1, 1), to_time=datetime.datetime(2004, 1, 1, 0, 0)
        )
        node_ids = [12]

        self.interface_to_viriato.get_roster_links_containing_any_node(time_window, node_ids)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj.last_request, get_api_url() + '/links')
        self.assertDictEqual(
            session_obj.last_body,
            dict(fromTime="2000-01-01T01:01:00", toTime="2004-01-01T00:00:00", nodeFilter=[12], linkType="roster")
        )

    @mock.patch('requests.Session', side_effect=GetRosterLinksContainingAnyNodeTestMockSession)
    def test_get_roster_links_containing_any_node_one_link_as_response(self, mocked_get_obj):
        time_window = TimeWindow(
            from_time=datetime.datetime(2000, 1, 1, 1, 1), to_time=datetime.datetime(2004, 1, 1, 0, 0)
        )
        node_ids = [12]

        links = self.interface_to_viriato.get_roster_links_containing_any_node(time_window, node_ids)

        self.assertIsInstance(links, list)
        self.assertEqual(links.__len__(), 2)

        self.assertIsInstance(links[0], AlgorithmRosterLink)
        algorithm_roster_link: AlgorithmRosterLink = links[0]
        self.assertEqual(algorithm_roster_link.from_node_id, 639)
        self.assertEqual(algorithm_roster_link.from_train_id, 11078)
        self.assertEqual(algorithm_roster_link.from_train_path_node_id, 11076)
        self.assertEqual(algorithm_roster_link.to_node_id, 622)
        self.assertEqual(algorithm_roster_link.to_train_id, 11083)
        self.assertEqual(algorithm_roster_link.to_train_path_node_id, 11079)
        self.assertEqual(algorithm_roster_link.debug_string, "string")

    @mock.patch('requests.Session', side_effect=GetRosterLinksContainingAnyNodeTestMockSession)
    def get_roster_links_containing_any_node_empty_list_as_response(self, mocked_get_obj):
        time_window = TimeWindow(
            from_time=datetime.datetime(2000, 1, 1, 1, 1), to_time=datetime.datetime(2000, 1, 1, 1, 1)
        )
        node_ids = [12]

        links = self.interface_to_viriato.get_roster_links_containing_any_node(time_window, node_ids)

        self.assertIsInstance(links, list)
        self.assertEqual(links.__len__(), 0)

    @mock.patch('requests.Session', side_effect=GetRosterLinksContainingAnyNodeTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
