import SimpleITK as sitk
import dynamit
import matplotlib.pyplot as plt
import lmfit


def main():

    dyn = dynamit.load_dynamic_series(
        "C:\\Users\\bub8ga\\data\\dynamit-i\\KTH\\NM73"
        # "C:\\Users\\bub8ga\\data\\dynamit1\\kth\\NM73"
    )

    roi = sitk.ReadImage(
        "C:\\Users\\bub8ga\\data\\dynamit-i\\KTH-seg\\kthseg.nrrd"
        # "C:\\Users\\bub8ga\\data\\dynamit1\\kth\\segs\\segs.nrrd"
    )
    # resampler = sitk.ResampleImageFilter()
    # resampler.SetReferenceImage(dyn['img'][0])
    # resampler.SetInterpolator(sitk.sitkNearestNeighbor)
    # roi_r = resampler.Execute(roi)

    resampled = dynamit.resample_series_to_reference(dyn['img'], roi)
    t = dyn['acq']
    means = dynamit.series_roi_means(resampled, roi)

    amp1 = 0.05
    extent1 = 20
    amp2 = 0.01
    extent2 = 170

    print("Fitting Model STEP1")
    t_cut = 30
    model = lmfit.Model(
        dynamit.model_step, independent_vars=['t', 'in_func'])
    res1 = model.fit(means[2][0:t_cut], t=t[0:t_cut],
                     in_func=means[3][0:t_cut], amp=amp2, extent=extent2)
    lmfit.report_fit(res1)
    best_fit = dynamit.model_step(res1.best_values['amp'],
                                  res1.best_values['extent'],
                                  t[0:t_cut],
                                  means[3][0:t_cut])
    print()

    print("Fitting Model STEP2")
    model = lmfit.Model(
        dynamit.model_step_2, independent_vars=['t', 'in_func'])
    res2 = model.fit(means[2][0:t_cut], t=t[0:t_cut],
                     in_func=means[3][0:t_cut],
                     amp1=amp1, extent1=extent1,
                     amp2=amp2, extent2=extent2)
    lmfit.report_fit(res2)
    best_fit2 = dynamit.model_step_2(res2.best_values['amp1'],
                                     res2.best_values['extent1'],
                                     res2.best_values['amp2'],
                                     res2.best_values['extent2'],
                                     t[0:t_cut],
                                     means[3][0:t_cut])
    print()

    print("Fitting Model PATLAK")
    t_cut = 30
    k = 0.01
    v0 = 0.7
    model = lmfit.Model(dynamit.model_patlak,
                        independent_vars=['t', 'in_func'])
    res3 = model.fit(means[2][0:t_cut], t=t[0:t_cut],
                     in_func=means[3][0:t_cut], k=k, v0=v0)
    lmfit.report_fit(res3)
    best_fit3 = dynamit.model_patlak(res3.best_values['k'],
                                     res3.best_values['v0'],
                                     t[0:t_cut],
                                     means[3][0:t_cut])
    print()

    fig, ax = plt.subplots()
    # ax.plot(acqtimes, means[1], 'g.', label="1")
    ax.plot(t, means[2], 'g.', label="Kidney")
    ax.plot(t, means[3], 'r.', label="Blood")
    # ax.plot(dyn.acq_times, m, 'k-', label="model0")
    ax.plot(t[0:t_cut], best_fit, 'g-', label="Fit STEP1")
    ax.plot(t[0:t_cut], best_fit2, 'k-', label="Fit STEP2")
    ax.plot(t[0:t_cut], best_fit3, 'b-', label="Fit PATLAK")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
