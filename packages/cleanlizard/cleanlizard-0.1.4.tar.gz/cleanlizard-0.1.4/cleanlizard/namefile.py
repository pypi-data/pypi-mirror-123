def namefile(name, tzadjust=5,tzdirection = '-', adjprecision='minutes', filetype = 'csv'):
    """takes a filename and filetype, and adds a timestamp adjusted relative to gmt to a precision
    and returns a string that concatenates them."""
    assert isinstance(name,str),"'name' must be of type str."
    assert isinstance(tzadjust,int),"'tzadjust' must be of type int"
    assert adjprecision in ['date','hour','minutes','seconds', 'max'], "'adjprecision' must be either \
    'date', hour','minutes','seconds', or 'max'"
    precision= {'max':None,'seconds':-7,'minutes':-9, 'hours':-14,'date':-20}
    if tzdirection== '-':
        timestamp = (pd.to_datetime('now')-pd.Timedelta(hours=tzadjust))
    else:
        timestamp = (pd.to_datetime('now')+pd.Timedelta(hours=int(tzadjust[1:])))
    timestamp = str(timestamp).replace(':','hrs',1).replace(':','min',1)
    timestamp = timestamp[:precision[adjprecision]]
    filename = name+'_' + timestamp+ '.' +filetype
    return filename
