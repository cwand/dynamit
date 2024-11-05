import argparse
import sys

import dynamit
import matplotlib.pyplot as plt
import lmfit
import numpy as np
import xmltodict
from typing import Any, Callable, OrderedDict


def main(argv: list[str]):

    print("Starting DYNAMIT1")
    print()

    tasks: dict[str,
                Callable[[OrderedDict[str, Any], dict[str, Any]], None]] = {}

    named_obj: dict[str, Any] = {}

    # Parse XML input file
    if len(argv) != 1:
        exit("Missing command line argument: path to an XML file.")
    xml_file = open(argv[0], "r")
    task_tree = xmltodict.parse(xml_file.read(), force_list=('task'))
    root = task_tree['dynamit1']

    for task in root['task']:
        tasks[task['@name']](task, named_obj)

    print("DYNAMIT1 ended!")

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
    header = ""
    for label in dyn:
        columns.append(dyn[label])
        header = header + str(label) + "   "

    print(header)

    data = np.column_stack(columns)
    np.savetxt(args.output_file, data, header=header)
    print("... done!")


def tac_fit():
    parser = argparse.ArgumentParser(
        description="Fit model to TAC data."
    )

    parser.add_argument('task', choices=['tac_fit'])

    parser.add_argument('tac_file',
                        help='The file containing the TAC data.')
    parser.add_argument('t',
                        help='The column containing the acquisition times.')
    parser.add_argument('inp',
                        help='The column containing the input function data.')
    parser.add_argument('tis',
                        help='The column containing the tissue data.')
    parser.add_argument('model', choices=['step', 'step2', 'patlak'],
                        help='The fit model to use.')

    args = parser.parse_args()

    print("Reading TACs from ", args.tac_file, "...")
    with open(args.tac_file) as f:
        header = f.readline()
    header_cols = header.split()
    header_cols = header_cols[1:]
    data = np.loadtxt(args.tac_file)
    data_dict = {}
    for i in range(len(header_cols)):
        data_dict[header_cols[i]] = data[:, i]
    print("... done!")
    print()

    model_dict = {
        'step': dynamit.model_step,
        'step2': dynamit.model_step_2
    }

    print("Fitting model ", args.model.upper(), "...")
    model = lmfit.Model(
        model_dict[args.model], independent_vars=['t', 'in_func'])

    amp1 = 0.05
    extent1 = 20
    amp2 = 0.01
    extent2 = 170
    # weights = 1.0/np.power(0.1*data_dict[args.tis]+1000, 2.0)
    res2 = model.fit(data_dict[args.tis], t=data_dict[args.t],
                     in_func=data_dict[args.inp],
                     amp1=amp1, extent1=extent1,
                     amp2=amp2, extent2=extent2)
    print("...done!")
    lmfit.report_fit(res2)
    best_fit = dynamit.model_step_2(res2.best_values['amp1'],
                                    res2.best_values['extent1'],
                                    res2.best_values['amp2'],
                                    res2.best_values['extent2'],
                                    list(data_dict[args.t]),
                                    list(data_dict[args.inp]))
    print()

    print("Plotting...")
    fig, ax = plt.subplots()
    ax.plot(data_dict[args.t], data_dict[args.tis], 'gx', label=args.tis)
    ax.plot(data_dict[args.t], data_dict[args.inp], 'rx', label=args.inp)
    # ax.plot(t, blood_shift, 'kx', label="Blood shifted")
    # ax.plot(t, best_fit, 'g-', label="Fit STEP1")
    ax.plot(data_dict[args.t], best_fit, 'k-', label="Fit")
    # ax.plot(t, best_fit3, 'b-', label="Fit PATLAK")
    plt.legend()
    plt.grid(visible=True)
    plt.show()
    print("... done!")


if __name__ == "__main__":
    if sys.argv[1] == 'roi_means':
        roi_means()
    elif sys.argv[1] == 'tac_fit':
        tac_fit()
