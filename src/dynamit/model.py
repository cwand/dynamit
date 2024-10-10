import numpy as np
import scipy


def _model_step_2_integrand(tau: float, t: float, amp: float, extent: float,
                            tp: list[float], in_func: list[float]) -> float:
    if t - tau < extent:
        resp = amp
    else:
        resp = 0.0
    return resp * float(np.interp(tau, tp, in_func))


def model_step_2(amp: float, extent: float, t: list[float],
                 in_func: list[float]) -> list[float]:
    res = []
    for ti in t:
        y = scipy.integrate.quad(_model_step_2_integrand, 0, ti,
                                 args=(ti, amp, extent, t, in_func),
                                 limit=100,
                                 epsabs=1e-2, epsrel=1e-4)
        res.append(y[0])
    return res


