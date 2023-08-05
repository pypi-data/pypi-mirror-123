import numpy as np
import pandas as pd


def appendstr(x, value, connector='', position='end'):
    """
    appends *value* and *x* separated by a *connector* with the position of *val* determined by *position*
    :param x:
    :param value:
    :param connector:
    :param position:
    """
    assert ((isinstance(x, str) | (x is None) | (x != x))), "x must be str type, NoneType or NaN: x is {} type." \
        .format(type(x))
    if ((x != x) | (x is None)):
        x = ''
    assert (isinstance(value, str)), "value must be str type: value is {} type.".format(type(value))
    assert (isinstance(connector, str)) \
        , "connector must be str or None type, not {} type.".format(type(connector))
    assert (isinstance(position, (str, int))), "position must be either str or int type, not {}." \
        .format(type(position))
    if isinstance(position, str):
        assert (position in ['start', 'end']), "If position is str type, it must be either 'start' or 'end'."
        positiondict = {'start': 0, 'end': len(x)}
        position = positiondict[position]
    if isinstance(position, int):
        assert (position in range(0, 1 + len(x))) \
            , "If position is int type, it must be a value in the range 0 through {}.".format(len(x))
    prefix = x[:position]
    suffix = x[position:]
    if len(x) == 0:
        res = value + connector
    else:
        if position == 0:
            res = prefix + value + connector + suffix
        if position == len(x):
            res = prefix + connector + value + suffix
        if (position > 0 & position < 1):
            res = prefix + connector + value + connector + suffix

    return res
