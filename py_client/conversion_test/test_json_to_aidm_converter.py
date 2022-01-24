from __future__ import annotations
import unittest

from py_client.conversion.json_to_aidm_converter import JsonToAidmConverter
from py_client.aidm import AlgorithmSectionTrack, AlgorithmFormation, AlgorithmNode, AlgorithmNodeTrack, StopStatus, AlgorithmTrainPathNode
from py_client.aidm.aidm_base_classes import _HasID, _HasCode, _HasDebugString
from py_client.communication.response_processing import AlgorithmPlatformConversionError
from typing import Optional, List
from enum import Enum
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

    def test_json_to_aidm_containing_datetime_not_optional_with_none(self):
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
            arrivalTime = None
        )
        with self.assertRaises(AlgorithmPlatformConversionError) as raised_exception:
            self.__converter.process_json_to_aidm(json_dict, AidmContainingDatetimeTest)
        self.assertEqual(
            "The AIDM class got a None value for a non-optional field",
            raised_exception.exception.message
        )

    def test_json_to_aidm_containing_optional_datetime(self):
        class AidmContainingDatetimeTest(_HasID):
            __arrival_time:  Optional[datetime.datetime]
            def __init__(self, id: int, arrival_time:  Optional[datetime.datetime]):
                _HasID.__init__(self, id)
                self.__arrival_time = arrival_time

            @property
            def arrival_time(self) -> Optional[datetime.datetime]:
                return self.__arrival_time

        json_dict = dict(
            id=54,
            arrivalTime = "2003-05-01T00:05:00"
        )

        aidm = self.__converter.process_json_to_aidm(json_dict, AidmContainingDatetimeTest)
        self.assertIsInstance(aidm, AidmContainingDatetimeTest)
        self.assertIn(type(aidm.arrival_time), [type(None), datetime.datetime])
        self.assertEqual(aidm.arrival_time, datetime.datetime(2003, 5, 1, hour=0, minute=5, second=0))

    def test_json_to_aidm_containing_optional_with_none_datetime(self):
        class AidmContainingDatetimeTest(_HasID):
            __arrival_time:  Optional[datetime.datetime]
            def __init__(self, id: int, arrival_time:  Optional[datetime.datetime]):
                _HasID.__init__(self, id)
                self.__arrival_time = arrival_time

            @property
            def arrival_time(self) -> Optional[datetime.datetime]:
                return self.__arrival_time

        json_dict = dict(
            id=54,
            arrivalTime = None
        )

        aidm = self.__converter.process_json_to_aidm(json_dict, AidmContainingDatetimeTest)
        self.assertIsInstance(aidm, AidmContainingDatetimeTest)
        self.assertIn(type(aidm.arrival_time), [type(None), datetime.datetime])
        self.assertEqual(aidm.arrival_time, None)

    def test_json_to_aidm_containing_datetime_with_wrong_datetime_format(self):
        class AidmContainingDatetimeTest(_HasID):
            __arrival_time: datetime.datetime

            def __init__(self, id: int, arrival_time: datetime.datetime):
                _HasID.__init__(self, id)
                self.__arrival_time = arrival_time

            @property
            def arrival_time(self) -> datetime.datetime:
                return self.__arrival_time

        json_dict = dict(
            id=54,
            arrivalTime="2003-05-01TZR00:05:00"
        )

        with self.assertRaises(AlgorithmPlatformConversionError) as conversion_error:
            self.__converter.process_json_to_aidm(json_dict, AidmContainingDatetimeTest)
        self.assertEqual(
            conversion_error.exception.message,
            "Could not parse datetime, invalid datetime format: {}".format(json_dict['arrivalTime']))

    def test_json_to_aidm_containing_timedelta(self):
        class AidmContainingTimedeltaTest(_HasID):
            __minimum_stop_time: datetime.timedelta

            def __init__(self, id: int, minimum_stop_time: datetime.datetime):
                _HasID.__init__(self, id)
                self.__minimum_stop_time = minimum_stop_time

            @property
            def minimum_stop_time(self) -> datetime.timedelta:
                return self.__minimum_stop_time

        json_dict = dict(
            id=54,
            minimumStopTime="PT6M"
        )

        aidm = self.__converter.process_json_to_aidm(json_dict, AidmContainingTimedeltaTest)
        self.assertIsInstance(aidm, AidmContainingTimedeltaTest)
        self.assertIsInstance(aidm.minimum_stop_time, datetime.timedelta)
        self.assertEqual(aidm.minimum_stop_time, datetime.timedelta(minutes=6))

    def test_json_to_aidm_containing_non_optional_timedelta_with_none_value(self):
        class AidmContainingTimedeltaTest(_HasID):
            __minimum_stop_time: datetime.timedelta

            def __init__(self, id: int, minimum_stop_time: datetime.datetime):
                _HasID.__init__(self, id)
                self.__minimum_stop_time = minimum_stop_time

            @property
            def minimum_stop_time(self) -> datetime.timedelta:
                return self.__minimum_stop_time

        json_dict = dict(
            id=54,
            minimumStopTime=None
        )

        with self.assertRaises(AlgorithmPlatformConversionError) as raised_exception:
            self.__converter.process_json_to_aidm(json_dict, AidmContainingTimedeltaTest)
        self.assertEqual(
            "The AIDM class got a None value for a non-optional field",
            raised_exception.exception.message
        )

    def test_json_to_aidm_containing_optional_timedelta(self):
        class AidmContainingTimedeltaTest(_HasID):
            __minimum_stop_time: Optional[datetime.timedelta]

            def __init__(self, id: int, minimum_stop_time: Optional[datetime.datetime]):
                _HasID.__init__(self, id)
                self.__minimum_stop_time = minimum_stop_time

            @property
            def minimum_stop_time(self) -> Optional[datetime.timedelta]:
                return self.__minimum_stop_time

        json_dict = dict(
            id=54,
            minimumStopTime="PT6M"
        )

        aidm = self.__converter.process_json_to_aidm(json_dict, AidmContainingTimedeltaTest)
        self.assertIsInstance(aidm, AidmContainingTimedeltaTest)
        self.assertIn(type(aidm.minimum_stop_time), [type(None), datetime.timedelta])
        self.assertEqual(aidm.minimum_stop_time, datetime.timedelta(minutes=6))

    def test_json_to_aidm_containing_optional_timedelta_with_non_value(self):
        class AidmContainingTimedeltaTest(_HasID):
            __minimum_stop_time: Optional[datetime.timedelta]

            def __init__(self, id: int, minimum_stop_time: Optional[datetime.timedelta]):
                _HasID.__init__(self, id)
                self.__minimum_stop_time = minimum_stop_time

            @property
            def minimum_stop_time(self) -> Optional[datetime.timedelta]:
                return self.__minimum_stop_time

        json_dict = dict(
            id=54,
            minimumStopTime=None
        )

        aidm = self.__converter.process_json_to_aidm(json_dict, AidmContainingTimedeltaTest)
        self.assertIsInstance(aidm, AidmContainingTimedeltaTest)
        self.assertIn(type(aidm.minimum_stop_time), [type(None), datetime.timedelta])
        self.assertEqual(aidm.minimum_stop_time, None)

    def test_json_to_aidm_containing_timedelta_with_conversion_error(self):
        class AidmContainingTimedeltaTest(_HasID):
            __minimum_stop_time: datetime.timedelta

            def __init__(self, id: int, minimum_stop_time: datetime.timedelta):
                _HasID.__init__(self, id)
                self.__minimum_stop_time = minimum_stop_time

            @property
            def minimum_stop_time(self) -> datetime.timedelta:
                return self.__minimum_stop_time

        json_dict = dict(
            id=54,
            minimumStopTime="PT6Z"
        )
        with self.assertRaises(AlgorithmPlatformConversionError) as conversion_error:
            self.__converter.process_json_to_aidm(json_dict, AidmContainingTimedeltaTest)
        self.assertEqual(conversion_error.exception.message, "Could not parse duration, invalid duration format: {}".format(json_dict['minimumStopTime']))

    def test_json_to_aidm_containing_optional(self):
        class AidmContainingOptionalTest(_HasID):
            __optional_field: Optional[str]

            def __init__(self, id: int, optional_field: Optional[str]):
                _HasID.__init__(self, id)
                self.__optional_field = optional_field

            @property
            def optional_field(self) -> Optional[str]:
                return self.__optional_field
        json_dict = dict(
            id=1223,
            optionalField="non empty"
        )

        test_optional = self.__converter.process_json_to_aidm(json_dict, AidmContainingOptionalTest)

        self.assertIsInstance(test_optional, AidmContainingOptionalTest)
        self.assertIn(type(test_optional.optional_field), [type(None), str])
        self.assertEqual(test_optional.optional_field, "non empty")

    def test_json_to_aidm_containing_optional_with_none_value(self):
        class AidmContainingOptionalTest(_HasID):
            __optional_field: Optional[str]

            def __init__(self, id: int, optional_field: Optional[str]):
                _HasID.__init__(self, id)
                self.__optional_field = optional_field

            @property
            def optional_field(self) -> Optional[str]:
                return self.__optional_field
        json_dict = dict(
            id=1223,
            optionalField=None
        )

        test_optional = self.__converter.process_json_to_aidm(json_dict, AidmContainingOptionalTest)

        self.assertIsInstance(test_optional, AidmContainingOptionalTest)
        self.assertIn(type(test_optional.optional_field), [type(None), str])
        self.assertEqual(test_optional.optional_field, None)

    def test_json_to_aidm_containing_not_optional_with_none_value(self):
        class AidmContainingNotOptionalTest(_HasID):
            __optional_field: str

            def __init__(self, id: int, optional_field: str):
                _HasID.__init__(self, id)
                self.__optional_field = optional_field

            @property
            def optional_field(self) -> str:
                return self.__optional_field
        json_dict = dict(
            id=1223,
            optionalField=None
        )

        with self.assertRaises(AlgorithmPlatformConversionError) as raised_exception:
            self.__converter.process_json_to_aidm(json_dict, AidmContainingNotOptionalTest)
        self.assertEqual(
            "The AIDM class got a None value for a non-optional field",
            raised_exception.exception.message
        )

    def test_json_to_aidm_containing_enum(self):
        class AidmContainingEnumTest(_HasID):
            __enum_field: StopStatus

            def __init__(self, id: int, enum_field: string):
                _HasID.__init__(self, id)
                self.__enum_field = enum_field

            @property
            def enum_field(self) -> StopStatus:
                return self.__enum_field
        json_dict = dict(
            id=1223,
            enumField="commercialStop"
        )

        test_enum = self.__converter.process_json_to_aidm(json_dict, AidmContainingEnumTest)
        self.assertIsInstance(test_enum, AidmContainingEnumTest)
        self.assertIsInstance(test_enum.enum_field, StopStatus)
        self.assertEqual(test_enum.enum_field, StopStatus.commercial_stop)

    def test_json_to_aidm_containing_enum_conversion_error(self):
        class AidmContainingEnumTest(_HasID):
            __enum_field: StopStatus

            def __init__(self, id: int, enum_field: string):
                _HasID.__init__(self, id)
                self.__enum_field = enum_field

            @property
            def enum_field(self) -> StopStatus:
                return self.__enum_field
        json_dict = dict(
            id=1223,
            enumField="nonStopStatusValue"
        )

        with self.assertRaises(AlgorithmPlatformConversionError) as conversion_error:
            self.__converter.process_json_to_aidm(json_dict, AidmContainingEnumTest)
        self.assertEqual(conversion_error.exception.message, "Could not parse Enum {}, invalid enum format for expected class Enum {}".format(json_dict['enumField'], StopStatus))

    def test_json_to_aimd_containing_datetime_timedelta_and_enum(self):
        json_dict = dict(
            id=4287,
            sectionTrackId=None,
            nodeId=18,
            nodeTrackId=None,
            formationId=4142,
            movementTypeId=2222,
            arrivalTime="2003-05-01T00:05:00",
            departureTime="2003-05-01T00:05:00",
            minimumRunTime="P3D",
            minimumStopTime="P5D",
            stopStatus="commercialStop",
            sequenceNumber=0
        )

        algorithm_train_path_node = self.__converter.process_json_to_aidm(json_dict, AlgorithmTrainPathNode)

        self.assertEqual(algorithm_train_path_node.id, 4287)

        self.assertIn(type(algorithm_train_path_node.section_track_id), [int, type(None)])
        self.assertEqual(algorithm_train_path_node.section_track_id, None)

        self.assertEqual(algorithm_train_path_node.node_id, 18)

        self.assertIn(type(algorithm_train_path_node.node_track_id), [int, type(None)])
        self.assertEqual(algorithm_train_path_node.node_track_id, None)

        self.assertEqual(algorithm_train_path_node.formation_id, 4142)
        self.assertEqual(algorithm_train_path_node.movement_type_id, 2222)

        self.assertIsInstance(algorithm_train_path_node.arrival_time, datetime.datetime)
        self.assertEqual(algorithm_train_path_node.arrival_time, datetime.datetime(year=2003, month=5, day= 1, hour=0, minute=5))

        self.assertIsInstance(algorithm_train_path_node.departure_time, datetime.datetime)
        self.assertEqual(algorithm_train_path_node.departure_time, datetime.datetime(year=2003, month=5, day=1, hour=0, minute=5))

        self.assertIsInstance(algorithm_train_path_node.minimum_run_time, datetime.timedelta)
        self.assertEqual(algorithm_train_path_node.minimum_run_time, datetime.timedelta(days=3))

        self.assertIsInstance(algorithm_train_path_node.minimum_stop_time, datetime.timedelta)
        self.assertEqual(algorithm_train_path_node.minimum_stop_time, datetime.timedelta(days=5))

        self.assertIsInstance(algorithm_train_path_node.stop_status, StopStatus)
        self.assertEqual(algorithm_train_path_node.stop_status, StopStatus.commercial_stop)

        self.assertEqual(algorithm_train_path_node.sequence_number, 0)


    def test_unsupported_non_primitive_type(self):
        json_dict = dict(someProperty = dict(someProperty = None))

        with self.assertRaises(AlgorithmPlatformConversionError):
            self.__converter.process_json_to_aidm(json_dict, SomeClass)

class SomeClass:
    __some_property: SomeClass

    def __init__(self, __some_property: SomeClass):
        self.__some_property = __some_property
