import datetime
import unittest

import AIDMClasses
from Conversion import algorithm_platform_json_to_AIDM_converter


class TestToAIDMConverter(unittest.TestCase):

    def test_convert_json_to_AIDM_Class_from_constructor(self):
        test_section_as_dict = dict(ID=12, Code='ATest', DebugString='str', Weight=8, SectionCode='TestSection')

        test_section = algorithm_platform_json_to_AIDM_converter.convert(
            AIDMClasses.AlgorithmSectionTrack, test_section_as_dict)

        self.assertIsInstance(test_section, AIDMClasses.AlgorithmSectionTrack)
        self.assertEqual(test_section.id, 12)
        self.assertEqual(test_section.code, 'ATest')
        self.assertEqual(test_section.debug_string, 'str')
        self.assertEqual(test_section.weight, 8)
        self.assertEqual(test_section.section_code, 'TestSection')

    def test_convert_json_to_AIDM_Class_populated_from_factory_method(self):
        test_class_inner_object = TestClassInner(id=99)
        test_class_outer_object = TestClassOuter(id=200, inner=test_class_inner_object)

        outer_test_object = dict(id=200, inner=dict(id=99))

        result = algorithm_platform_json_to_AIDM_converter.convert(convert_test_class_outer, outer_test_object)

        self.assertIsInstance(result, TestClassOuter)
        self.assertEqual(test_class_outer_object.id, result.id)
        self.assertIsInstance(result.inner, TestClassInner)
        self.assertEqual(test_class_outer_object.inner.id, result.inner.id)

    def test_convert_list_of_dict_to_list_of_AIDM(self):
        test_section_as_dict = dict(ID=12, Code='ATest', DebugString='str', Weight=8, SectionCode='TestSection')
        test_section_dict_in_list = [test_section_as_dict, test_section_as_dict, test_section_as_dict]

        test_section_list = algorithm_platform_json_to_AIDM_converter.convert_list(AIDMClasses.AlgorithmSectionTrack,
                                                                                   test_section_dict_in_list)

        self.assertIsInstance(test_section_list, list)
        self.assertIsInstance(test_section_list[0], AIDMClasses.AlgorithmSectionTrack)
        self.assertEqual(test_section_list[0].debug_string, 'str')

    def test_convert_json_to_AlgorithmNode(self):
        test_node_tracks_as_list = [
            dict(ID=162, Code="1", DebugString="AString"),
            dict(ID=123, Code="2", DebugString='AnotherDebugString')]
        test_node_as_dict = dict(ID=15, Code='A', DebugString='test123', NodeTracks=test_node_tracks_as_list)

        test_node = algorithm_platform_json_to_AIDM_converter.convert_json_to_AlgorithmNode(test_node_as_dict)

        self.assertIsInstance(test_node, AIDMClasses.AlgorithmNode)
        self.assertEqual(test_node.id, 15)
        self.assertEqual(test_node.code, 'A')
        self.assertEqual(test_node.debug_string, 'test123')
        self.assertIsInstance(test_node.node_tracks, list)
        self.assertEqual(test_node.node_tracks[0].id, 162)
        self.assertEqual(test_node.node_tracks[0].code, "1")
        self.assertEqual(test_node.node_tracks[0].debug_string, "AString")

    def test_convert_json_to_AlgorithmNode_without_node_tracks(self):
        test_node_tracks_as_list = []
        test_node_as_dict = dict(ID=15, Code='A', DebugString='test123', NodeTracks=test_node_tracks_as_list)

        test_node = algorithm_platform_json_to_AIDM_converter.convert_json_to_AlgorithmNode(test_node_as_dict)

        self.assertIsInstance(test_node, AIDMClasses.AlgorithmNode)
        self.assertEqual(test_node.id, 15)
        self.assertEqual(test_node.code, 'A')
        self.assertEqual(test_node.debug_string, 'test123')
        self.assertIsInstance(test_node.node_tracks, list)
        self.assertListEqual(test_node.node_tracks, [])

    def test_convert_list_of_json_to_AlgorithmNode(self):
        test_node_tracks_as_list = [
            dict(ID=162, Code="1", DebugString="AString"),
            dict(ID=123, Code="2", DebugString='AnotherDebugString')]
        test_node_as_dict = dict(ID=15, Code='A', DebugString='test123', NodeTracks=test_node_tracks_as_list)
        test_node_as_list_of_dict = [test_node_as_dict, test_node_as_dict.copy(), test_node_as_dict.copy()]

        test_node_list = algorithm_platform_json_to_AIDM_converter.convert_list(
            algorithm_platform_json_to_AIDM_converter.convert_json_to_AlgorithmNode,
            test_node_as_list_of_dict)

        self.assertIsInstance(test_node_list, list)
        self.assertIsInstance(test_node_list[0], AIDMClasses.AlgorithmNode)
        self.assertEqual(test_node_list[0].id, 15)
        self.assertEqual(test_node_list[0].node_tracks[0].id, 162)
        self.assertEqual(test_node_list[0].node_tracks[0].code, "1")
        self.assertEqual(test_node_list[0].node_tracks[0].debug_string, "AString")

    def test_convert_camel_case_json_to_TrainPathNode(self):
        test_node_as_dict = dict(ID=1332, sectionTrackID=None, nodeID=18, nodeTrackID=None, formationID=1187,
                                 arrivalTime="2003-05-01T00:04:00", departureTime="2003-05-01T00:05:00",
                                 minimumRunTime=None, minimumStopTime="P0D", stopStatus="commercialStop",
                                 sequenceNumber=0)

        test_train_path_node = algorithm_platform_json_to_AIDM_converter.convert_json_to_AlgorithmTrainPathNode(
            test_node_as_dict)

        self.assertIsInstance(test_train_path_node, AIDMClasses.AlgorithmTrainPathNode)
        self.assertEqual(test_train_path_node.id, 1332)
        self.assertEqual(test_train_path_node.minimum_run_time, None)
        self.assertEqual(test_train_path_node.minimum_stop_time, datetime.timedelta(0))

    def test_convert_pascal_case_json_to_TrainPathNode(self):
        test_node_as_dict = dict(ID=1332, SectionTrackID=None, NodeID=18, NodeTrackID=None, FormationID=1187,
                                 ArrivalTime="2003-05-01T00:04:00", DepartureTime="2003-05-01T00:05:00",
                                 MinimumRunTime=None, MinimumStopTime="P0D", StopStatus="CommercialStop",
                                 SequenceNumber=0)

        test_train_path_node = algorithm_platform_json_to_AIDM_converter.convert_json_to_AlgorithmTrainPathNode(
            test_node_as_dict)

        self.assertIsInstance(test_train_path_node, AIDMClasses.AlgorithmTrainPathNode)
        self.assertEqual(test_train_path_node.id, 1332)
        self.assertEqual(test_train_path_node.minimum_run_time, None)
        self.assertEqual(test_train_path_node.minimum_stop_time, datetime.timedelta(0))

    def test_convert_json_to_AlgorithmTrain(self):
        test_train_as_dict = dict(ID=3516, TrainPathNodes=[
            dict(ID=2424, SectionTrackID=None, NodeID=7, NodeTrackID=8, FormationID=1187,
                 ArrivalTime="2003-05-01T00:10:00", DepartureTime="2003-05-01T00:10:00", MinimumRunTime=None,
                 MinimumStopTime="P0D", StopStatus="commercialStop", SequenceNumber=0),
            dict(ID=11040, SectionTrackID=1165, NodeID=24, NodeTrackID=25, FormationID=1187,
                 ArrivalTime="2003-05-01T00:10:00", DepartureTime="2003-05-01T00:10:00", MinimumRunTime="P0D",
                 MinimumStopTime="P0D", StopStatus="passing", SequenceNumber=1),
            dict(ID=3152, SectionTrackID=1166, NodeID=10, NodeTrackID=12, FormationID=None,
                 ArrivalTime="2003-05-01T00:19:00", DepartureTime="2003-05-01T00:19:00", MinimumRunTime="PT9M",
                 MinimumStopTime="P0D", StopStatus="commercialStop", SequenceNumber=2)
        ], DebugString="RVZH_3_1_J03 tt_(S)")

        test_train = algorithm_platform_json_to_AIDM_converter.convert_json_to_AlgorithmTrain(test_train_as_dict)

        self.assertIsInstance(test_train, AIDMClasses.AlgorithmTrain)
        self.assertIsInstance(test_train.train_path_nodes[0], AIDMClasses.AlgorithmTrainPathNode)
        self.assertEqual(test_train.train_path_nodes[0].minimum_run_time, None)
        self.assertEqual(test_train.train_path_nodes[0].minimum_stop_time, datetime.timedelta(0))

    def test_convert_json_to_TimeWindow(self):
        test_time_window_as_dict = dict(FromTime="2003-05-01T08:00:00", ToTime="2023-05-02T10:00:50")

        test_time_window = algorithm_platform_json_to_AIDM_converter.convert_json_to_TimeWindow(
            test_time_window_as_dict)

        self.assertIsInstance(test_time_window, AIDMClasses.TimeWindow)
        self.assertIsInstance(test_time_window.from_time, datetime.datetime)
        self.assertEqual(test_time_window.from_time, datetime.datetime(year=2003, month=5, day=1, hour=8, minute=0))
        self.assertIsInstance(test_time_window.to_time, datetime.datetime)
        self.assertEqual(test_time_window.to_time, datetime.datetime(year=2023, month=5, day=2, hour=10, minute=0,
                                                                     second=50))

    def test_convert_json_to_AlgorithmSectionTrackClosure(self):
        param_dict = dict(DebugString="sectiontrackclosure:s_70011 1 n_85ZMUS 85ZLSTA", SectionTrackID=1080,
                          FromNodeID=621, ToNodeID=620,
                          ClosureTimeWindowFromNode=dict(FromTime="2003-05-01T08:00:00", ToTime="2003-05-01T09:00:00"),
                          ClosureTimeWindowToNode=dict(FromTime="2003-05-01T08:30:00", ToTime="2003-05-01T09:30:00"))

        test_closure = algorithm_platform_json_to_AIDM_converter.convert_json_to_AlgorithmSectionTrackClosure(
            param_dict)

        self.assertIsInstance(test_closure, AIDMClasses.AlgorithmSectionTrackClosure)
        self.assertIsInstance(test_closure.closure_time_window_from_node, AIDMClasses.TimeWindow)
        self.assertEqual(test_closure.from_node_id, 621)

    def test_convert_json_to_AlgorithmNodeTrackClosure(self):
        param_dict = dict(DebugString="nodetrackclosure:85ZMUS 24", NodeID=621, NodeTrackID=622,
                          ClosureTimeWindow=dict(FromTime="2003-05-01T08:00:00", ToTime="2003-05-02T10:00:00"))

        test_closure = algorithm_platform_json_to_AIDM_converter.convert_json_to_AlgorithmNodeTrackClosure(param_dict)

        self.assertIsInstance(test_closure, AIDMClasses.AlgorithmNodeTrackClosure)
        self.assertIsInstance(test_closure.closure_time_window, AIDMClasses.TimeWindow)
        self.assertEqual(test_closure.debug_string, "nodetrackclosure:85ZMUS 24")

    def test_convert_json_to_incoming_routing_edge_set(self):
        param_dict = dict(IncomingEdges=[
            dict(StartSectionTrackID=887, EndNodeTrackID=888, NodeID=281),
            dict(StartSectionTrackID=888, EndNodeTrackID=887, NodeID=281)])

        test_incoming_routing_edge_set = \
            algorithm_platform_json_to_AIDM_converter.convert_json_to_IncomingRoutingEdgeSet(param_dict)

        self.assertIsInstance(test_incoming_routing_edge_set, AIDMClasses.IncomingRoutingEdgeSet)
        self.assertIsInstance(test_incoming_routing_edge_set.routing_edges[0], AIDMClasses.IncomingRoutingEdge)
        self.assertEqual(test_incoming_routing_edge_set.routing_edges[0].start_section_track_id, 887)
        self.assertEqual(test_incoming_routing_edge_set.routing_edges[0].end_node_track_id, 888)
        self.assertEqual(test_incoming_routing_edge_set.routing_edges[0].node_id, 281)

    def test_convert_json_to_outgoing_routing_edge_set(self):
        param_dict = dict(OutgoingEdges=[
            dict(StartNodeTrackID=887, EndSectionTrackID=888, NodeID=281),
            dict(StartNodeTrackID=888, EndSectionTrackID=887, NodeID=281)])

        test_outgoing_routing_edge_set = \
            algorithm_platform_json_to_AIDM_converter.convert_json_to_OutgoingRoutingEdgeSet(param_dict)

        self.assertIsInstance(test_outgoing_routing_edge_set, AIDMClasses.OutgoingRoutingEdgeSet)
        self.assertIsInstance(test_outgoing_routing_edge_set.routing_edges[0], AIDMClasses.OutgoingRoutingEdge)
        self.assertEqual(test_outgoing_routing_edge_set.routing_edges[0].start_node_track_id, 887)
        self.assertEqual(test_outgoing_routing_edge_set.routing_edges[0].end_section_track_id, 888)
        self.assertEqual(test_outgoing_routing_edge_set.routing_edges[0].node_id, 281)

    def test_convert_json_to_crossing_routing_edge_set(self):
        param_dict = dict(CrossingEdges=[
            dict(StartSectionTrackID=887, EndSectionTrackID=888, NodeID=281),
            dict(StartSectionTrackID=888, EndSectionTrackID=887, NodeID=281)])

        test_crossing_routing_edge_set = \
            algorithm_platform_json_to_AIDM_converter.convert_json_to_CrossingRoutingEdgeSet(param_dict)

        self.assertIsInstance(test_crossing_routing_edge_set, AIDMClasses.CrossingRoutingEdgeSet)
        self.assertIsInstance(test_crossing_routing_edge_set.routing_edges[0], AIDMClasses.CrossingRoutingEdge)
        self.assertEqual(test_crossing_routing_edge_set.routing_edges[0].start_section_track_id, 887)
        self.assertEqual(test_crossing_routing_edge_set.routing_edges[0].end_section_track_id, 888)
        self.assertEqual(test_crossing_routing_edge_set.routing_edges[0].node_id, 281)

    def test_convert_json_to_UpdateTrainTimes(self):
        param_dict = dict(TrainID=1012, Times= \
            [dict(TrainPathNodeID=3880, ArrivalTime="2003-05-01T07:00:00", DepartureTime="2003-05-01T07:00:00",
                  MinimumRunTime=None, MinimumStopTime="P0D", StopStatus="commercialStop"),
             dict(TrainPathNodeID=4246, ArrivalTime="2003-05-01T07:01:42", DepartureTime="2003-05-01T07:01:42",
                  MinimumRunTime="PT1M42S", MinimumStopTime="P0D", StopStatus="passing")])

        test_update_train_times = algorithm_platform_json_to_AIDM_converter.convert_json_to_UpdateTrainTimes(
            param_dict)

        self.assertIsInstance(test_update_train_times, AIDMClasses.UpdateTrainTimes)
        self.assertEqual(test_update_train_times.train_id, 1012)
        self.assertIsInstance(test_update_train_times.times[0], AIDMClasses.UpdateTrainTimesNode)
        self.assertEqual(test_update_train_times.times[0].train_path_node_id, 3880)
        self.assertEqual(test_update_train_times.times[0].arrival_time,
                         datetime.datetime(year=2003, month=5, day=1, hour=7, minute=0))

    def test_convert_json_to_update_train_times_node(self):
        param_dict = dict(TrainPathNodeID=3880, ArrivalTime="2003-05-01T07:00:00", DepartureTime="2003-05-01T07:00:00",
                          MinimumRunTime=None, MinimumStopTime="P0D", StopStatus="CommercialStop")

        test_update_train_times_node = algorithm_platform_json_to_AIDM_converter.convert_json_to_UpdateTrainTimesNode(
            param_dict)

        self.assertIsInstance(test_update_train_times_node, AIDMClasses.UpdateTrainTimesNode)
        self.assertEqual(test_update_train_times_node.train_path_node_id, 3880)
        self.assertEqual(test_update_train_times_node.arrival_time,
                         datetime.datetime(year=2003, month=5, day=1, hour=7, minute=0))
        self.assertEqual(test_update_train_times_node.minimum_run_time, None)
        self.assertEqual(test_update_train_times_node.minimum_stop_time, datetime.timedelta(0))
        self.assertEqual(test_update_train_times_node.stop_status, AIDMClasses.StopStatus.commercial_stop)


class TestClassInner:
    def __init__(self, id: int):
        self.__id = id

    @property
    def id(self):
        return self.__id


class TestClassOuter:
    def __init__(self, inner: TestClassInner, id: int):
        self.__id = id
        self.__inner = inner

    @property
    def id(self):
        return self.__id

    @property
    def inner(self):
        return self.__inner


def convert_test_class_outer(attribute_dict: dict) -> TestClassOuter:
    return TestClassOuter(id=attribute_dict["id"], inner=TestClassInner(**attribute_dict["inner"]))
