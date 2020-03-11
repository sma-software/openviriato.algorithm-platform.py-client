import datetime
import unittest

import ConverterLayer.to_AIDM_converter
from AIDMClasses import AIDM_classes


class TestToAIDMConverterSpecificConversions(unittest.TestCase):

    def test_convert_dict_to_AlgorithmNode(self):
        test_node_as_dict = dict(ID=15, Code='A', DebugString='test123', NodeTracks=[])

        test_node = ConverterLayer.to_AIDM_converter.convert_dict_to_AlgorithmNode(test_node_as_dict)

        self.assertIsInstance(test_node, AIDM_classes.AlgorithmNode)
        self.assertEqual(test_node.ID, 15)
        self.assertEqual(test_node.Code, 'A')
        self.assertEqual(test_node.DebugString, 'test123')
        self.assertEqual(test_node.NodeTracks, [])

    def test_convert_list_of_dict_to_AlgorithmNode(self):
        test_node_as_dict = dict(ID=15, Code='A', DebugString='test123', NodeTracks=[])
        test_node_as_list_of_dict = [test_node_as_dict, test_node_as_dict, test_node_as_dict, test_node_as_dict]

        test_node_list = ConverterLayer.to_AIDM_converter.convert_list_of_dict_to_list_of_AIDM(
            ConverterLayer.to_AIDM_converter.convert_dict_to_AlgorithmNode, test_node_as_list_of_dict)

        self.assertIsInstance(test_node_list, list)
        self.assertIsInstance(test_node_list[1], AIDM_classes.AlgorithmNode)
        self.assertEqual(test_node_list[1].ID, 15)

    def test_convert_dict_to_TrainPathNode(self):
        test_node_as_dict = dict(ID=1332, SectionTrackID=None, NodeID=18, NodeTrackID=None, FormationID=1187,
                                 ArrivalTime="2003-05-01T00:04:00", DepartureTime="2003-05-01T00:05:00",
                                 MinimumRunTime=None, MinimumStopTime="P0D", StopStatus="commercialStop",
                                 SequenceNumber=0)

        test_train_path_node = ConverterLayer.to_AIDM_converter.convert_dict_to_TrainPathNode(test_node_as_dict)

        self.assertIsInstance(test_train_path_node, AIDM_classes.TrainPathNode)
        self.assertEqual(test_train_path_node.ID, 1332)
        self.assertEqual(test_train_path_node.MinimumRunTime, None)
        self.assertEqual(test_train_path_node.MinimumStopTime, datetime.timedelta(0))

    def test_convert_dict_to_AlgorithmTrain(self):
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

        test_train = ConverterLayer.to_AIDM_converter.convert_dict_to_AlgorithmTrain(test_train_as_dict)

        self.assertIsInstance(test_train, AIDM_classes.AlgorithmTrain)
        self.assertIsInstance(test_train.TrainPathNodes[0], AIDM_classes.TrainPathNode)
        self.assertEqual(test_train.TrainPathNodes[0].MinimumRunTime, None)
        self.assertEqual(test_train.TrainPathNodes[0].MinimumStopTime, datetime.timedelta(0))