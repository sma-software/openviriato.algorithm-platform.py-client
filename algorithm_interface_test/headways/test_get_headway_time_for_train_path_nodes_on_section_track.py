import datetime
import unittest
from unittest import mock

import algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client.algorithm_interface import algorithm_interface_factory
from algorithm_interface_test.test_helper.SessionMockTestBase import \
    get_api_url, \
    SessionMockTestBase


class TestGetHeadwayTimeForTrainPathNodesOnSectionTrack(unittest.TestCase):
    class GetHeadwayTimeForTrainPathNodesOnSectionTrackTestMockSession(SessionMockTestBase):
        # to replace session.get:
        def get(self, request, params):
            self.__last_body = params
            self.__last_request = request
            json_string = """{ "headwayTime": "PT2M54S"}"""

            return SessionMockFactory.create_response_mock(json_string, 200)

    @mock.patch('requests.Session', side_effect=GetHeadwayTimeForTrainPathNodesOnSectionTrackTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetHeadwayTimeForTrainPathNodesOnSectionTrackTestMockSession)
    def test_get_headway_time_for_train_path_nodes_on_section_track_request(self, mocked_get_obj):
        proceeding_node_id = 4246
        succeeding_node_id = 2
        section_track_id = 9998
        from_node_id = 162
        to_node_id = 348

        self.interface_to_viriato.get_headway_time_for_train_path_nodes_on_section_track(proceeding_node_id,
                                                                                         succeeding_node_id,
                                                                                         section_track_id,
                                                                                         from_node_id, to_node_id)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetHeadwayTimeForTrainPathNodesOnSectionTrackTestMockSession__last_request,
                         get_api_url() + "/headway-times/between-train-path-nodes/4246/2/for-section-track/9998/in"
                                         "-direction/162/348")
        self.assertDictEqual(session_obj._GetHeadwayTimeForTrainPathNodesOnSectionTrackTestMockSession__last_body, {})

    @mock.patch('requests.Session', side_effect=GetHeadwayTimeForTrainPathNodesOnSectionTrackTestMockSession)
    def test_get_headway_time_for_train_path_nodes_on_section_track_response(self, mocked_get_obj):
        proceeding_node_id = 4246
        succeeding_node_id = 2
        section_track_id = 9998
        from_node_id = 162
        to_node_id = 348

        headway_timedelta = self.interface_to_viriato.get_headway_time_for_train_path_nodes_on_section_track(
            proceeding_node_id,
            succeeding_node_id,
            section_track_id,
            from_node_id, to_node_id)

        self.assertIsInstance(headway_timedelta, datetime.timedelta)
        self.assertEqual(datetime.timedelta(seconds=174), headway_timedelta)

    @mock.patch('requests.Session', side_effect=GetHeadwayTimeForTrainPathNodesOnSectionTrackTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
