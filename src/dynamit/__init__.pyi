import SimpleITK as sitk
from datetime import datetime

# From core.py

class Dynamic:

    image: sitk.Image
    acq_times: list[float]

    def __init__(self, image_in: sitk.Image, acq_times_in: list[float]): ...

    def report(self) -> str: ...

def get_acq_datetime(dicom_path: str) -> datetime: ...

def load_dynamic(dicom_path: str) -> Dynamic: ...

def roi_mean(dyn: Dynamic, roi: sitk.Image) -> dict[int, list[float]]: ...


# From model.py

def model_step(amp: float, extent: float, t: list[float],
               in_func: list[float]) -> list[float]: ...

def model_step_2(amp1: float,
                 extent1: float,
                 amp2: float,
                 extent2: float,
                 t: list[float],
                 in_func: list[float]) -> list[float]: ...