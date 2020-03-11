import AIDMClasses.AIDM_enum_classes
import unittest


class TestStopStatus(unittest.TestCase):

    def test_stop_status_init_undef_state(self):
        status_string = 'There almost never a stop State with this Name as an ID XY@sdf'

        with self.assertRaises(KeyError) as test_parse_to_datetime_wrong_format:
            AIDMClasses.AIDM_enum_classes.StopStatus[status_string]

    def test_stop_status_init_passing_state(self):
        status_string = 'passing'

        stop_status = AIDMClasses.AIDM_enum_classes.StopStatus[status_string]

        self.assertIsInstance(stop_status, AIDMClasses.AIDM_enum_classes.StopStatus)
        self.assertEqual(stop_status.name, 'passing')
