import pandas as pd
import numpy as np
import logging


def label_pattern(x, pat_num, pattern, pat_col='toe_pattern', col='toes'):
    """searches a pandas series for a regex expression, pattern, and replaces with replacement"""
    # To-Do needs to capture when an entry fits multiple patterns and which patterns those are
    try:
        x.loc[(x[col].str.match(pattern)) & (x[pat_col].isnull()), pat_col] = str(pat_num)
    except Exception as e:
        logging.error("No values in f'{col} match f'{pattern} where f'{pat_col} is null")
    return x


def make_str(x):
    assert isinstance(x, pd.Series)
    # convert series to string
    x = x.astype(str)
    # create an index of single-digit numbers
    idx = x.str.len() < 2
    # add a zero to the beginning of those single-digit numbers
    x.loc[idx] = '0' + x.loc[idx]
    return x


def replace_pattern(x, source_col, pattern_b, replacement, action):
    """searches a pandas series for a pattern, in values of source_col and replaces with replacement"""

    tmp_source_col = x[source_col]
    tmp_pattern_b = x[pattern_b]
    tmp_replacement = x[replacement]
    tmp_action = x[action]
    try:
        actionconfig = {'replace': [tmp_source_col.strip().replace(tmp_pattern_b, tmp_replacement)],
                        'save': [tmp_source_col, logging.info(f'{tmp_source_col} needs to be reviewed.')],
                        'ignore': [tmp_source_col, logging.info(f'{tmp_source_col} was ignored.')]}

        res = actionconfig[tmp_action][0]
    except Exception as e:
        logging.error("Replacement failed for {}.".format(tmp_source_col))
        res = tmp_source_col
    return res


def report_pattern(x, pattern_col, pattern_num_col, source_col, report_type):
    """searches a pandas series for a regex expression, pattern, and replaces with replacement"""
    col = x[source_col]
    res = pd.DataFrame()
    print(x[pattern_col].unique())
    for pattern in x[pattern_col].unique():
        try:
            logging.info("report_pattern succeeded for {} - {}.".format(x.loc[x[pattern_col] == pattern,
                                                                              pattern_num_col], pattern))
            res = res.append('{}:\ntoe pattern {}:{}'.format(report_type, pattern, (x[col].str.match(pattern) is True)\
                                                             .sum()))
            print(res)
        except Exception as e:
            logging.error("report_pattern failed for {} - {}.".format(x.loc[x[pattern_col] == pattern,
                                                                            pattern_num_col], pattern))
            # res = res
    return res
