import AIDMClasses.AIDM_enum_classes
import unittest


class TestStationEntryOrExit(unittest.TestCase):

    def test_station_entry_or_exit_undef_state(self):
        status_string = 'There almost never a stop State with this Name as an ID XY@sdf'

        with self.assertRaises(KeyError) as test_parse_to_datetime_wrong_format:
            AIDMClasses.AIDM_enum_classes.StationEntryOrExit[status_string]

    def test_station_entry_or_exit_exit_state(self):
        status_string = 'exit'

        stop_status = AIDMClasses.AIDM_enum_classes.StationEntryOrExit[status_string]

        self.assertIsInstance(stop_status, AIDMClasses.AIDM_enum_classes.StationEntryOrExit)
        self.assertEqual(stop_status.name, 'exit')
