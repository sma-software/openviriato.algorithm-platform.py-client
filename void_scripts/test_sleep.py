import time
import unittest


class sleepeertest(unittest.TestCase):

    def test_sleep(self):
        for i in range(3):
            time.sleep(i)
            print("slept for {0} seconds".format(i))
