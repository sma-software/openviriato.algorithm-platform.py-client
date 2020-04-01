import datetime
import json
import unittest

import Conversion.object_to_algorithm_platform_json_converter
from AIDMClasses import AIDM_classes


class TestFromAIDMConverter(unittest.TestCase):

    def test_convert_AIDM_object_with_properties_to_convert(self):
        test_train_path_node = AIDM_classes.TrainPathNode(ID=11038, SectionTrackID=None, NodeID=18, NodeTrackID=None,
                                                          FormationID=1187, ArrivalTime=
                                                          datetime.datetime(year=1, month=5, day=1, hour=1, minute=1),
                                                          DepartureTime=
                                                          datetime.datetime(year=1, month=5, day=1, hour=1, minute=1),
                                                          MinimumRunTime=None, MinimumStopTime=datetime.timedelta(0),
                                                          StopStatus=AIDM_classes.StopStatus['passing'],
                                                          SequenceNumber=0)

        test_node_as_dict = Conversion.object_to_algorithm_platform_json_converter.convert_any_object(test_train_path_node)

        self.assertIsInstance(test_node_as_dict, dict)
        self.assertEqual(test_node_as_dict['ID'], 11038)
        self.assertEqual(test_node_as_dict['SectionTrackID'], None)
        self.assertEqual(test_node_as_dict['StopStatus'], 'passing')

    def test_convert_AIDM_object_with_properties_is_json_conform_dict(self):
        test_train_path_node = AIDM_classes.TrainPathNode(ID=11038, SectionTrackID=None, NodeID=18, NodeTrackID=None,
                                                          FormationID=1187, ArrivalTime=
                                                          datetime.datetime(year=1, month=5, day=1, hour=1, minute=1),
                                                          DepartureTime=
                                                          datetime.datetime(year=1, month=5, day=1, hour=1, minute=1),
                                                          MinimumRunTime=None, MinimumStopTime=datetime.timedelta(0),
                                                          StopStatus=AIDM_classes.StopStatus['passing'],
                                                          SequenceNumber=0)

        test_node_as_dict = Conversion.object_to_algorithm_platform_json_converter.convert_any_object(test_train_path_node)
        test_node_as_json = json.dumps(test_node_as_dict)

        expected_json_string = '{"ID": 11038, "ArrivalTime": "0001-05-01T01:01:00", ' \
                               '"DepartureTime": "0001-05-01T01:01:00", "SectionTrackID": null, "NodeID": 18, ' \
                               '"NodeTrackID": null, "FormationID": 1187, "MinimumRunTime": null, ' \
                               '"MinimumStopTime": "P0D", "StopStatus": "passing", "SequenceNumber": 0}'

        self.assertEqual(test_node_as_json, expected_json_string)

    def test_convert_to_list_of_dict_empty(self):
        test_list_of_dict = []

        test_section_list = Conversion.object_to_algorithm_platform_json_converter.convert_any_object(test_list_of_dict)

        self.assertIsInstance(test_section_list, list)
        self.assertListEqual(test_section_list, [])

    def test_convert_list(self):
        algorithm_section_track = AIDM_classes.AlgorithmSectionTrack(ID=12, Code='ATest', DebugString='str', Weight=8,
                                                                     SectionCode='TestSection')
        test_list_of_algorithm_section_track = [algorithm_section_track, algorithm_section_track]

        test_section_list_of_dict = Conversion.object_to_algorithm_platform_json_converter.convert_any_object(test_list_of_algorithm_section_track)

        self.assertIsInstance(test_section_list_of_dict, list)
        self.assertIsInstance(test_section_list_of_dict[0], dict)
        self.assertEqual(test_section_list_of_dict[0]['DebugString'], 'str')
