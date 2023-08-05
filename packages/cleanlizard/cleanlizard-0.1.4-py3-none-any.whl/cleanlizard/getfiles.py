
import pandas as pd
import numpy as np
import os


def xlcolshape(file, verbose=True):
    """xlcolshape takes a file name as a string and returns the shape of the excel file"""
    assert isinstance(verbose, bool), "'verbose' must be bool not,{}".format(type(verbose))
    dictionary = {}
    for sheet in pd.ExcelFile(file).sheet_names:
        try:
            tmp = pd.read_excel(file, sheet_name=sheet).shape
            dictentry = file + '_' + sheet
            dictionary[dictentry] = tmp
            if verbose == True:
                logging.info("Doing stuff you asked me to do for file \'{}\',sheet \'{}\' programmer person." \
                      .format(file, sheet))
        except:
            logging.info("This didn't work for file {}, sheet {}".format(file, sheet))

    return dictionary


def xluniquecol2(file, header = 0, verbose=True):
    tmp = []
    for sheet in pd.ExcelFile(file).sheet_names:
        if (('species' in pd.read_excel(file,sheet_name=sheet, header = header).columns)\
            or('Species' in pd.read_excel(file,sheet_name=sheet, header = header).columns)):
            try:
                tmp = list(set(tmp+list(pd.read_excel(file,sheet_name=sheet).columns)))
                if verbose==True:
                    logging.info("Doing stuff you asked me to do for file \'{}\',sheet \'{}\' programmer person."\
                          .format(file,sheet))
                res = tmp
            except:
                logging.warning("This didn't work for file {}, sheet {}".format(file,sheet))
        else:
            logging.info("Check columns for file {}.".format(file))
            res = None
    return res

def colmatchtodict(x,series, dictsource, key= None):
    """This takes a string, x, and a looks for values in a series that match that contain that string.
    Those values which match are returned as values in a python dict for the key, key."""
    assert isinstance(series,pd.Series)
    if key is None:
        key = x
    tmp = series[series.astype(str).str.contains(x,case = False)].tolist()
    dictsource[key] = tmp
    return dictsource

def findsyn (name,dictionary, verbose = True):
    """
    *findsyn* checks searches the values of the dict *dictionary* for the string, *name* and returns
    the key for the key,value pair to which *name* belongs.
    """
    tmp = pd.DataFrame({'preferredcol':list(dictionary.keys()),'synonymns':list(dictionary.values())})
    try:
        res = list(tmp.preferredcol[tmp.synonymns.apply(lambda x:name in x)])[0]
    except:
        res = None
        if verbose == True:
            logging.warning("No value matching \"{}\" was found in the dictionary.".format(name))
    return res

def readnsplit(file,newsourcefolder,dtype=None,verbose=True):
    """
    This function reads an excel file, splits its sheets into separate files and saves them to folder
    *newsourcefolder*.
    """
    suffix = '.'+file.split('.')[1]
    prefix = file[:-len(suffix)]
    for sheet in pd.ExcelFile(file).sheet_names:
        try:
            splitfile = newsourcefolder+'/'+prefix+'_'+sheet+suffix
            pd.read_excel(file,dtype=dtype, sheet_name=sheet).to_excel(splitfile,index=False)
            if verbose==True:
                logging.info("Succes!  \'{}\',sheet \'{}\' has been saved to {} and the corresponding\
                google drive file as {}.".format(file,sheet,newsourcefolder,splitfile))
            continue
        except:
            logging.warning("Unable to save \'{}\',sheet \'{}\' as a separate file.".format(file,sheet))

def mapndrop(df,dictionary,verbose=True):
    """
    This function renames columns in *df* deemed synonymous according to a dict,
    *dictionary*, and drops unnecessary columns before returning the cleaner dataframe.
    """
    try:
        df.columns = pd.Series(df.columns).map(lambda x:dictionary[x])
        tmp = df
        if verbose==True:
            logging.info("Successfully mapped columns for df.")
        dropidx =[None==col for col in list(tmp.columns)]
        tmp=tmp.drop(columns=df.columns[dropidx])
        if verbose==True:
            logging.info("Successfully dropped unnecessary columns for df.")
    except:
        tmp = None
        logging.warning("Skipping mapndrop call for df.")
    return tmp

def readnclean(x, dictionary, dtype=None):
    """
    This function reads an excel file, renames columns deemed synonymous according to a dict,
    *dictionary*, and drops unnecessary columns before returning the cleaner dataframe.
    """
    tmp = pd.read_excel(x, dtype=dtype)
    tmp.columns = pd.Series(tmp.columns).map(lambda x: dictionary[x])
    dropidx = [None == col for col in list(tmp.columns)]
    tmp = tmp.drop(columns=tmp.columns[dropidx])

    return tmp
