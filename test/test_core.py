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
