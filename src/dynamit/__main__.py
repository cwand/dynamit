import SimpleITK as sitk
import dynamit
import matplotlib.pyplot as plt


def main():

    dyn = dynamit.load_dynamic(
        # os.path.join('test', 'data', '8_3V')
        "C:\\Users\\bub8ga\\data\\dynamit-i\\KTH\\NM73"
    )
    image = dyn.image
    acqtimes = dyn.acq_times

    print("Image Size:", image.GetSize())
    print("Image Spacing:", image.GetSpacing())
    print("Image Dimension:", image.GetDimension())
    print("Image Origin:", image.GetOrigin())
    print("Acquisition time points: ", acqtimes)
    print()

    roi = sitk.ReadImage(
        # os.path.join('test', 'data', '8_3V_seg', 'Segmentation.nrrd')
        "C:\\Users\\bub8ga\\data\\dynamit-i\\KTH-seg\\kthseg.nrrd"
    )
    print("ROI Size:", image.GetSize())
    print("ROI Spacing:", image.GetSpacing())
    print("ROI Dimension:", image.GetDimension())
    print("ROI Origin:", image.GetOrigin())
    print()

    img3 = image[:, :, :, 0]

    resampler = sitk.ResampleImageFilter()
    resampler.SetReferenceImage(img3)
    resampler.SetInterpolator(sitk.sitkNearestNeighbor)
    resampler.SetOutputPixelType(roi.GetPixelID())
    resampled_roi = resampler.Execute(roi)

    means = dynamit.roi_mean(dyn, resampled_roi)

    # fit(means, acqtimes, ...)

    fig, ax = plt.subplots()
    ax.plot(acqtimes, means[1], 'kx-', label="1")
    ax.plot(acqtimes, means[2], 'gx-', label="2")
    ax.plot(acqtimes, means[3], 'rx-', label="3")
    plt.show()


if __name__ == "__main__":
    main()
