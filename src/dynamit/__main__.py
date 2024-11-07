import argparse
import sys

import dynamit
import matplotlib.pyplot as plt
import lmfit
import numpy as np
import xmltodict


def main(argv: list[str]):

    print("Starting DYNAMIT1")
    print()

    tasks = {
        'ROIMeans': dynamit.task_roi_means,
        'TACFit': dynamit.task_tac_fit
    }

    # Parse XML input file
    if len(argv) != 1:
        exit("Missing command line argument: path to an XML file.")
    xml_file = open(argv[0], "r")
    task_tree = xmltodict.parse(xml_file.read(), force_list=('task'))
    root = task_tree['dynamit1']

    for task in root['task']:
        tasks[task['@name']](task)

    print("DYNAMIT1 ended!")


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
    main(sys.argv[1:])
