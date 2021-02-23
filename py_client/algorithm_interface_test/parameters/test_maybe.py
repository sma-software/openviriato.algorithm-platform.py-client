from unittest import TestCase

from py_client.aidm.maybe import Maybe


class TestMaybe(TestCase):
    def test_with_value(self):
        maybe_with_not_none = Maybe(19)

        self.assertTrue(maybe_with_not_none.has_value)
        self.assertEqual(maybe_with_not_none.get_value, 19)

    def test_with_none(self):
        maybe_with_none = Maybe(None)

        self.assertFalse(maybe_with_none.has_value)

        with self.assertRaises(ValueError) as error_instance:
            _ = maybe_with_none.get_value

        self.assertEqual(error_instance.exception.args[0], 'Tried to get a None-value from a Maybe')
