from __future__ import annotations
import unittest

from py_client.conversion.json_to_aidm_converter import JsonToAidmConverter
from py_client.aidm import AlgorithmSectionTrack, AlgorithmFormation
from py_client.aidm.aidm_base_classes import _HasID, _HasCode, _HasDebugString
from py_client.communication.response_processing import AlgorithmPlatformConversionError

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


    def test_unsupported_non_primitive_type(self):
        json_dict = dict(someProperty = dict(someProperty = None))

        with self.assertRaises(AlgorithmPlatformConversionError):
            self.__converter.process_json_to_aidm(json_dict, SomeClass)

class SomeClass:
    __some_property: SomeClass

    def __init__(self, __some_property: SomeClass):
        self.__some_property = __some_property
