import SimpleITK as sitk
from datetime import datetime
from collections import defaultdict


class Dynamic:
    """A collection of a dynamic image series and the image acquisition times.
    The image acquisition times are stored in seconds after the first image in
    the series.

    Member fields:
    image       --  the dynamic images stored in a SimpleITK Image.
    acq_times   --  a list containing the image acquisition times.
    """

    image: sitk.Image
    acq_times: list[float]

    def __init__(self, image_in: sitk.Image, acq_times_in: list[float]):
        """Constructor for a Dynamic object.

        Arguments:
        image_in        --  The dynamic image series as a 4D SimpleITK Image
        acq_times_in    --  The acquisition times
        """
        self.image = image_in
        self.acq_times = acq_times_in


def get_acq_datetime(dicom_path: str) -> datetime:
    """Get an image acquisition datetime from its dicom header.
    Dicom images store the acquisition date and time in tags in the images
    dicom header. This function reads the relevant tags and turns it into a
    datetime object.

    Arguments:
    dicom_path  --  The path to the dicom file.

    Return value:
    A datetime object representing the date and time of the acquisition.
    """

    # Read the dicom image into Simple ITK
    img = sitk.ReadImage(dicom_path)

    # Read the relevant header tags as strings
    img_time = img.GetMetaData('0008|0032')
    img_date = img.GetMetaData('0008|0022')

    # Format the strings into ISO 8601 format [ YYYY-MM-DD hh:mm:ss.ffffff ]
    sd = img_date[:4] + "-" + img_date[4:6] + "-" + img_date[6:]
    sd = sd + " " + img_time[:2] + ":" + img_time[2:4] + ":" + img_time[4:6]
    sd = sd + "." + img_time[-1].ljust(6, "0")
    return datetime.fromisoformat(sd)


def load_dynamic(dicom_path: str) -> Dynamic:
    """Loads a dynamic image series and stores it in Dynamic object.

    Arguments:
    dicom_path  --  The path to the dicom files

    Return value:
    A Dynamic object containing the images and acquisition times of the series
    """

    # Prepare a SimpleITK reader for loading the images
    reader = sitk.ImageSeriesReader()

    # Get a sorted (according to acquisition time) list of file names to laod
    dcm_names = reader.GetGDCMSeriesFileNames(dicom_path)

    # Read the images in order
    reader.SetFileNames(dcm_names)
    image = reader.Execute()

    # Make a list of acquisition times, starting with 0.0 for the first image
    acq_times = [0.0]

    # Read the date and time of the first image
    acq0 = get_acq_datetime(dcm_names[0])

    # Read the date and time for the rest of the images and compute difference
    for dcm_name in dcm_names[1:]:
        acq = get_acq_datetime(dcm_name)
        acq_times.append((acq - acq0).total_seconds())

    return Dynamic(image, acq_times)


def roi_mean(dyn: Dynamic, roi: sitk.Image) -> dict[int, list[float]]:
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

    # Gets the number of time points in the dynamic series
    n_frames = dyn.image.GetSize()[3]

    for i in range(n_frames):
        label_stats_filter = sitk.LabelStatisticsImageFilter()

        # Get label stats for the i'th image in the series for all labels
        label_stats_filter.Execute(dyn.image[:, :, :, i], roi)

        for label in label_stats_filter.GetLabels():
            # Append the mean value to the list for each label.
            res[label].append(label_stats_filter.GetMean(label))

    return res
