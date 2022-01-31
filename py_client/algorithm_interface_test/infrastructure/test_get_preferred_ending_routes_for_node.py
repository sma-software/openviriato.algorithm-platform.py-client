from unittest import mock, TestCase

from py_client.aidm import OutgoingNodeTrackRoutingEdge, IncomingNodeTrackRoutingEdge
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper import SessionMockFactory as SessionMockFactory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestGetPreferredEndingRoutesForNode(TestCase):
    class GetPreferredEndingRoutesForNodeTestMock(SessionMockTestBase):
        def get(self, request: str, params: dict):
            self._last_body = params
            self._last_request = request

            json_string = (
                "[\n"
                "  {\n"
                "    \"incomingRoutingEdge\": {\n"
                "      \"startSectionTrackId\": 1204,\n"
                "      \"endNodeTrackId\": 19,\n"
                "      \"type\": \"incomingNodeTrack\",\n"
                "      \"nodeId\": 18\n"
                "    },\n"
                "    \"outgoingRoutingEdge\": null\n"
                "  },\n"
                "  {\n"
                "    \"incomingRoutingEdge\": {\n"
                "      \"startSectionTrackId\": 1206,\n"
                "      \"endNodeTrackId\": 20,\n"
                "      \"type\": \"incomingNodeTrack\",\n"
                "      \"nodeId\": 18\n"
                "    },\n"
                "    \"outgoingRoutingEdge\": null\n"
                "  },\n"
                "  {\n"
                "    \"incomingRoutingEdge\": {\n"
                "      \"startSectionTrackId\": 1207,\n"
                "      \"endNodeTrackId\": 21,\n"
                "      \"type\": \"incomingNodeTrack\",\n"
                "      \"nodeId\": 18\n"
                "    },\n"
                "    \"outgoingRoutingEdge\": null\n"
                "  }\n"
                "]"
            )

            return SessionMockFactory.create_response_mock(json_string, 200)

    @mock.patch('requests.Session', side_effect=GetPreferredEndingRoutesForNodeTestMock)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetPreferredEndingRoutesForNodeTestMock)
    def test_get_preferred_routes_request_all_arguments(self, mocked_get_obj):
        node_id = 1082
        start_section_track_id = 500
        self.interface_to_viriato.get_preferred_ending_routes_for_node(node_id, start_section_track_id)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession

        self.assertEqual(session_obj.last_request, get_api_url() + '/nodes/1082/preferred-routes')
        self.assertEqual(session_obj.last_body, {'endInNode': True, 'startSectionTrackID': 500, 'startInNode': False})

    @mock.patch('requests.Session', side_effect=GetPreferredEndingRoutesForNodeTestMock)
    def test_get_preferred_routes_request_only_node_id(self, mocked_get_obj):
        node_id = 1024
        start_section_track_id = None
        self.interface_to_viriato.get_preferred_ending_routes_for_node(node_id, start_section_track_id)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession

        self.assertEqual(session_obj.last_request, get_api_url() + '/nodes/1024/preferred-routes')
        self.assertEqual(session_obj.last_body, {'endInNode': True, 'startSectionTrackID': None, 'startInNode': False})

    @mock.patch('requests.Session', side_effect=GetPreferredEndingRoutesForNodeTestMock)
    def test_get_preferred_routes_return(self, mocked_get_obj):
        node_id = 1082
        start_section_track_id = 500
        test_routes = self.interface_to_viriato.get_preferred_ending_routes_for_node(node_id, start_section_track_id)

        self.assertIsInstance(test_routes, list)
        self.assertEqual(len(test_routes), 3)

        first_routing_edge_pair = test_routes[0]
        self.assertIsInstance(first_routing_edge_pair.incoming_routing_edge, IncomingNodeTrackRoutingEdge)
        self.assertEqual(first_routing_edge_pair.incoming_routing_edge.node_id, 18)
        self.assertEqual(first_routing_edge_pair.incoming_routing_edge.end_node_track_id, 19)
        self.assertEqual(first_routing_edge_pair.incoming_routing_edge.start_section_track_id, 1204)
        self.assertIsNone(first_routing_edge_pair.outgoing_routing_edge)

        second_routing_edge_pair = test_routes[1]
        self.assertIsInstance(second_routing_edge_pair.incoming_routing_edge, IncomingNodeTrackRoutingEdge)
        self.assertEqual(second_routing_edge_pair.incoming_routing_edge.node_id, 18)
        self.assertEqual(second_routing_edge_pair.incoming_routing_edge.end_node_track_id, 20)
        self.assertEqual(second_routing_edge_pair.incoming_routing_edge.start_section_track_id, 1206)
        self.assertIsNone(second_routing_edge_pair.outgoing_routing_edge)

        third_routing_edge_pair = test_routes[2]
        self.assertIsInstance(third_routing_edge_pair.incoming_routing_edge, IncomingNodeTrackRoutingEdge)
        self.assertEqual(third_routing_edge_pair.incoming_routing_edge.node_id, 18)
        self.assertEqual(third_routing_edge_pair.incoming_routing_edge.end_node_track_id, 21)
        self.assertEqual(third_routing_edge_pair.incoming_routing_edge.start_section_track_id, 1207)
        self.assertIsNone(third_routing_edge_pair.outgoing_routing_edge)

    @mock.patch('requests.Session', side_effect=GetPreferredEndingRoutesForNodeTestMock)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
