import SimpleITK as sitk
from datetime import datetime
from typing import Any

# From core.py

def get_acq_datetime(dicom_path: str) -> datetime: ...


# From image.py

def load_dynamic_series(dicom_path: str) \
        -> dict[str, Any]: ...

def resample_series_to_reference(series: list[sitk.Image],
                                 ref: sitk.Image) -> list[sitk.Image]: ...

def series_roi_means(series: list[sitk.Image],
                     roi: sitk.Image) -> dict[int, list[float]]: ...


# From model.py

def model_step(amp: float, extent: float, t: list[float],
               in_func: list[float]) -> list[float]: ...

def model_step_2(amp1: float,
                 extent1: float,
                 amp2: float,
                 extent2: float,
                 t: list[float],
                 in_func: list[float]) -> list[float]: ...

def model_patlak(k: float,
                 v0: float,
                 t: list[float],
                 in_func: list[float]) -> list[float]: ...
