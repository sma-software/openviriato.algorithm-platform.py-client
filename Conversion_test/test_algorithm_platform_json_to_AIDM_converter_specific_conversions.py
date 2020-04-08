import datetime
import unittest

import AIDMClasses
from Conversion import algorithm_platform_json_to_AIDM_converter


class TestToAIDMConverterSpecificConversions(unittest.TestCase):

    def test_convert_json_to_AlgorithmNode(self):
        test_node_as_dict = dict(ID=15, Code='A', DebugString='test123', NodeTracks=[])

        test_node = algorithm_platform_json_to_AIDM_converter.convert_json_to_AlgorithmNode(test_node_as_dict)

        self.assertIsInstance(test_node, AIDMClasses.AlgorithmNode)
        self.assertEqual(test_node.ID, 15)
        self.assertEqual(test_node.Code, 'A')
        self.assertEqual(test_node.DebugString, 'test123')
        self.assertEqual(test_node.NodeTracks, [])

    def test_convert_list_of_json_to_AlgorithmNode(self):
        test_node_as_dict = dict(ID=15, Code='A', DebugString='test123', NodeTracks=[])
        test_node_as_list_of_dict = [test_node_as_dict, test_node_as_dict, test_node_as_dict, test_node_as_dict]

        test_node_list = algorithm_platform_json_to_AIDM_converter.convert_list(
            algorithm_platform_json_to_AIDM_converter.convert_json_to_AlgorithmNode, test_node_as_list_of_dict)

        self.assertIsInstance(test_node_list, list)
        self.assertIsInstance(test_node_list[1], AIDMClasses.AlgorithmNode)
        self.assertEqual(test_node_list[1].ID, 15)

    def test_convert_json_to_TrainPathNode(self):
        test_node_as_dict = dict(ID=1332, SectionTrackID=None, NodeID=18, NodeTrackID=None, FormationID=1187,
                                 ArrivalTime="2003-05-01T00:04:00", DepartureTime="2003-05-01T00:05:00",
                                 MinimumRunTime=None, MinimumStopTime="P0D", StopStatus="commercialStop",
                                 SequenceNumber=0)

        test_train_path_node = algorithm_platform_json_to_AIDM_converter.convert_json_to_TrainPathNode(
            test_node_as_dict)

        self.assertIsInstance(test_train_path_node, AIDMClasses.TrainPathNode)
        self.assertEqual(test_train_path_node.ID, 1332)
        self.assertEqual(test_train_path_node.MinimumRunTime, None)
        self.assertEqual(test_train_path_node.MinimumStopTime, datetime.timedelta(0))

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
        self.assertIsInstance(test_train.TrainPathNodes[0], AIDMClasses.TrainPathNode)
        self.assertEqual(test_train.TrainPathNodes[0].MinimumRunTime, None)
        self.assertEqual(test_train.TrainPathNodes[0].MinimumStopTime, datetime.timedelta(0))

    def test_convert_json_to_TimeWindow(self):
        test_time_window_as_dict = dict(FromTime="2003-05-01T08:00:00", ToTime="2023-05-02T10:00:50")

        test_time_window = algorithm_platform_json_to_AIDM_converter.convert_json_to_TimeWindow(
            test_time_window_as_dict)

        self.assertIsInstance(test_time_window, AIDMClasses.TimeWindow)
        self.assertIsInstance(test_time_window.FromTime, datetime.datetime)
        self.assertEqual(test_time_window.FromTime, datetime.datetime(year=2003, month=5, day=1, hour=8, minute=0))
        self.assertIsInstance(test_time_window.ToTime, datetime.datetime)
        self.assertEqual(test_time_window.ToTime, datetime.datetime(year=2023, month=5, day=2, hour=10, minute=0,
                                                                    second=50))

    def test_convert_json_to_AlgorithmSectionTrackClosure(self):
        param_dict = dict(DebugString="sectiontrackclosure:s_70011 1 n_85ZMUS 85ZLSTA", SectionTrackID=1080,
                          FromNodeID=621, ToNodeID=620,
                          ClosureTimeWindowFromNode=dict(FromTime="2003-05-01T08:00:00", ToTime="2003-05-01T09:00:00"),
                          ClosureTimeWindowToNode=dict(FromTime="2003-05-01T08:30:00", ToTime="2003-05-01T09:30:00"))

        test_closure = algorithm_platform_json_to_AIDM_converter.convert_json_to_AlgorithmSectionTrackClosure(
            param_dict)

        self.assertIsInstance(test_closure, AIDMClasses.AlgorithmSectionTrackClosure)
        self.assertIsInstance(test_closure.ClosureTimeWindowFromNode, AIDMClasses.TimeWindow)
        self.assertEqual(test_closure.FromNodeID, 621)

    def test_convert_json_to_AlgorithmNodeTrackClosure(self):
        param_dict = dict(DebugString="nodetrackclosure:85ZMUS 24", NodeID=621, NodeTrackID=622,
                          ClosureTimeWindow=dict(FromTime="2003-05-01T08:00:00", ToTime="2003-05-02T10:00:00"))

        test_closure = algorithm_platform_json_to_AIDM_converter.convert_json_to_AlgorithmNodeTrackClosure(param_dict)

        self.assertIsInstance(test_closure, AIDMClasses.AlgorithmNodeTrackClosure)
        self.assertIsInstance(test_closure.ClosureTimeWindow, AIDMClasses.TimeWindow)
        self.assertEqual(test_closure.DebugString, "nodetrackclosure:85ZMUS 24")

    @unittest.skip('VPLAT-7405:')
    def test_convert_json_to_incoming_routing_edge_set(self):
        raise NotImplementedError

    @unittest.skip('VPLAT-7405:')
    def test_convert_json_to_outgoing_routing_edge_set(self):
        raise NotImplementedError

    @unittest.skip('VPLAT-7405:')
    def test_convert_json_to_crossing_routing_edge_set(self):
        raise NotImplementedError

    def test_convert_json_to_UpdateTrainTimes(self):
        param_dict = dict(TrainID=1012, Times= \
            [dict(TrainPathNodeID=3880, ArrivalTime="2003-05-01T07:00:00", DepartureTime="2003-05-01T07:00:00",
                  MinimumRunTime=None, MinimumStopTime="P0D", StopStatus="commercialStop"),
             dict(TrainPathNodeID=4246, ArrivalTime="2003-05-01T07:01:42", DepartureTime="2003-05-01T07:01:42",
                  MinimumRunTime="PT1M42S", MinimumStopTime="P0D", StopStatus="passing")])

        test_update_train_times = algorithm_platform_json_to_AIDM_converter.convert_json_to_UpdateTrainTimes(
            param_dict)

        self.assertIsInstance(test_update_train_times, AIDMClasses.UpdateTrainTimes)
        self.assertEqual(test_update_train_times.TrainID, 1012)
        self.assertIsInstance(test_update_train_times.Times[0], AIDMClasses.UpdateTrainTimesNode)
        self.assertEqual(test_update_train_times.Times[0].TrainPathNodeID, 3880)
        self.assertEqual(test_update_train_times.Times[0].ArrivalTime,
                         datetime.datetime(year=2003, month=5, day=1, hour=7, minute=0))

    def test_convert_json_to_update_train_times_node(self):
        param_dict = dict(TrainPathNodeID=3880, ArrivalTime="2003-05-01T07:00:00", DepartureTime="2003-05-01T07:00:00",
                          MinimumRunTime=None, MinimumStopTime="P0D", StopStatus="commercialStop")

        test_update_train_times_node = algorithm_platform_json_to_AIDM_converter.convert_json_to_UpdateTrainTimesNode(
            param_dict)

        self.assertIsInstance(test_update_train_times_node, AIDMClasses.UpdateTrainTimesNode)
        self.assertEqual(test_update_train_times_node.TrainPathNodeID, 3880)
        self.assertEqual(test_update_train_times_node.ArrivalTime,
                         datetime.datetime(year=2003, month=5, day=1, hour=7, minute=0))
        self.assertEqual(test_update_train_times_node.MinimumRunTime, None)
        self.assertEqual(test_update_train_times_node.MinimumStopTime, datetime.timedelta(0))
        self.assertEqual(test_update_train_times_node.StopStatus, AIDMClasses.StopStatus["commercialStop"])
