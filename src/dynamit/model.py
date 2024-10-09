import numpy as np
import scipy


def _model_step_2_resp(amp: float, extent: float, t: float) -> float:
    if t < extent:
        return amp
    else:
        return 0.0


def _model_step_2_integrand(tau: float, t: float, amp: float, extent: float,
                            tp: list[float], in_func: list[float]) -> float:
    return (_model_step_2_resp(amp, extent, t - tau) *
            float(np.interp(tau, tp, in_func)))


def model_step_2(amp: float, extent: float, t: list[float],
                 in_func: list[float]) -> list[float]:
    res = []
    for ti in t:
        y = scipy.integrate.quad(_model_step_2_integrand, 0, ti,
                                 args=(ti, amp, extent, t, in_func))
        res.append(y[0])
    return res
