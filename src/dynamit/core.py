import SimpleITK as sitk
from datetime import datetime
import numpy as np


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


def shift_time(y: list[float], t: list[float],
               deltat: float) -> list[float]:
    """Given the samples y of a function y(t) sampled at the time points t,
    this function computes the samples of another function x(t) at the same
    time points under the assumption that x(t) = y(t-deltat), i.e. that x is
    shifted deltat units of time to the right from y. Since y is not
    necessarily known at these time points, y is linearly interpolated between
    the samples.
    Depending on the sign of deltat we will have to extrapolate y(t) either
    before the first sample or after the last sample. In either case we simply
    use the value of the extreme sample value for the extrapolation, i.e. if
    deltat is positive any extrapolation beyond the first sample point will
    simply take the value of the first sample, and if deltat is negative any
    extrapolation beyond the last sample point will take the value of the last
    sample.

    Arguments:
    y       --  The samples of the original function at time points t
    t       --  The time points of the samples of the original function
    deltat  --  The time shift

    Return value:
    A list of the interpolated values of the function x(t) = y(t-deltat).
    """

    # Construct the timepoints where y should be interpolated
    t_inter = [tt - deltat for tt in t]

    return list(np.interp(t_inter, t, y))
