import SimpleITK as sitk


def main():
    image = sitk.ReadImage("C:\\Users\\bub8ga\\data\\dynamit1\\kth\\NM73\\NM000031.dcm")

    roi = sitk.ReadImage("C:\\Users\\bub8ga\\data\\dynamit1\\kth\\segs\\segs.nrrd")

    resampler = sitk.ResampleImageFilter()
    resampler.SetReferenceImage(image)
    resampler.SetInterpolator(sitk.sitkNearestNeighbor)
    resampler.SetOutputPixelType(roi.GetPixelID())
    resampled_roi = resampler.Execute(roi)

    label_stats_filter = sitk.LabelStatisticsImageFilter()
    label_stats_filter.Execute(image, resampled_roi)

    for label in label_stats_filter.GetLabels():
        print(f"Label: {label}")
        print(f"Mean ROI-value: {label_stats_filter.GetMean(label)}")


if __name__ == "__main__":
    main()
