import datetime
import unittest

import AIDMClasses.AIDM_classes
import AIDMClasses.AIDM_enum_classes
import Conversion.to_AIDM_converter


class TestTrainPathNode(unittest.TestCase):

    def test_convert_dict_to_TrainPathNode(self):
        train_path_node_dict = dict(ID=8113, SectionTrackID=None, NodeID=7, NodeTrackID=8, FormationID=1187,
                                    ArrivalTime="2002-01-01T00:07:00",
                                    DepartureTime="2003-09-01T00:10:00", MinimumRunTime=None, MinimumStopTime="PT1M",
                                    StopStatus="commercialStop", SequenceNumber=0)

        test_train_path_node = Conversion.to_AIDM_converter.convert_dict_to_TrainPathNode(train_path_node_dict)

        self.assertEqual(8113, test_train_path_node.ID)
        self.assertEqual(test_train_path_node.FormationID, 1187)
        self.assertIsInstance(test_train_path_node.StopStatus, AIDMClasses.AIDM_enum_classes.StopStatus)
        self.assertEqual(test_train_path_node.StopStatus, AIDMClasses.AIDM_enum_classes.StopStatus['commercialStop'])
        self.assertEqual(test_train_path_node.SequenceNumber, 0)
        self.assertEqual(test_train_path_node.MinimumStopTime, datetime.timedelta(seconds=60))
        self.assertEqual(test_train_path_node.MinimumRunTime, None)
        self.assertEqual(test_train_path_node.ArrivalTime,
                         datetime.datetime(year=2002, month=1, day=1, hour=0, minute=7))
        self.assertEqual(test_train_path_node.DepartureTime,
                         datetime.datetime(year=2003, month=9, day=1, hour=0, minute=10))
        self.assertEqual(test_train_path_node.NodeTrackID, 8)
        self.assertEqual(test_train_path_node.NodeID, 7)

    def test_convert_dict_to_TrainPathNode_MinimumStopTime_wrongly_none(self):
        train_path_node_dict = dict(ID=8113, SectionTrackID=None, NodeID=7, NodeTrackID=8, FormationID=1187,
                                    ArrivalTime="2002-01-01T00:07:00",
                                    DepartureTime="2003-09-01T00:10:00", MinimumRunTime=None, MinimumStopTime=None,
                                    StopStatus="commercialStop", SequenceNumber=0)
        with self.assertRaises(TypeError) as MinimumStopTime_wrongly_none:
            test_train_path_node = Conversion.to_AIDM_converter.convert_dict_to_TrainPathNode(
                train_path_node_dict)
