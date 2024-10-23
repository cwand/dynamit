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

    resampled = dynamit.resample_series_to_reference(dyn['img'], roi)
    t = dyn['acq']
    means = dynamit.series_roi_means(resampled, roi)

    amp1 = 0.05
    extent1 = 20
    amp2 = 0.01
    extent2 = 170

    print("Fitting Model STEP1")
    model = lmfit.Model(
        dynamit.model_step, independent_vars=['t', 'in_func'])
    res = model.fit(means[2], t=t, in_func=means[3],
                    amp=amp2, extent=extent2)
    lmfit.report_fit(res)
    best_fit = dynamit.model_step(res.best_values['amp'],
                                  res.best_values['extent'],
                                  t,
                                  means[3])
    print()

    print("Fitting Model STEP2")
    model = lmfit.Model(
        dynamit.model_step_2, independent_vars=['t', 'in_func'])
    res = model.fit(means[2], t=t, in_func=means[3],
                    amp1=amp1, extent1=extent1,
                    amp2=amp2, extent2=extent2)
    lmfit.report_fit(res)
    best_fit2 = dynamit.model_step_2(res.best_values['amp1'],
                                     res.best_values['extent1'],
                                     res.best_values['amp2'],
                                     res.best_values['extent2'],
                                     t,
                                     means[3])
    print()

    fig, ax = plt.subplots()
    # ax.plot(acqtimes, means[1], 'g.', label="1")
    ax.plot(t, means[2], 'g.', label="Kidney")
    ax.plot(t, means[3], 'r.', label="Blood")
    # ax.plot(dyn.acq_times, m, 'k-', label="model0")
    ax.plot(t, best_fit, 'g-', label="Fit STEP1")
    ax.plot(t, best_fit2, 'k-', label="Fit STEP2")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
