import datetime
import unittest

import AIDM_module.AIDM_classes
import converter_module.to_AIDM_converter


class AlgorithmTrain(unittest.TestCase):

    def test_train_path_node_objects(self):
        train_path_node_dict = dict(ID=8113, SectionTrackID=None, NodeID=7, NodeTrackID=8, FormationID=1187,
                               ArrivalTime="2003-09-01T00:10:00",
                               DepartureTime="2003-09-01T00:10:00", MinimumRunTime=None, MinimumStopTime="P0D",
                               StopStatus="commercialStop", SequenceNumber=0)

        test_train_path_node = converter_module.to_AIDM_converter.convert_dict_to_TrainPathNode(train_path_node_dict)

        self.assertEqual(8113, test_train_path_node.ID)
        self.assertIsInstance(test_train_path_node.StopStatus, AIDM_module.AIDM_classes.StopStatus)
        self.assertEqual(test_train_path_node.StopStatus, AIDM_module.AIDM_classes.StopStatus['commercialStop'])
        self.assertEqual(test_train_path_node.SequenceNumber, 0)
        self.assertEqual(test_train_path_node.MinimumRunTime, datetime.timedelta(0))
        self.assertEqual(test_train_path_node.NodeTrackID, 8)
        self.assertEqual(test_train_path_node.NodeID, 7)