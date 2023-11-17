"""
This module is where we put the helpers that are used by multiple other modules.
"""
import traceback
import introcs
import os, sys


def data_for_file(filename):
    """
    Returns the 2-dimensional table for the given CSV file.
    
    CSV files should have a header with attributes.  The header COMMENTS is ignored.
    All other attributes are kept and should have numeric values.
    
    Parameter filename: The file to parse
    Precondition: filename is a name of a CSV file.
    """
    try:
        if filename is None:
            return None
        
        table = introcs.read_csv(filename)
        
        # Is there a column called COMMENTS?
        header = list(map(lambda x: x.lower(), table[0]))
        pos = header.index('comments') if 'comments' in header else len(header)
        contents = []
        for row in table[1:]:
            point = row[:pos]+row[pos+1:]
            contents.append(tuple(map(float,point)))
        
        return contents
    except:
        traceback.print_exc()
        raise AssertionError('%s is not a valid dataset' % repr(filename))


def list_csv(directory,suffix=None):
    """
    Returns the list of CSV files in a directory.

    The optional suffix attribute is used to separate 2d CSV files from other,
    more general files.

    Parameter directory: The directory path
    Precondition: directory is a string and valid path name

    Parameter suffix: The suffix BEFORE the .csv extension.
    Precondition: suffix is a string
    """
    result = []
    for item in os.listdir(directory):
        pair = os.path.splitext(item)
        if pair[1] == '.csv':
            if not suffix:
                result.append(pair[0])
            elif pair[0].endswith(suffix):
                result.append(pair[0][:-len(suffix)])
    result.sort()
    return result
