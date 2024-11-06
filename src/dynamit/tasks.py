from typing import OrderedDict, Any
import dynamit


def task_roi_means(task: OrderedDict[str, Any]):

    print("Starting image read and ROI-mean calculation.")

    img_path = str(task['img_path'])
    roi_path = str(task['roi_path'])
    out_path = str(task['out_path'])

    print("Reading images from ", img_path, ".")
    print("Reading ROI image from ", roi_path, ".")
    print("Processing...")
    dyn = dynamit.lazy_series_roi_means(img_path,
                                        roi_path)
    print("... done!")
    print()

    print("Saving images to file ", out_path, ".")
    print("Saving...")
    dynamit.save_tac(dyn, out_path)
    print("... done!")
