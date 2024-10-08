import SimpleITK as sitk
from datetime import datetime
from collections import defaultdict


class Dynamic:

    image: sitk.Image
    acq_times: list[float]

    def __init__(self, image_in: sitk.Image, acq_times_in: list[float]):
        self.image = image_in
        self.acq_times = acq_times_in


def get_acq_datetime(dicom_path: str) -> datetime:
    img = sitk.ReadImage(dicom_path)
    img_time = img.GetMetaData('0008|0032')
    img_date = img.GetMetaData('0008|0022')
    sd = img_date[:4] + "-" + img_date[4:6] + "-" + img_date[6:]
    sd = sd + " " + img_time[:2] + ":" + img_time[2:4] + ":" + img_time[4:6]
    sd = sd + "." + img_time[-1] + "00"
    return datetime.fromisoformat(sd)


def load_dynamic(dicom_path: str) -> Dynamic:
    reader = sitk.ImageSeriesReader()
    dcm_names = reader.GetGDCMSeriesFileNames(dicom_path)
    reader.SetFileNames(dcm_names)
    image = reader.Execute()

    acq_times = [0.0]

    acq0 = get_acq_datetime(dcm_names[0])
    for dcm_name in dcm_names[1:]:
        acq = get_acq_datetime(dcm_name)
        acq_times.append((acq - acq0).total_seconds())

    return Dynamic(image, acq_times)


def roi_mean(dyn: Dynamic, roi: sitk.Image) -> dict[int, list[float]]:
    res = defaultdict(list)
    n_frames = dyn.image.GetSize()[3]
    for i in range(n_frames):
        label_stats_filter = sitk.LabelStatisticsImageFilter()
        label_stats_filter.Execute(dyn.image[:, :, :, i], roi)
        for label in label_stats_filter.GetLabels():
            res[label].append(label_stats_filter.GetMean(label))
    return res
