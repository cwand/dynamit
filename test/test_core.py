import os.path
import unittest
from datetime import datetime
import dynamit
import SimpleITK as sitk


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


class TestLoadDynamic(unittest.TestCase):

    def test_load_dynamic_series_8_3V(self):
        dcm_path = os.path.join('test', 'data', '8_3V')
        dyn = dynamit.load_dynamic(dcm_path)
        image: sitk.Image = dyn.image
        self.assertEqual(image.GetSize(), (128, 128, 64, 9))
        self.assertEqual(image.GetSpacing(), (4.92, 4.92, 4.92, 1.0))
        self.assertEqual(image.GetDimension(), 4)
        self.assertEqual(dyn.acq_times,
                         [0, 3.0, 6.3, 9.5, 12.8, 16.0, 19.3, 22.5, 25.8])

    def test_load_dynamic_report(self):
        dcm_path = os.path.join('test', 'data', '8_3V')
        dyn = dynamit.load_dynamic(dcm_path)
        s = dyn.report()
        x = s.splitlines()
        self.assertEqual(4, len(x))
        self.assertEqual("Image size: (128, 128, 64, 9)", x[0])
        self.assertEqual("Image spacing: (4.92, 4.92, 4.92, 1.0)", x[1])
        self.assertEqual("Image dimension: 4", x[2])
        self.assertEqual("Acquisition time points: [0.0, 3.0, 6.3, 9.5, "
                         "12.8, 16.0, 19.3, 22.5, 25.8]", x[3])


class TestROIMean(unittest.TestCase):

    def test_means_8_3V(self):
        dcm_path = os.path.join('test', 'data', '8_3V')
        roi_path = os.path.join(
            'test', 'data', '8_3V_seg', 'Segmentation.nrrd')
        dyn = dynamit.load_dynamic(dcm_path)
        roi = sitk.ReadImage(roi_path)

        r = dynamit.roi_mean(dyn, roi)

        self.assertEqual(r[1][0], 0)
        self.assertAlmostEqual(r[2][0], 31.3157, places=4)

        self.assertAlmostEqual(r[1][1], 0.767681, places=6)
        self.assertAlmostEqual(r[2][1], 3501.54, places=2)

        self.assertAlmostEqual(r[1][2], 1229.61, places=2)
        self.assertAlmostEqual(r[2][2], 33128.1, places=1)

        self.assertAlmostEqual(r[1][3], 12019.3, places=1)
        self.assertAlmostEqual(r[2][3], 38544.1, places=1)

        self.assertAlmostEqual(r[1][4], 12058.9, places=1)
        self.assertAlmostEqual(r[2][4], 9529.26, places=2)

        self.assertAlmostEqual(r[1][5], 1277.01, places=2)
        self.assertAlmostEqual(r[2][5], 642.525, places=3)

        self.assertAlmostEqual(r[1][6], 13.4822, places=4)
        self.assertAlmostEqual(r[2][6], 2.57748, places=5)

        self.assertAlmostEqual(r[1][7], 0.748028, places=6)
        self.assertAlmostEqual(r[2][7], 0.345963, places=6)

        self.assertEqual(r[1][8], 0)
        self.assertAlmostEqual(r[2][8], 0.0727437, places=7)
