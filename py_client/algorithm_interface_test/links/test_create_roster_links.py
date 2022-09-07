import unittest
from unittest import mock

from py_client.aidm import AlgorithmRosterLink, AlgorithmRosterLinkDefinition
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper import SessionMockFactory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import SessionMockTestBase, get_api_url


class TestCreateRosterLinks(unittest.TestCase):
    class CreateRosterLinksTestMockSession(SessionMockTestBase):
        def post(self, request, json):
            self._last_body = json
            self._last_request = request
            if len(self._last_body) == 0:
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
                    '        "id": 6542,\n'
                    '        "debugString": "DebugStringTest+-+asd"\n'
                    "    }"
                    "]"
                )

            return SessionMockFactory.create_response_mock(json_string, 200)

    @mock.patch("requests.Session", side_effect=CreateRosterLinksTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch("requests.Session", side_effect=CreateRosterLinksTestMockSession)
    def test_create_roster_links(self, mocked_get_obj):
        roster_link_definition = AlgorithmRosterLinkDefinition(1, 20, 200, 2000)

        self.interface_to_viriato.create_roster_links([roster_link_definition])

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj.last_request, get_api_url() + "/links")
        expected_body = [
            dict(
                fromTrainPathNodeId=1,
                toTrainPathNodeId=20,
                fromVehiclePositionInFormation=200,
                toVehiclePositionInFormation=2000,
                type="roster",
            )
        ]
        self.assertListEqual(session_obj.last_body, expected_body)

    @mock.patch("requests.Session", side_effect=CreateRosterLinksTestMockSession)
    def test_create_roster_links_one_link_as_response(self, mocked_get_obj):
        roster_link_definition = AlgorithmRosterLinkDefinition(1, 20, 200, 2000)

        listed_roster_links = self.interface_to_viriato.create_roster_links([roster_link_definition])

        self.assertIsInstance(listed_roster_links, list)
        self.assertEqual(listed_roster_links.__len__(), 1)

        self.assertIsInstance(listed_roster_links[0], AlgorithmRosterLink)
        algorithm_roster_link: AlgorithmRosterLink = listed_roster_links.pop()
        self.assertEqual(algorithm_roster_link.from_node_id, 639)
        self.assertEqual(algorithm_roster_link.from_train_id, 11078)
        self.assertEqual(algorithm_roster_link.from_train_path_node_id, 11076)
        self.assertEqual(algorithm_roster_link.to_node_id, 622)
        self.assertEqual(algorithm_roster_link.to_train_id, 11083)
        self.assertEqual(algorithm_roster_link.to_train_path_node_id, 11079)
        self.assertEqual(algorithm_roster_link.debug_string, "DebugStringTest+-+asd")

    @mock.patch("requests.Session", side_effect=CreateRosterLinksTestMockSession)
    def test_get_roster_links_empty_list_as_response(self, mocked_get_obj):

        listed_roster_links = self.interface_to_viriato.create_roster_links([])

        self.assertIsInstance(listed_roster_links, list)
        self.assertEqual(listed_roster_links.__len__(), 0)

    @mock.patch("requests.Session", side_effect=CreateRosterLinksTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
