import datetime
import json
import unittest

import py_client.conversion.object_to_algorithm_platform_json_converter
from py_client.aidm import AlgorithmSectionTrack, AlgorithmTrainPathNode, StopStatus


class TestFromAIDMConverter(unittest.TestCase):

    def test_convert_aidm_object_with_properties_to_convert(self):
        test_train_path_node = AlgorithmTrainPathNode(
            id=11038, section_track_id=None, node_id=18, node_track_id=None, formation_id=1187,
            arrival_time=datetime.datetime(year=1, month=5, day=1, hour=1, minute=1),
            departure_time=datetime.datetime(year=1, month=5, day=1, hour=1, minute=1),
            minimum_run_time=None, minimum_stop_time=datetime.timedelta(0),
            stop_status=StopStatus['operational_stop'], sequence_number=0)

        test_node_as_dict = py_client.conversion.object_to_algorithm_platform_json_converter.convert_any_object(
            test_train_path_node)

        self.assertIsInstance(test_node_as_dict, dict)
        self.assertEqual(test_node_as_dict['ID'], 11038)
        self.assertEqual(test_node_as_dict['SectionTrackID'], None)
        self.assertEqual(test_node_as_dict['StopStatus'], 'OperationalStop')

    def test_convert_aidm_object_with_properties_is_json_conform_dict(self):
        test_train_path_node = AlgorithmTrainPathNode(
            id=11038, section_track_id=None, node_id=18, node_track_id=None, formation_id=1187,
            arrival_time=datetime.datetime(year=1, month=5, day=1, hour=1, minute=1),
            departure_time=datetime.datetime(year=1, month=5, day=1, hour=1, minute=1),
            minimum_run_time=None, minimum_stop_time=datetime.timedelta(0),
            stop_status=StopStatus['passing'], sequence_number=0)

        test_node_as_dict = py_client.conversion.object_to_algorithm_platform_json_converter.convert_any_object(
            test_train_path_node)
        test_node_as_json = json.dumps(test_node_as_dict)

        expected_json_string = '{"ID": 11038, "ArrivalTime": "0001-05-01T01:01:00", ' \
                               '"DepartureTime": "0001-05-01T01:01:00", "SectionTrackID": null, "NodeID": 18, ' \
                               '"NodeTrackID": null, "FormationID": 1187, "MinimumRunTime": null, ' \
                               '"MinimumStopTime": "P0D", "StopStatus": "Passing", "SequenceNumber": 0}'

        self.assertEqual(test_node_as_json, expected_json_string)

    def test_convert_list_empty(self):
        test_list_of_dict = []

        test_section_list = py_client.conversion.object_to_algorithm_platform_json_converter.convert_any_object(
            test_list_of_dict)

        self.assertIsInstance(test_section_list, list)
        self.assertListEqual(test_section_list, [])

    def test_convert_list(self):
        algorithm_section_track = AlgorithmSectionTrack(id=12, code='ATest', debug_string='str', weight=8,
                                                        section_code='TestSection')
        test_list_of_algorithm_section_track = [algorithm_section_track, algorithm_section_track]

        test_section_list_of_dict = py_client.conversion.object_to_algorithm_platform_json_converter.convert_any_object(
            test_list_of_algorithm_section_track)

        self.assertIsInstance(test_section_list_of_dict, list)
        self.assertIsInstance(test_section_list_of_dict[0], dict)
        self.assertEqual(test_section_list_of_dict[0]['DebugString'], 'str')
