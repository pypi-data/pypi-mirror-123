def vocab_run(x, connector_dict={1: None, 2: ' and ', 'run': ', '}):
    """vocab_run takes a list, joins its the first the elements with a separator placing a different separator between
     the penultimate and final members of the list and returns the result as a string
     :param x: a list of strings to be concatenated
     :param connector_dict: a dictionary with keys describing the size of the list and values indicating the type of
     connectors separate the list elements.
    """
    x = [str(el) for el in x]
    if len(x) == 1:
        vocab = x
    else:
        if len(x) == 2:
            vocab = (connector_dict[len(x)]).join(x)
        else:
            connector = connector_dict['run']
            connector_final = connector_dict[2]
            vocab = connector.join(x[:-1])+connector_final+x[-1]
    return vocab
