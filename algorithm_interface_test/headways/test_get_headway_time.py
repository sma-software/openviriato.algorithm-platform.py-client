import datetime
import unittest
from unittest import mock
import algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client.algorithm_interface import algorithm_interface_factory
from algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestGetHeadwayTime(unittest.TestCase):
    class GetHeadwayTimeTestMockSession(SessionMockTestBase):
        def get(self, request, params):
            self.__last_body = params
            self.__last_request = request
            json_string = """{ "headwayTime": "PT5M12S"}"""

            return SessionMockFactory.create_response_mock(json_string, 200)

    @mock.patch('requests.Session', side_effect=GetHeadwayTimeTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetHeadwayTimeTestMockSession)
    def test_get_headway_time_request_non_optional_parameters_only(self, mocked_get_obj):
        section_track_id = 5332
        from_node_id = None
        to_node_id = None
        preceding_train_path_node_id = 12
        succeeding_train_path_node_id = 13

        self.interface_to_viriato.get_headway_time(
            section_track_id,
            from_node_id,
            to_node_id,
            preceding_train_path_node_id,
            succeeding_train_path_node_id)

        expected_parameter_dict = dict(PrecedingTrainPathNodeID=12, SucceedingTrainPathNodeID=13)
        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetHeadwayTimeTestMockSession__last_request,
                         get_api_url() + "/section-tracks/5332/headway-times")
        self.assertDictEqual(session_obj._GetHeadwayTimeTestMockSession__last_body, expected_parameter_dict)

    @mock.patch('requests.Session', side_effect=GetHeadwayTimeTestMockSession)
    def test_get_headway_time_request_non_optional_parameters_and_from_node_id(self, mocked_get_obj):
        section_track_id = 5332
        from_node_id = 99
        to_node_id = None
        preceding_train_path_node_id = 12
        succeeding_train_path_node_id = 13

        self.interface_to_viriato.get_headway_time(
            section_track_id,
            from_node_id,
            to_node_id,
            preceding_train_path_node_id,
            succeeding_train_path_node_id)

        expected_parameter_dict = dict(
            FromNodeID=99,
            PrecedingTrainPathNodeID=12,
            SucceedingTrainPathNodeID=13)
        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetHeadwayTimeTestMockSession__last_request,
                         get_api_url() + "/section-tracks/5332/headway-times")
        self.assertDictEqual(session_obj._GetHeadwayTimeTestMockSession__last_body, expected_parameter_dict)

    @mock.patch('requests.Session', side_effect=GetHeadwayTimeTestMockSession)
    def test_get_headway_time_request_non_optional_parameters_and_to_node_id(self, mocked_get_obj):
        section_track_id = 5332
        from_node_id = None
        to_node_id = 270
        preceding_train_path_node_id = 12
        succeeding_train_path_node_id = 13

        self.interface_to_viriato.get_headway_time(
            section_track_id,
            from_node_id,
            to_node_id,
            preceding_train_path_node_id,
            succeeding_train_path_node_id)

        expected_parameter_dict = dict(
            ToNodeID=270,
            PrecedingTrainPathNodeID=12,
            SucceedingTrainPathNodeID=13)
        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetHeadwayTimeTestMockSession__last_request,
                         get_api_url() + "/section-tracks/5332/headway-times")
        self.assertDictEqual(session_obj._GetHeadwayTimeTestMockSession__last_body, expected_parameter_dict)

    @mock.patch('requests.Session', side_effect=GetHeadwayTimeTestMockSession)
    def test_get_headway_time_request_all_parameters_defined(self, mocked_get_obj):
        section_track_id = 5332
        from_node_id = 99
        to_node_id = 270
        preceding_train_path_node_id = 12
        succeeding_train_path_node_id = 13

        self.interface_to_viriato.get_headway_time(
            section_track_id,
            from_node_id,
            to_node_id,
            preceding_train_path_node_id,
            succeeding_train_path_node_id)

        expected_parameter_dict = dict(
            FromNodeID=99,
            ToNodeID=270,
            PrecedingTrainPathNodeID=12,
            SucceedingTrainPathNodeID=13)
        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetHeadwayTimeTestMockSession__last_request,
                         get_api_url() + "/section-tracks/5332/headway-times")
        self.assertDictEqual(session_obj._GetHeadwayTimeTestMockSession__last_body, expected_parameter_dict)

    @mock.patch('requests.Session', side_effect=GetHeadwayTimeTestMockSession)
    def test_get_headway_time_response(self, mocked_get_obj):
        section_track_id = 5332
        from_node_id = 99
        to_node_id = 270
        preceding_train_path_node_id = 12
        succeeding_train_path_node_id = 13

        headway_time = self.interface_to_viriato.get_headway_time(
            section_track_id,
            from_node_id,
            to_node_id,
            preceding_train_path_node_id,
            succeeding_train_path_node_id)

        self.assertIsInstance(headway_time, datetime.timedelta)
        self.assertEqual(headway_time, datetime.timedelta(minutes=5, seconds=12))

    @mock.patch('requests.Session', side_effect=GetHeadwayTimeTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
