import SimpleITK as sitk
import dynamit
import matplotlib.pyplot as plt
import lmfit


def main():

    dyn = dynamit.load_dynamic(
        # os.path.join('test', 'data', '8_3V')
        # "C:\\Users\\bub8ga\\data\\dynamit-i\\KTH\\NM73"
        "C:\\Users\\bub8ga\\data\\dynamit1\\kth\\NM73"
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
        # "C:\\Users\\bub8ga\\data\\dynamit-i\\KTH-seg\\kthseg.nrrd"
        "C:\\Users\\bub8ga\\data\\dynamit1\\kth\\segs\\segs.nrrd"
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

    amp1 = 0.05
    extent1 = 20
    amp2 = 0.01
    extent2 = 170
    m = dynamit.model_step_2(amp1, extent1, amp2, extent2, acqtimes, means[3])

    model = lmfit.Model(
        dynamit.model_step_2, independent_vars=['t', 'in_func'])
    res = model.fit(means[2], t=acqtimes, in_func=means[3],
                    amp1=amp1, extent1=extent1,
                    amp2=amp2, extent2=extent2)
    lmfit.report_fit(res)
    best_fit = dynamit.model_step_2(res.best_values['amp1'],
                                    res.best_values['extent1'],
                                    res.best_values['amp2'],
                                    res.best_values['extent2'],
                                    acqtimes,
                                    means[3])

    fig, ax = plt.subplots()
    # ax.plot(acqtimes, means[1], 'g.', label="1")
    ax.plot(acqtimes, means[2], 'g.', label="2")
    ax.plot(acqtimes, means[3], 'r.', label="3")
    ax.plot(acqtimes, m, 'k-', label="model0")
    ax.plot(acqtimes, best_fit, 'g-', label="fit")
    plt.show()


if __name__ == "__main__":
    main()
