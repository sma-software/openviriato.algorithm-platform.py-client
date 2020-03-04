import unittest

import AIDM_module.AIDM_factories
from AIDM_module import AIDM_classes


class AlgorithmTrain(unittest.TestCase):

    def test_algorithm_train_from_json_dict_factory(self):
        json_dict = dict(ID=5,
                         DebugString='test_algorithm_train_objects',
                         TrainPathNodes=[
                             dict(ID=2, SectionTrackID=None, NodeID=7, NodeTrackID=8, FormationID=8,
                                  ArrivalTime="2007-08-01T00:10:00",
                                  DepartureTime="2003-09-01T00:10:00", MinimumRunTime=None, MinimumStopTime="P0D",
                                  StopStatus="passing", SequenceNumber=0),
                             dict(ID=8114, SectionTrackID=1175, NodeID=15, NodeTrackID=16, FormationID=None,
                                  ArrivalTime="2003-09-01T00:14:00", DepartureTime="2003-09-01T00:14:00",
                                  MinimumRunTime="PT4M",
                                  MinimumStopTime="P0D", StopStatus="passing", SequenceNumber=1)])

        test_train = AIDM_classes.AlgorithmTrain.from_json_dict_factory(json_dict)
        self.assertEqual(test_train.ID, 5)
        self.assertEqual(test_train.DebugString, "test_algorithm_train_objects")
        self.assertIsInstance(test_train.TrainPathNodes[0], AIDM_classes.TrainPathNode)
        self.assertIsInstance(test_train.TrainPathNodes[1], AIDM_classes.TrainPathNode)