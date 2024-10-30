import argparse
import sys

import dynamit
import matplotlib.pyplot as plt
import lmfit
import numpy as np


def main():

    dcm_path = "C:\\Users\\bub8ga\\data\\dynamit-i\\KTH\\NM73"
    # dcm_path = "C:\\Users\\bub8ga\\data\\dynamit1\\kth\\NM73"

    roi_path = "C:\\Users\\bub8ga\\data\\dynamit-i\\KTH-seg\\kthseg.nrrd"
    # roi_path "C:\\Users\\bub8ga\\data\\dynamit1\\kth\\segs\\segs.nrrd"

    dyn = dynamit.lazy_series_roi_means(dcm_path, roi_path, resample='img')

    t = dyn['tacq']
    blood = dyn[3]
    kid1 = dyn[1]
    # kid2 = dyn[2]

    delta_t = 2
    shift_t = [tt - delta_t for tt in t]
    blood_shift = list(np.interp(shift_t, t, blood))

    amp1 = 0.05
    extent1 = 20
    amp2 = 0.01
    extent2 = 170

    '''
    print("Fitting Model STEP1")
    # t_cut = 30
    model = lmfit.Model(
        dynamit.model_step, independent_vars=['t', 'in_func'])
    res1 = model.fit(kid1, t=t,
                     in_func=blood_shift, amp=amp2, extent=extent2)
    lmfit.report_fit(res1)
    best_fit = dynamit.model_step(res1.best_values['amp'],
                                  res1.best_values['extent'],
                                  t,
                                  blood_shift)
    print()
    '''

    print("Fitting Model STEP2")
    model = lmfit.Model(
        dynamit.model_step_2, independent_vars=['t', 'in_func'])
    res2 = model.fit(kid1, t=t,
                     in_func=blood_shift,
                     amp1=amp1, extent1=extent1,
                     amp2=amp2, extent2=extent2)
    lmfit.report_fit(res2)
    best_fit2 = dynamit.model_step_2(res2.best_values['amp1'],
                                     res2.best_values['extent1'],
                                     res2.best_values['amp2'],
                                     res2.best_values['extent2'],
                                     t,
                                     blood_shift)
    print()

    '''
    print("Fitting Model PATLAK")
    k = 0.01
    v0 = 0.7
    model = lmfit.Model(dynamit.model_patlak,
                        independent_vars=['t', 'in_func'])
    res3 = model.fit(kid1, t=t,
                     in_func=blood_shift, k=k, v0=v0)
    lmfit.report_fit(res3)
    best_fit3 = dynamit.model_patlak(res3.best_values['k'],
                                     res3.best_values['v0'],
                                     t,
                                     blood_shift)
    print()
    '''

    fig, ax = plt.subplots()
    ax.plot(t, kid1, 'gx', label="Kidney")
    ax.plot(t, blood, 'rx', label="Blood")
    ax.plot(t, blood_shift, 'kx', label="Blood shifted")
    # ax.plot(t, best_fit, 'g-', label="Fit STEP1")
    ax.plot(t, best_fit2, 'k-', label="Fit STEP2")
    # ax.plot(t, best_fit3, 'b-', label="Fit PATLAK")
    plt.legend()
    plt.show()


def roi_means():

    parser = argparse.ArgumentParser(
        description="Calculate image series ROI-mean values."
    )

    parser.add_argument('task', choices=['roi_means'])

    parser.add_argument('image_dir',
                        help='The directory containing the image series.')
    parser.add_argument('roi_file',
                        help='The file containing the ROI image.')
    parser.add_argument('output_file',
                        help='Where to write the output file.')

    args = parser.parse_args()

    print("Starting image read and ROI-mean calculation.")
    print("Reading images from ", args.image_dir, ".")
    print("Reading ROI image from ", args.roi_file, ".")
    print("Processing...")
    dyn = dynamit.lazy_series_roi_means(args.image_dir,
                                        args.roi_file,
                                        resample='img')
    print("... done!")
    print()

    print("Saving images to file ", args.output_file, ".")
    print("Saving...")
    columns = []
    header = []
    for label in dyn:
        columns.append(dyn[label])
        header.append(label)

    data = np.column_stack(columns)
    np.savetxt(args.output_file, data, header=str(header))
    print("... done!")


if __name__ == "__main__":
    if sys.argv[1] == 'roi_means':
        roi_means()
