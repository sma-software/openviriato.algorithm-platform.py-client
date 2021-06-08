from unittest import mock, TestCase

from py_client.aidm import OutgoingNodeTrackRoutingEdge
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper import SessionMockFactory as SessionMockFactory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestGetPreferredStartingRoutesForNode(TestCase):
    class GetPreferredStartingRoutesForNodeTestMock(SessionMockTestBase):
        def get(self, request: str, params: dict):
            self._last_body = params
            self._last_request = request

            json_string = (
                "[\n"
                "  {\n"
                "    \"incomingRoutingEdge\": null,\n"
                "    \"outgoingRoutingEdge\": {\n"
                "      \"startNodeTrackId\": 21,\n"
                "      \"endSectionTrackId\": 1207,\n"
                "      \"type\": \"outgoing\",\n"
                "      \"nodeId\": 18\n"
                "    }\n"
                "  }\n"
                "]"
            )

            return SessionMockFactory.create_response_mock(json_string, 200)

    @mock.patch('requests.Session', side_effect=GetPreferredStartingRoutesForNodeTestMock)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetPreferredStartingRoutesForNodeTestMock)
    def test_get_preferred_routes_request_all_arguments(self, mocked_get_obj):
        node_id = 1082
        end_section_track_id = 123123
        self.interface_to_viriato.get_preferred_starting_routes_for_node(node_id, end_section_track_id)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession

        self.assertEqual(session_obj.last_request, get_api_url() + '/nodes/1082/preferred-routes')
        self.assertEqual(session_obj.last_body, {'endInNode': False, 'endSectionTrackID': 123123, 'startInNode': True})

    @mock.patch('requests.Session', side_effect=GetPreferredStartingRoutesForNodeTestMock)
    def test_get_preferred_routes_request_only_node_id(self, mocked_get_obj):
        node_id = 1024
        end_section_track_id = None
        self.interface_to_viriato.get_preferred_starting_routes_for_node(node_id, end_section_track_id)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession

        self.assertEqual(session_obj.last_request, get_api_url() + '/nodes/1024/preferred-routes')
        self.assertEqual(session_obj.last_body, {'endInNode': False, 'endSectionTrackID': None, 'startInNode': True})

    @mock.patch('requests.Session', side_effect=GetPreferredStartingRoutesForNodeTestMock)
    def test_get_preferred_routes_return(self, mocked_get_obj):
        node_id = 1082
        end_section_track_id = 1123
        test_routes = self.interface_to_viriato.get_preferred_starting_routes_for_node(node_id, end_section_track_id)

        self.assertIsInstance(test_routes, list)
        self.assertEqual(len(test_routes), 1)

        first_routing_edge_pair = test_routes[0]
        self.assertIsNone(first_routing_edge_pair.incoming_routing_edge)
        self.assertIsInstance(first_routing_edge_pair.outgoing_routing_edge, OutgoingNodeTrackRoutingEdge)
        self.assertEqual(first_routing_edge_pair.outgoing_routing_edge.node_id, 18)
        self.assertEqual(first_routing_edge_pair.outgoing_routing_edge.start_node_track_id, 21)
        self.assertEqual(first_routing_edge_pair.outgoing_routing_edge.end_section_track_id, 1207)

    @mock.patch('requests.Session', side_effect=GetPreferredStartingRoutesForNodeTestMock)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
