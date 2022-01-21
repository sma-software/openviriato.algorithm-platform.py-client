from __future__ import annotations
import unittest

from py_client.conversion.json_to_aidm_converter import JsonToAidmConverter
from py_client.aidm import AlgorithmSectionTrack, AlgorithmFormation, AlgorithmNode, AlgorithmNodeTrack
from py_client.aidm.aidm_base_classes import _HasID, _HasCode, _HasDebugString
from py_client.communication.response_processing import AlgorithmPlatformConversionError
from typing import List
import datetime

class TestJsonToAIDMConverter(unittest.TestCase):
    __converter: JsonToAidmConverter

    def setUp(self):
        self.__converter = JsonToAidmConverter()


    def test_json_to_section_track(self):
        json_dict = dict(
            id = 1082,
            code ="900",
            sectionCode = "70015",
            distanceUnits = 10000,
            debugString = "sectiontrack:s_70015 n_85ZHDB 900")

        test_section_track = self.__converter.process_json_to_aidm(json_dict, AlgorithmSectionTrack)

        self.assertIsInstance(test_section_track, AlgorithmSectionTrack)
        self.assertEqual(test_section_track.id, 1082)
        self.assertEqual(test_section_track.debug_string, "sectiontrack:s_70015 n_85ZHDB 900")
        self.assertEqual(test_section_track.section_code, "70015")
        self.assertEqual(test_section_track.code, "900")
        self.assertEqual(test_section_track.distance_units, 10000)

    def test_json_to_section_track_attribute_missing(self):
        json_dict = dict(
            id=1082,
            code="900",
            sectionCode="70015",
           debugString="sectiontrack:s_70015 n_85ZHDB 900")

        with self.assertRaises(AlgorithmPlatformConversionError):
            self.__converter.process_json_to_aidm(json_dict, AlgorithmSectionTrack)

    def test_json_to_section_track_extra_attribute(self):
        json_dict = dict(
            extraAttribute="i don't belong here for a section track",
            id=1082,
            code="900",
            sectionCode="70015",
            distanceUnits=10000,
            debugString="sectiontrack:s_70015 n_85ZHDB 900")

        with self.assertRaises(AlgorithmPlatformConversionError):
            self.__converter.process_json_to_aidm(json_dict, AlgorithmSectionTrack)

    def test_json_to_aidm_containing_list_of_primitives(self):
        json_dict = dict(
            id=1223,
            vehicleTypeIds=[689],
            placesFirstClass=125,
            placesSecondClass=326,
            debugString="train configuration:  seats 125 326"
        )

        test_formation = self.__converter.process_json_to_aidm(json_dict, AlgorithmFormation)

        self.assertIsInstance(test_formation, AlgorithmFormation)
        self.assertIsInstance(test_formation.vehicle_type_ids, list)
        self.assertEqual(test_formation.vehicle_type_ids[0], 689)

    def test_json_to_aidm_containing_list_of_aidm(self):
        json_dict = dict(
            id = 162,
            code = "85AR",
            nodeTracks = [
                dict(id = 163,
                     code = "1",
                     debugString = "stationtrack:85AR_{StationTrack SID = 34138}"
                     ),
                dict(
                    id = 164,
                    code = "2",
                    debugString = "stationtrack:85AR_{StationTrack SID = 34140}"
                )
            ],
            debugString = "station:85AR"
        )

        algorithm_node = self.__converter.process_json_to_aidm(json_dict, AlgorithmNode)
        self.assertIsInstance(algorithm_node, AlgorithmNode)
        self.assertIsInstance(algorithm_node.node_tracks, List)
        self.assertEqual(len(algorithm_node.node_tracks), 2)
        self.assertIsInstance(algorithm_node.node_tracks[0], AlgorithmNodeTrack)

    def test_json_to_aidm_containing_empty_list_of_aidm(self):
        json_dict = dict(
            id = 162,
            code = "85AR",
            nodeTracks = [],
            debugString = "station:85AR"
        )

        algorithm_node = self.__converter.process_json_to_aidm(json_dict, AlgorithmNode)
        self.assertIsInstance(algorithm_node, AlgorithmNode)
        self.assertIsInstance(algorithm_node.node_tracks, List)
        self.assertEqual(len(algorithm_node.node_tracks), 0)

    def test_json_to_list_of_aidm(self):
        json_dict = [
            dict(id = 1,
                 code = "45ADW",
                 nodeTracks = [],
                 debugString= "station:45ADW"
                 ),
            dict(id = 2,
                 code = "45LNG",
                 nodeTracks = [],
                 debugString = "station:45LNG"
                 ),
            dict(
                id = 3,
                code = "45SIA",
                nodeTracks = [],
                debugString ="station:45SIA"
            )
        ]

        algorithm_nodes = self.__converter.process_json_to_aidm(json_dict, List[AlgorithmNode])
        self.assertIsInstance(algorithm_nodes, list)
        self.assertEqual(len(algorithm_nodes), 3)
        self.assertIsInstance(algorithm_nodes[0], AlgorithmNode)

    def test_json_to_empty_list_of_aidm(self):
        json_dict = []

        algorithm_nodes = self.__converter.process_json_to_aidm(json_dict, List[AlgorithmNode])
        self.assertIsInstance(algorithm_nodes, List)
        self.assertEqual(len(algorithm_nodes), 0)

    def test_json_to_aidm_containing_datetime(self):
        class AidmContainingDatetimeTest(_HasID):
            __arrival_time:  datetime.datetime
            def __init__(self, id: int, arrival_time:  datetime.datetime):
                _HasID.__init__(self, id)
                self.__arrival_time = arrival_time

            @property
            def arrival_time(self) -> datetime.datetime:
                return self.__arrival_time

        json_dict = dict(
            id=54,
            arrivalTime = "2003-05-01T00:05:00"
        )

        aidm = self.__converter.process_json_to_aidm(json_dict, AidmContainingDatetimeTest)
        self.assertIsInstance(aidm, AidmContainingDatetimeTest)
        self.assertIsInstance(aidm.arrival_time, datetime.datetime)
        self.assertEqual(aidm.arrival_time, datetime.datetime(2003, 5, 1, hour=0, minute=5, second=0))

    def test_unsupported_non_primitive_type(self):
        json_dict = dict(someProperty = dict(someProperty = None))

        with self.assertRaises(AlgorithmPlatformConversionError):
            self.__converter.process_json_to_aidm(json_dict, SomeClass)

class SomeClass:
    __some_property: SomeClass

    def __init__(self, __some_property: SomeClass):
        self.__some_property = __some_property
