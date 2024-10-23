import numpy as np
import scipy


def _model_step_integrand(tau: float, t: float, amp: float, extent: float,
                          tp: list[float], in_func: list[float]) -> float:
    """Defines the integrand when the input response is a step function.
    The response function is defined on the domain [0, infinty). It has value
    amp on the interval [0, extent), and value 0 on the interval
    [extent, infinity).
    The integrand is the product of the response function evaluated at t-tau
    and the input function evaluated at tau. The input function is interpolated
    linearly between the sampled points.

    Arguments:
    tau     --  The integration variable
    t       --  The time point at which the integral is evaluated
    amp     --  The amplitude of the step function
    extent  --  The length of the step function
    tp      --  The time points of the input function samples
    in_func --  The input function samples

    Return value:
    The integrand evaluated at time point t and integration variable value tau.
    """

    # Compute response function value at t - tau
    if t - tau < extent:
        resp = amp
    else:
        resp = 0.0

    # Return integrand value.
    # Numpy.interp returns an array, which is cast back to a float value.
    return resp * float(np.interp(tau, tp, in_func))


def model_step(amp: float, extent: float, t: list[float],
               in_func: list[float]) -> list[float]:
    """Solves the model where the input response function is assumed to be a
    step function.
    This function calculates the convolution of a sampled input function with
    a step function. The step function has value amp on the interval
    [0, extent) and value 0 on the interval [extent, infinity).
    The convolution is evaluated at the same time points as the sampled
    input function and returned as a list.
    The convolution is performed numerically using scipy.integrate.quad and
    the input function is interpolated linearly between sample points.

    Arguments:
    amp     --  The amplitude of the step function.
    extent  --  The length of the step function.
    t       --  The time points of the input function samples.
    in_func --  The input function samples.

    Return value:
    A list containing the modeled values at each time point.
    """

    res = []
    for ti in t:
        # For each time point the integrand (see above) is integrated.
        # We use a higher subproblem limit and higher error tolerances to avoid
        # running into problems, since the functions are not necessarily very
        # well-behaved.
        y = scipy.integrate.quad(_model_step_integrand, 0, ti,
                                 args=(ti, amp, extent, t, in_func),
                                 limit=100,
                                 epsabs=1e-2, epsrel=1e-4)
        res.append(y[0])
    return res


def _model_step_2_integrand(tau: float, t: float,
                            amp1: float,
                            extent1: float,
                            amp2: float,
                            extent2: float,
                            tp: list[float], in_func: list[float]) -> float:
    """Defines the integrand when the input response is a 2-step function.
    The response function is defined on the domain [0, infinty). It has value
    amp1+amp2 on the interval [0, extent1), value amp2 on the interval
    [extent1, extent2) and value 0 on the interval [extent2, infinity).
    The integrand is the product of the response function evaluated at t-tau
    and the input function evaluated at tau. The input function is interpolated
    linearly between the sampled points.

    Arguments:
    tau     --  The integration variable.
    t       --  The time point at which the integral is evaluated.
    amp1    --  The amplitude of the step function on [0, extent1).
    extent1 --  The length of the first step function.
    amp2    --  The amplitude of the step function on [extent1, extent2).
    extent2 --  The length of the second step function.
    tp      --  The time points of the input function samples.
    in_func --  The input function samples.

    Return value:
    The integrand evaluated at time point t and integration variable value tau.
    """

    # Compute response function value at t - tau
    if t - tau < extent1:
        resp = amp1 + amp2
    elif t - tau < extent2:
        resp = amp2
    else:
        resp = 0.0

    # Return integrand value.
    # Numpy.interp returns an array, which is cast back to a float value.
    return resp * float(np.interp(tau, tp, in_func))


def model_step_2(amp1: float,
                 extent1: float,
                 amp2: float,
                 extent2: float,
                 t: list[float],
                 in_func: list[float]) -> list[float]:
    """Solves the model where the input response function is assumed to be a
    2-step function.
    This function calculates the convolution of a sampled input function with
    a 2-step function. The step function has value amp1+amp2 on the interval
    [0, extent1), value amp2 on the interval [extent1, extent2) and value 0 on
    the interval [extent2, infinity).
    The convolution is evaluated at the same time points as the sampled
    input function and returned as a list.
    The convolution is performed numerically using scipy.integrate.quad and
    the input function is interpolated linearly between sample points.

    Arguments:
    amp1    --  The amplitude of the step function on [0, extent1).
    extent1 --  The length of the first step function.
    amp2    --  The amplitude of the step function on [extent1, extent2).
    extent2 --  The length of the second step function.
    t       --  The time points of the input function samples.
    in_func --  The input function samples.

    Return value:
    A list containing the modeled values at each time point.
    """
    res = []
    for ti in t:
        # For each time point the integrand (see above) is integrated.
        # We use a higher subproblem limit and higher error tolerances to avoid
        # running into problems, since the functions are not necessarily very
        # well-behaved.
        y = scipy.integrate.quad(_model_step_2_integrand, 0, ti,
                                 args=(ti, amp1, extent1, amp2, extent2,
                                       t, in_func),
                                 limit=100,
                                 epsabs=1e-2, epsrel=1e-4)
        res.append(y[0])
    return res


def model_patlak(k: float,
                 v0: float,
                 t: list[float],
                 in_func: list[float]) -> list[float]:
    return [0.0, 0.0, 0.0, 0.0, 0.0]
