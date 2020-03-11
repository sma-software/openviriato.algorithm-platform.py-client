import datetime
import json
import unittest

import ConverterLayer.from_AIDM_converter
from AIDMClasses import AIDM_classes


class TestFromAIDMConverter(unittest.TestCase):

    def test_convert_to_json_conform_dict_return(self):
        test_train_path_node = AIDM_classes.TrainPathNode(ID=11038, SectionTrackID=None, NodeID=18, NodeTrackID=None,
                                                          FormationID=1187, ArrivalTime=
                                                          datetime.datetime(year=1, month=5, day=1, hour=1, minute=1),
                                                          DepartureTime=
                                                          datetime.datetime(year=1, month=5, day=1, hour=1, minute=1),
                                                          MinimumRunTime=None, MinimumStopTime=datetime.timedelta(0),
                                                          StopStatus=AIDM_classes.StopStatus['passing'],
                                                          SequenceNumber=0)

        test_node_as_dict = ConverterLayer.from_AIDM_converter.convert_to_json_conform_dict(test_train_path_node)

        self.assertIsInstance(test_node_as_dict, dict)
        self.assertEqual(test_node_as_dict['ID'], 11038)
        self.assertEqual(test_node_as_dict['SectionTrackID'], None)
        self.assertEqual(test_node_as_dict['StopStatus'], 'passing')

    def test_convert_to_json_conform_dict_return_to_json(self):
        test_train_path_node = AIDM_classes.TrainPathNode(ID=11038, SectionTrackID=None, NodeID=18, NodeTrackID=None,
                                                          FormationID=1187, ArrivalTime=
                                                          datetime.datetime(year=1, month=5, day=1, hour=1, minute=1),
                                                          DepartureTime=
                                                          datetime.datetime(year=1, month=5, day=1, hour=1, minute=1),
                                                          MinimumRunTime=None, MinimumStopTime=datetime.timedelta(0),
                                                          StopStatus=AIDM_classes.StopStatus['passing'],
                                                          SequenceNumber=0)

        test_node_as_dict = ConverterLayer.from_AIDM_converter.convert_to_json_conform_dict(test_train_path_node)
        test_node_as_json = json.dumps(test_node_as_dict)

        expected_json_string = ('{"ArrivalTime": "0001-05-01T01:01:00", "DepartureTime": "0001-05-01T01:01:00",' +
                                ' "FormationID": 1187, "ID": 11038, "MinimumRunTime": null, "MinimumStopTime": "P0D",' +
                                ' "NodeID": 18, "NodeTrackID": null, "SectionTrackID": null, "SequenceNumber": 0,' +
                                ' "StopStatus": "passing"}')
        self.assertEqual(test_node_as_json, expected_json_string)

    def test_convert_to_list_of_dict_emtpy(self):
        test_list_of_dict = []

        test_section_list = ConverterLayer.from_AIDM_converter.convert_to_list_of_dict(test_list_of_dict)

        self.assertIsInstance(test_section_list, list)
        self.assertListEqual(test_section_list, [])

    def test_convert_to_list_of_dict(self):
        algorithm_section_track = AIDM_classes.AlgorithmSectionTrack(ID=12, Code='ATest', DebugString='str', Weight=8,
                                                                     SectionCode='TestSection')
        test_list_of_algorithm_section_track = [algorithm_section_track, algorithm_section_track,
                                                algorithm_section_track]

        test_section_list_of_dict = ConverterLayer.from_AIDM_converter.convert_to_list_of_dict(
            test_list_of_algorithm_section_track)

        self.assertIsInstance(test_section_list_of_dict, list)
        self.assertIsInstance(test_section_list_of_dict[0], dict)
        self.assertEqual(test_section_list_of_dict[0]['DebugString'], 'str')
