"""Methods to convert data to and from tables (DataFrames)."""


import pandas


def df_to_list(df):
    """Convert a pandas DataFrame values to a list of lists.

    Args:
        df (pandas.DataFrame): A DataFrame to convert to a dictionary.

    Returns:
        list: A list of lists
    """
    return [df[column_name].values.tolist() for column_name in df.columns]


def df_to_dict(df):
    """Convert a pandas DataFrame to a dictionary of lists.
    
    Args:
        df (pandas.DataFrame): A DataFrame to convert to a dictionary.

    Returns:
        dict: A dictionary with the format `{column -> [values]}`.
    """
    return df.to_dict(orient = "list")


def list_to_df(lol, colnames = None, transpose = True):
    """Convert a list of list to a pandas DataFrame.
    
    Args:
        lol (list of lists): 2-dimensional list array to parse to a DataFrame.
            Data is arranged row-wise, see argument `transpose`.
        colnames (list): Column names to set. If given `None`,
            create pseudo names with [col1, col2, ..., coli, ..., coln] notation.
        transpose (bool): Import data column-wise.
    
    Returns:
        pandas.DataFrame

    .. exec_code::
        :caption: Example code:
        :caption_output: Result:

        import miscset
        print(miscset.tables.list_to_df([[1,2,3], ["a","b","c"]]))

    """
    df = pandas.DataFrame(data = lol)
    if transpose:
        df = df.transpose()
    ncols = len(df.columns)
    if colnames is None:
        colnames = [f"col{i+1}" for i in range(ncols)]
    df.columns = colnames
    return df


def dict_to_df(d):
    """Convert a dictionary to a pandas DataFrame.
    
    Args:
        d (dict): A dictionary formatted `{column -> [values]}`.
    
    Returns:
        pandas.DataFrame
    """
    return pandas.DataFrame(data = d)