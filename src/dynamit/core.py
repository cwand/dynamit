import SimpleITK as sitk
from datetime import datetime


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
