from datetime import datetime
import unittest

from py_client.aidm.aidm_conflict import ConflictDetectionArguments
from py_client.aidm.aidm_time_window_classes import TimeWindow
from py_client.aidm.aidm_conflict import ConflictType


class TestConflictDetectionArguments(unittest.TestCase):
    def test_mandatory_filter(self):
        train_ids = [1234, 1237]
        conflict_detection_arguments = ConflictDetectionArguments(train_ids)

        self.assertIsInstance(conflict_detection_arguments, ConflictDetectionArguments)

        self.assertEqual(conflict_detection_arguments.filter_conflict_types, None)

        self.assertEqual(conflict_detection_arguments.filter_node_ids, None)

        self.assertEqual(conflict_detection_arguments.filter_section_track_ids, None)

        self.assertEqual(conflict_detection_arguments.filter_train_id, None)

        self.assertEqual(conflict_detection_arguments.time_window, None)

        self.assertIsInstance(conflict_detection_arguments.train_ids, list)
        self.assertEqual(conflict_detection_arguments.train_ids, train_ids)

    def test_non_mandatory_filters(self):
        train_ids = [1234, 1237]
        filter_node_ids = [1456, 1457]
        filter_section_track_ids = [1654, 1657]
        conflict_types = [ConflictType.Crossing, ConflictType.InvalidDrivingDirection]
        train_id = 1230
        time_window = TimeWindow(
            from_time=datetime(year=2022, month=2, day=7, hour=17, minute=10), to_time=datetime(year=2022, month=2, day=7, hour=17, minute=15)
        )

        conflict_detection_arguments = (
            ConflictDetectionArguments(train_ids)
            .with_type_filter(conflict_types)
            .with_location_filter(filter_node_ids, filter_section_track_ids)
            .with_train_filter(train_id)
            .with_time_filter(time_window)
        )

        self.assertIsInstance(conflict_detection_arguments, ConflictDetectionArguments)

        self.assertIsInstance(conflict_detection_arguments.filter_conflict_types, list)
        self.assertEqual(conflict_detection_arguments.filter_conflict_types, [ConflictType.Crossing, ConflictType.InvalidDrivingDirection])

        self.assertIsInstance(conflict_detection_arguments.filter_node_ids, list)
        self.assertEqual(conflict_detection_arguments.filter_node_ids, [1456, 1457])

        self.assertIsInstance(conflict_detection_arguments.filter_section_track_ids, list)
        self.assertEqual(conflict_detection_arguments.filter_section_track_ids, [1654, 1657])

        self.assertEqual(conflict_detection_arguments.filter_train_id, 1230)

        self.assertIsInstance(conflict_detection_arguments.time_window, TimeWindow)
        self.assertEqual(conflict_detection_arguments.time_window.from_time, datetime(year=2022, month=2, day=7, hour=17, minute=10))
        self.assertEqual(conflict_detection_arguments.time_window.to_time, datetime(year=2022, month=2, day=7, hour=17, minute=15))

        self.assertIsInstance(conflict_detection_arguments.train_ids, list)
        self.assertEqual(conflict_detection_arguments.train_ids, [1234, 1237])
