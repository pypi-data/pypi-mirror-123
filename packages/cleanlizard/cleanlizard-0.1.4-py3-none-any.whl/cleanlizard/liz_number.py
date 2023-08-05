import os
import pandas as pd
import logging


def validate(x, sort_criteria=['species', 'toes', 'sex', 'initialCaptureDate', 'smallest_svl'],
             validation=['year_diff <= 7', 'svl_diff >= -2']):
    """
    Takes a pandas data frame and creates a new column in the data set populated by the number 1.  It trims the df so
    that to only retains those rows for which validation criteria are satisfied. Validate then groups by sort_criteria,
    produces the minimum value for tmp in each group before assigning the cummulative sum as the new tmp value in each
    row. It produces df of rows containing non-unique individuals as well as counts of unvalidated and validated rows in
    the original df.  Validate uses merging to assign the cummulative sums as liznumber in the original data set
    It then drop 'tmp' and 'smallest_svl, prints summary results, and returns a dict of the original df, and counts of
    validated and unvalidated rows in a dict.

    :type validation: list
    :param x: 
    :param sort_criteria: 
    :param validation: 
    :return: 
    """
    # Drop liznumber if it already exists in x
    if 'liznumber' in x.columns:
        x = x.drop('liznumber',1)
    # Create a new column in the data set populated by the number 1
    x['tmp'] = 1
    # Trim so that we only retain those rows for which validation criteria are satisfied. Group by sort_criteria and
    # produce the minimum value for tmp in each group. Assign the cumulative sum as the new tmp value in each row.
    numbers = x.loc[(x.year_diff <= 7) & (x.svl_diff >= -2), :]. \
        groupby(sort_criteria).tmp.min().cumsum().reset_index()
    # Rename last column to liznumber
    numbers = numbers.rename(columns={'tmp': 'liznumber'})
    # the next line merges the numbers to the original data frame to assign the lizard number to the full record
    # of an animal.  It then drop 'tmp', since we won't be using this again
    x = x.merge(numbers, 'left', on=sort_criteria).drop(['tmp'], 1)
    # Produce the a df of rows which passed validation criteria (i.e. non-unique individuals)
    not_val_df = x.loc[~((x.year_diff <= 7) & (x.svl_diff >= -2)), :]
    # Produce counts of unvalidated and validated rows
    not_validated_count = not_val_df.shape[0]
    # print summary results
    logging.info("\nOf those entries we can handle, there are {} individuals as defined by {} which pass validation based\
    on {} and {} rows which do not pass validation.".format(x.liznumber.max(), sort_criteria, validation,
                                                            not_validated_count))
    # Return dict of the original df, the number of unvalidated individuals, and the number of validated individuals
    return {'val_data': x, 'n_val_data': not_val_df, 'n_validated': not_validated_count}


def smallest(x, svl_group=['species', 'toes', 'sex', 'initialCaptureDate']):
    """finds svl of animal at date of the initial capture."""
    # To-Do:  Make 'sortable_smallest_svl' into local variable
    if any(x.columns == 'smallest_svl'):
        x = x.drop('smallest_svl', 1)
    sortable_smallest_svl = x.groupby(svl_group).svl.min().reset_index()\
        .rename(index=str, columns={'svl': 'smallest_svl'})
    # sortable_smallest_svl
    x = x.merge(sortable_smallest_svl, how='left', on=svl_group)
    x['svl_diff'] = x.svl - x.smallest_svl
    return x


def mindate(x, sort_criteria=['species', 'toes', 'sex']):
    """
    takes a pandas data frame and returns a dataframe with sorting criteria adds a column containing the earliest date
    at which each unique combination of the sort criteria was sighted. [Requires that the source dataframe,x, has a
    column labeled 'date'.]
    """
    if any(x.columns == 'initialCaptureDate'):
        x = x.drop('initialCaptureDate',1)
    sortable_min_date = pd.DataFrame(x.groupby(sort_criteria).date.min()).\
        rename(index=str, columns={'date': 'initialCaptureDate'}).reset_index()
    x = x.merge(sortable_min_date, how='left', on=sort_criteria)
    x['year_diff'] = x.date.dt.year - x.initialCaptureDate.dt.year
    return x


def lizsort(x, path: str, sort_criteria=['species', 'toes', 'sex'], validation=['date', 'svl'],\
            unsortablefile='unsortable.csv'):
    """
    takes a pandas data frame and returns a pandas data frame with only those values which
    can be evaluated according to given criteria and prints a summary of the files evaluated
    :param path:
    :param sort_criteria:
    :param validation:
    :param unsortablefile:
    """
    # identify lizards with sufficient data to evaluate
    # report on those without sufficient data and save them to a file for later evaluation
    critical = sort_criteria + validation
    unsortable = x.loc[x.loc[:, critical].isnull().any(axis=1)]
    sortable = x.loc[x.loc[:, critical].notnull().all(axis=1)]
    os.chdir(path)
    unsortable.to_csv(unsortablefile)
    logging.info("\nThere were {} entries for which values for one of the critical criteria, ({}), were null.  \
    These entries could not be evaluated and were written out to the file {} for evaluation."
                 .format(unsortable.shape[0], critical, unsortablefile))
    return sortable
