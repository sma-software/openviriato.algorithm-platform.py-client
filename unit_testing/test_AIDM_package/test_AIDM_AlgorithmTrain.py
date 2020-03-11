import unittest

import AIDMClasses.AIDM_classes
import ConverterLayer.to_AIDM_converter


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

        test_algo_train = ConverterLayer.to_AIDM_converter.convert_dict_to_AlgorithmTrain(json_dict)

        self.assertEqual(test_algo_train.ID, 5)
        self.assertEqual(test_algo_train.DebugString, "test_algorithm_train_objects")
        self.assertIsInstance(test_algo_train.TrainPathNodes[0], AIDMClasses.AIDM_classes.TrainPathNode)
        self.assertEqual(test_algo_train.TrainPathNodes[0].ID, 2)