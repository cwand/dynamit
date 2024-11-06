import SimpleITK as sitk
from datetime import datetime
from typing import Any, Optional, Union, OrderedDict

# From core.py

def get_acq_datetime(dicom_path: str) -> datetime: ...

def shift_time(y: list[float], t: list[float],
               deltat: float) -> list[float]: ...

def save_tac(tac: dict[Union[str, int], list[float]], path: str): ...

def load_tac(path: str) -> dict[str, list[float]]: ...

# From image.py

def load_dynamic_series(dicom_path: str) \
        -> dict[str, Any]: ...

def resample_series_to_reference(series: list[sitk.Image],
                                 ref: sitk.Image) -> list[sitk.Image]: ...

def series_roi_means(series: list[sitk.Image],
                     roi: sitk.Image) -> dict[int, list[float]]: ...

def lazy_series_roi_means(series_path: str,
                          roi_path: str,
                          resample: Optional[str] = ...,
                          labels: Optional[dict[
                              Union[str, int], Union[str, int]]] = ...)\
        -> dict[Union[str, int], list[float]]: ...

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

# From tasks.py

def task_roi_means(task: OrderedDict[str, Any]) -> None: ...