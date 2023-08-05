import logging
import pandas as pd
import numpy as np
from scipy import stats


def distribution(x):
    """*distribution* takes a series or list of numeric objects, *x*, and returns descriptive stats of x"""
    if isinstance(x, list):
        x = pd.Series(x)
    try:
        n = x.count()
        minimum = x.min()
        maximum = x.max()
        median = x.median()
        siqr = stats.iqr(x) / 2
        mean = x.mean()
        stdev = x.std()
        tmp_dict = {'n': [n], 'minimum': [minimum], 'maximum': [maximum],
                    'median': [median], 'siqr': [siqr], 'mean': [mean],
                    'stdev': [stdev]}
        res = pd.DataFrame().from_dict(tmp_dict)
    except Exception as e:
        nonnumericvalues = []
        for v in x:
            if not (isinstance(v, int) | (isinstance(v, float))):
                nonnumericvalues = nonnumericvalues + [v]
        nonnumericvalues
        if len(nonnumericvalues) > 1:
            grammar = 'values in x are'
        else:
            grammar = 'value in x is'
        logging.error("x must contain only numeric, or NoneType variables:\n x:\n{}\n the following {} non-numeric:\n{}"
                      .format(x, grammar, nonnumericvalues))
        res = None
    return res

def review(x, pretty = True):
    """This function returns the set of unique item types and the set of unique values within a series or list"""
    uniqueTypes = {type(val) for val in x}
    if len(uniqueTypes)>1:
        typeStatus = "Check"
    else:
        typeStatus = "OK"
    uniqueVal = {val for val in x}
    if pretty:
        res = ("Unique types include the following: {}".format(uniqueTypes),
               "Unique values include:{}".format(uniqueVal),typeStatus)
    else:
        res = (uniqueTypes,uniqueVal,typeStatus)
    return res
    