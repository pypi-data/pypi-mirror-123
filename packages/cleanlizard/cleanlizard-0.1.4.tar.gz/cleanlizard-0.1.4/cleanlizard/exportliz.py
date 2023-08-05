import pandas as pd
def exportliz(df,iterator, lizard = None, prefix = None):
    """creates a filename for each lizards and then saves that lizards data to that filename. 
    Can take a list of lizards or iterate over the entire dataframe"""
    assert isinstance(df,pd.DataFrame), "df must be pandas DataFrame, not {}.".format(type(df))
    assert ((lizard is None) |(isinstance(lizard,list))), "lizard must be Nonetype or list, not {}.".format(lizard)
    assert ((prefix is None) |(isinstance(prefix,str))), "lizard must be Nonetype or str, not {}.".format(lizard)
    assert iterator in df.columns, "iterator must be in df.columns:\n {}".format(df.columns)
    if prefix is None:
        prefix = "File for lizard" 
    suffix = ".csv"
    if lizard is not None:
        assert lizard in df[iterator].unique(), "lizard must be None or contained in df[iterator]."
        filename = prefix + str(lizard) + suffix
        data = df.loc[df[iterator] == lizard]
        data.to_csv(filename)
    else:
        for liz in pd.unique(iterator):
            filename = prefix + str(liz) + suffix
            data = df.loc[df[iterator] == liz]
            data.to_csv(filename)