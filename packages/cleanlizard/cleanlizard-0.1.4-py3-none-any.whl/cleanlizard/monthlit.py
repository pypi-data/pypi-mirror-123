import numpy as np


def monthlit(x):
    months = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sept', 10: 'Oct',
              11: 'Nov', 12: 'Dec'}
    if (x is None) | (np.isnan(x)):
        res = x
    else:
        res = months[int(x)]
    return res
