import unittest
import dynamit


class TestCore(unittest.TestCase):

    def test_add(self):
        t = dynamit.add(2, 3)
        self.assertEqual(t, 5)
