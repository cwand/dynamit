from typing import OrderedDict, Any, Optional
import dynamit
import lmfit
import matplotlib.pyplot as plt


def task_roi_means(task: OrderedDict[str, Any]):
    """Run the ROIMeans task. Loads an image series and a ROI image, and
    computes mean voxel values for each ROI in each time frame. The result
    is saved to a text file.
    The input to the function is an xml structure, which must have the
    following structure (not ordered):

    <img_path>PATH_TO_IMAGE_SERIES</img_path>
    <roi_path>PATH_TO_ROI_IMAGE_FILE</roi_path>
    <labels>ROI_LABEL_1,NEW_LABEL_1;
            ROI_LABEL_2,NEW_LABEL_2;...</labels> <!-- OPTIONAL -->
    <resample>img_OR_roi</resample> <!-- OPTIONAL -->
    <out_path>PATH_TO_RESULT_FILE</out_path>

    With the <labels>-tag, new labels can be chosen if the ROI-labels in the
    ROI-file are no descriptive.
    The <resample>-tag can be used to resample either the images in the
    series to the ROI image (use the value 'img') or the other way around
    (use the value 'roi'). This is a mandatory input if the two images are
    not in the same physical space.
    """

    print("Starting image read and ROI-mean calculation.")

    # Get the image and output paths
    img_path = str(task['img_path'])
    roi_path = str(task['roi_path'])
    out_path = str(task['out_path'])

    # Create label dictionary
    labels = {}
    if 'labels' in task:
        # This section transforms the string "X,a;Y,b;Z,c" into a dict of the
        # form {'X': 'a', 'Y': 'b', 'Z': 'c'}
        label_string = str(task['labels']).split(';')
        for label in label_string:
            label_split = label.split(',')
            labels[label_split[0]] = label_split[1]

    # Check if resampling is required
    resample: Optional[str] = None
    if 'resample' in task:
        resample = str(task['resample'])

    print("Reading images from ", img_path, ".")
    print("Reading ROI image from ", roi_path, ".")
    print("Processing...")
    # Run the task!
    dyn = dynamit.lazy_series_roi_means(img_path,
                                        roi_path,
                                        resample=resample,
                                        labels=labels)
    print("... done!")
    print()

    print("Saving images to file ", out_path, ".")
    print("Saving...")
    # Save file to disk
    dynamit.save_tac(dyn, out_path)
    print("... done!")


def task_tac_fit(task: OrderedDict[str, Any]):
    """Run the TACFit task. Fits model parameters to a measured TAC. The fit
    is shown in standard out and a figure of the fitted curve and the data is
    shown.
    The input is an xml-structure, which must have the following content (in
    any order):

    <tac_path>PATH_TO_TAC_FILE</tac_path>
    <time_label>LABEL_OF_TIME_DATA</time_label>
    <inp_label>LABEL_OF_INPUT_FUNCTION_DATA</inp_label>
    <tis_label>LABEL_OF_TISSUE_DATA</tis_label>
    <model>FIT_MODEL</model>
    <init>
        <PARAM1>PARAM1_INIT_VALUE</PARAM1>
        <PARAM2>PARAM2_INIT_VALUE</PARAM2>
    </init>

    """

    print("Starting TAC-fitting.")

    # Get the data path
    tac_path = str(task['tac_path'])

    # Get labels of relevant TACs
    inp_label = str(task['inp_label'])
    time_label = str(task['time_label'])
    tis_label = str(task['tis_label'])

    # Get required fit model:
    fit_model = str(task['model'])

    # Load TAC data
    print("Loading TAC-data from", tac_path, "...")
    tac = dynamit.load_tac(tac_path)
    print("... done!")
    print()

    print("Fitting TAC data to model ", fit_model, ".")

    # Dict of possible models
    models = {
        'step2': dynamit.model_step_2,
        'step': dynamit.model_step,
        'patlak': dynamit.model_patlak
    }

    # Put initial parameters into a dict
    init_param = {}
    for param in task['init']:
        init_param[param] = float(task['init'][param])

    # Define model to fit
    model = lmfit.Model(models[fit_model], independent_vars=['t', 'in_func'])
    # Run fit from initial values
    res = model.fit(tac[tis_label], t=tac[time_label],
                    in_func=tac[inp_label],
                    **init_param)
    # Report!
    lmfit.report_fit(res)
    # Calculate besti fitting model
    best_fit = models[fit_model](t=list(tac[time_label]),  # type: ignore
                                 in_func=list(tac[inp_label]),
                                 **res.best_values)

    print("... done!")
    print()

    print("Plotting...")
    fig, ax = plt.subplots()
    ax.plot(tac[time_label], tac[tis_label], 'gx', label=tis_label)
    ax.plot(tac[time_label], tac[inp_label], 'rx', label=inp_label)
    ax.plot(tac[time_label], best_fit, 'k-', label="Fit")
    plt.legend()
    plt.grid(visible=True)
    plt.show()
    print("... done!")
    print()
