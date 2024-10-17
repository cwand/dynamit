import os.path
import unittest
import dynamit
import SimpleITK as sitk


class TestLoadDynamicSeries(unittest.TestCase):

    def test_load_dynamic_series_8_3V(self):
        dcm_path = os.path.join('test', 'data', '8_3V')
        dyn = dynamit.load_dynamic_series(dcm_path)
        img = dyn['img']
        acq = dyn['acq']
        self.assertEqual(len(img), 9)
        self.assertEqual(img[0].GetSize(), (128, 128, 64))
        self.assertEqual(img[0].GetSpacing(), (4.92, 4.92, 4.92))
        self.assertEqual(img[0].GetDimension(), 3)
        self.assertEqual(img[1].GetSize(), (128, 128, 64))
        self.assertEqual(img[1].GetSpacing(), (4.92, 4.92, 4.92))
        self.assertEqual(img[1].GetDimension(), 3)
        self.assertEqual(img[2].GetSize(), (128, 128, 64))
        self.assertEqual(img[2].GetSpacing(), (4.92, 4.92, 4.92))
        self.assertEqual(img[2].GetDimension(), 3)
        self.assertEqual(img[3].GetSize(), (128, 128, 64))
        self.assertEqual(img[3].GetSpacing(), (4.92, 4.92, 4.92))
        self.assertEqual(img[3].GetDimension(), 3)
        self.assertEqual(img[4].GetSize(), (128, 128, 64))
        self.assertEqual(img[4].GetSpacing(), (4.92, 4.92, 4.92))
        self.assertEqual(img[4].GetDimension(), 3)
        self.assertEqual(img[5].GetSize(), (128, 128, 64))
        self.assertEqual(img[5].GetSpacing(), (4.92, 4.92, 4.92))
        self.assertEqual(img[5].GetDimension(), 3)
        self.assertEqual(img[6].GetSize(), (128, 128, 64))
        self.assertEqual(img[6].GetSpacing(), (4.92, 4.92, 4.92))
        self.assertEqual(img[6].GetDimension(), 3)
        self.assertEqual(img[7].GetSize(), (128, 128, 64))
        self.assertEqual(img[7].GetSpacing(), (4.92, 4.92, 4.92))
        self.assertEqual(img[7].GetDimension(), 3)
        self.assertEqual(img[8].GetSize(), (128, 128, 64))
        self.assertEqual(img[8].GetSpacing(), (4.92, 4.92, 4.92))
        self.assertEqual(img[8].GetDimension(), 3)
        self.assertEqual(acq,
                         [0, 3.0, 6.3, 9.5, 12.8, 16.0, 19.3, 22.5, 25.8])


class TestResampleSeriesToReference(unittest.TestCase):

    def test_resample_series_to_reference_8_3V(self):
        dcm_path = os.path.join('test', 'data', '8_3V')
        dyn = dynamit.load_dynamic_series(dcm_path)

        ref_img = sitk.ReadImage(os.path.join(
            'test', 'data', '8_3V_seg', 'Segmentation_2.nrrd'))

        img = dynamit.resample_series_to_reference(dyn['img'], ref_img)
        self.assertEqual(img[0].GetSize(), (512, 512, 132))
        self.assertAlmostEqual(img[0].GetSpacing()[0], 1.269531, places=5)
        self.assertAlmostEqual(img[0].GetSpacing()[1], 1.269531, places=5)
        self.assertAlmostEqual(img[0].GetSpacing()[2], 2.5, places=5)
        self.assertEqual(img[0].GetDimension(), 3)
        self.assertEqual(img[1].GetSize(), (512, 512, 132))
        self.assertAlmostEqual(img[1].GetSpacing()[0], 1.269531, places=5)
        self.assertAlmostEqual(img[1].GetSpacing()[1], 1.269531, places=5)
        self.assertAlmostEqual(img[1].GetSpacing()[2], 2.5, places=5)
        self.assertEqual(img[1].GetDimension(), 3)
        self.assertEqual(img[2].GetSize(), (512, 512, 132))
        self.assertAlmostEqual(img[2].GetSpacing()[0], 1.269531, places=5)
        self.assertAlmostEqual(img[2].GetSpacing()[1], 1.269531, places=5)
        self.assertAlmostEqual(img[2].GetSpacing()[2], 2.5, places=5)
        self.assertEqual(img[2].GetDimension(), 3)
        self.assertEqual(img[3].GetSize(), (512, 512, 132))
        self.assertAlmostEqual(img[3].GetSpacing()[0], 1.269531, places=5)
        self.assertAlmostEqual(img[3].GetSpacing()[1], 1.269531, places=5)
        self.assertAlmostEqual(img[3].GetSpacing()[2], 2.5, places=5)
        self.assertEqual(img[3].GetDimension(), 3)
        self.assertEqual(img[4].GetSize(), (512, 512, 132))
        self.assertAlmostEqual(img[4].GetSpacing()[0], 1.269531, places=5)
        self.assertAlmostEqual(img[4].GetSpacing()[1], 1.269531, places=5)
        self.assertAlmostEqual(img[4].GetSpacing()[2], 2.5, places=5)
        self.assertEqual(img[4].GetDimension(), 3)
        self.assertEqual(img[5].GetSize(), (512, 512, 132))
        self.assertAlmostEqual(img[5].GetSpacing()[0], 1.269531, places=5)
        self.assertAlmostEqual(img[5].GetSpacing()[1], 1.269531, places=5)
        self.assertAlmostEqual(img[5].GetSpacing()[2], 2.5, places=5)
        self.assertEqual(img[5].GetDimension(), 3)
        self.assertEqual(img[6].GetSize(), (512, 512, 132))
        self.assertAlmostEqual(img[6].GetSpacing()[0], 1.269531, places=5)
        self.assertAlmostEqual(img[6].GetSpacing()[1], 1.269531, places=5)
        self.assertAlmostEqual(img[6].GetSpacing()[2], 2.5, places=5)
        self.assertEqual(img[6].GetDimension(), 3)
        self.assertEqual(img[7].GetSize(), (512, 512, 132))
        self.assertAlmostEqual(img[7].GetSpacing()[0], 1.269531, places=5)
        self.assertAlmostEqual(img[7].GetSpacing()[1], 1.269531, places=5)
        self.assertAlmostEqual(img[7].GetSpacing()[2], 2.5, places=5)
        self.assertEqual(img[7].GetDimension(), 3)
        self.assertEqual(img[8].GetSize(), (512, 512, 132))
        self.assertAlmostEqual(img[8].GetSpacing()[0], 1.269531, places=5)
        self.assertAlmostEqual(img[8].GetSpacing()[1], 1.269531, places=5)
        self.assertAlmostEqual(img[8].GetSpacing()[2], 2.5, places=5)
        self.assertEqual(img[8].GetDimension(), 3)


class TestSeriesRoiMeans(unittest.TestCase):

    def test_series_roi_means_8_3V(self):
        dcm_path = os.path.join('test', 'data', '8_3V')
        roi_path = os.path.join(
            'test', 'data', '8_3V_seg', 'Segmentation.nrrd')
        dyn = dynamit.load_dynamic_series(dcm_path)
        roi = sitk.ReadImage(roi_path)

        r = dynamit.series_roi_means(dyn['img'], roi)

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
