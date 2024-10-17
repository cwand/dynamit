import SimpleITK as sitk
from collections import defaultdict
import dynamit
from typing import Any


def load_dynamic_series(dicom_path: str) -> dict[str, Any]:
    """Loads a dynamic image series. The images and their relative acquisition
    times are stored in a dictionary object. The keys 'img' and 'acq' are
    available:
    Under the key 'img' the images are stored in a list in order of acquisition
    time. Each image is stored as a SimpleITK Image.
    Under the key 'acq' the relative acquisition times are stored in seconds.
    This means: result['img'][i] is acquired result['acq'][i] seconds after
    result['img'][0].

    Arguments:
    dicom_path  --  The path to the dicom files

    Return value:
    A dict-object with keys 'img' (SimpleITK Images in a list) and 'acq'
    (acquisition times in seconds in a list).
    """

    # Prepare reader
    reader = sitk.ImageSeriesReader()

    # Get dicom file names in folder sorted according to acquisition time.
    dcm_names = reader.GetGDCMSeriesFileNames(dicom_path)

    img_arr = []
    acq_arr = []

    # Get acquisition time of first image
    acq0 = dynamit.get_acq_datetime(dcm_names[0])

    for name in dcm_names:
        # Load image and read acquisition time of each image and store in list
        img = sitk.ReadImage(name)
        img_arr.append(img)
        acq_arr.append((dynamit.get_acq_datetime(name)-acq0).total_seconds())

    return {'img': img_arr,
            'acq': acq_arr}


def resample_series_to_reference(series: list[sitk.Image],
                                 ref: sitk.Image) -> list[sitk.Image]:
    """Resample each image in an image series to the same physical space as
    a reference image. The pixel values in the resampled images will be
    interpolated according to the nearest-neighbour principle.

    Arguments:
    series  --  The image series.
    ref     --  The reference image.

    Return value:
    A list containing each resampled image in the same order.
    """

    resampler = sitk.ResampleImageFilter()
    resampler.SetReferenceImage(ref)
    resampler.SetInterpolator(sitk.sitkNearestNeighbor)
    return [resampler.Execute(img) for img in series]


def series_roi_means(series: list[sitk.Image],
                     roi: sitk.Image) -> dict[int, list[float]]:
    """Compute mean image values in a ROI set.
    This function computes the mean image values in a given ROI for every time
    point in the dynamic series.
    The ROI and image should be in the same physical space. The ROI is treated
    as a labelmap with each label value being treated as a seperate ROI.

    Arguments:
    dyn --  The dynamic image series of interes
    roi --  The ROI labelmap image

    Return value:
    A dict object with ROI labels as keys and a list with ROI mean values for
    every time point in the dynamic series as values.
    """

    res = defaultdict(list)

    # Get the number of time points in the dynamic series
    n_frames = len(series)

    label_stats_filter = sitk.LabelStatisticsImageFilter()

    for i in range(n_frames):

        # Get label stats for the i'th image in the series for all labels
        label_stats_filter.Execute(series[i], roi)

        for label in label_stats_filter.GetLabels():
            # Append the mean value to the list for each label.
            res[label].append(label_stats_filter.GetMean(label))

    return res
