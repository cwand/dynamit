from typing import OrderedDict, Any, Optional

import dynamit


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
