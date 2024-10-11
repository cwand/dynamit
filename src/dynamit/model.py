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


def _model_step_4_integrand(tau: float, t: float,
                            amp1: float,
                            extent1: float,
                            amp2: float,
                            extent2: float,
                            tp: list[float], in_func: list[float]) -> float:
    if t - tau < extent1:
        resp = amp1 + amp2
    elif t - tau < extent2:
        resp = amp2
    else:
        resp = 0.0
    return resp * float(np.interp(tau, tp, in_func))


def model_step_4(amp1: float,
                 extent1: float,
                 amp2: float,
                 extent2: float,
                 t: list[float],
                 in_func: list[float]) -> list[float]:
    res = []
    for ti in t:
        y = scipy.integrate.quad(_model_step_4_integrand, 0, ti,
                                 args=(ti, amp1, extent1, amp2, extent2,
                                       t, in_func),
                                 limit=100,
                                 epsabs=1e-2, epsrel=1e-4)
        res.append(y[0])
    return res
