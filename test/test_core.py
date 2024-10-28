import os.path
import unittest
from datetime import datetime
import dynamit


class TestGetAcqDateTime(unittest.TestCase):

    def test_acq_datetime_8_3V_1(self):
        dcm_path = os.path.join(
            'test', 'data', '8_3V',
            'Patient_test_Study_10_Scan_10_Bed_1_Dyn_1.dcm')
        dt = dynamit.get_acq_datetime(dcm_path)
        self.assertEqual(dt, datetime(2023, 12, 1, 13, 30, 28, 0))

    def test_acq_datetime_8_3V_5(self):
        dcm_path = os.path.join(
            'test', 'data', '8_3V',
            'Patient_test_Study_10_Scan_10_Bed_1_Dyn_5.dcm')
        dt = dynamit.get_acq_datetime(dcm_path)
        self.assertEqual(dt, datetime(2023, 12, 1, 13, 30, 40, 800000))


class TestShiftTime(unittest.TestCase):

    def test_shift_time_one_step(self):
        res = dynamit.shift_time([1.0, 2.0], [1.0, 2.0], 1.0)
        self.assertEqual(2, len(res))
        self.assertAlmostEqual(1.0, res[0], places=6)
        self.assertAlmostEqual(1.0, res[1], places=6)

    def test_shift_time_one_and_a_half_steps(self):
        res = dynamit.shift_time([2.0, 4.0, 3.0], [1.0, 2.0, 3.0], 1.5)
        self.assertEqual(3, len(res))
        self.assertAlmostEqual(2.0, res[0], places=6)
        self.assertAlmostEqual(2.0, res[1], places=6)
        self.assertAlmostEqual(3.0, res[2], places=6)
