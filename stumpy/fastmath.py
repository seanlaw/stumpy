import importlib

import numba
from numba import njit

from . import config


@njit(fastmath=config._STUMPY_DEFAULTS["STUMPY_FASTMATH_FASTMATH._ADD_ASSOC"])
def _add_assoc(x, y):  # pragma: no cover
    """
    A dummy function to test the fastmath module

    Parameters
    ----------
    x : float
        A float value

    y : floatf
        A float value

    Returns
    -------
    out : float
        The ouput valus

    Notes
    -----
    This is taken from the following link:
    https://numba.pydata.org/numba-doc/dev/user/performance-tips.html#fastmath
    """
    return (x - y) + y


def _set(module_name, func_name, flag):
    """
    Set fastmath flag for a given function

    Parameters
    ----------
    module_name : str
        The module name

    func_name : str
        The function name

    flag : set or bool
        The fastmath flag

    Returns
    -------
    None
    """
    module = importlib.import_module(f".{module_name}", package="stumpy")
    func = getattr(module, func_name)
    try:
        func.targetoptions["fastmath"] = flag
        func.recompile()
    except AttributeError as e:
        if numba.config.DISABLE_JIT and (
            str(e) == "'function' object has no attribute 'targetoptions'"
            or str(e) == "'function' object has no attribute 'recompile'"
        ):
            pass
        else:  # pragma: no cover
            raise

    return


def _reset(module_name, func_name):
    """
    Reset the value of fastmath to its default value

    Parameters
    ----------
    module_name : str
        The module name

    func_name : str
        The function name

    Returns
    -------
    None
    """
    key = module_name + "." + func_name
    key = "STUMPY_FASTMATH_" + key.upper()
    default_flag = config._STUMPY_DEFAULTS[key]
    _set(module_name, func_name, default_flag)

    return
