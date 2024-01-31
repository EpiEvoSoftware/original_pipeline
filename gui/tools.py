"""
This module is where we put the helpers that are used by multiple other modules.
"""
import traceback
import os, sys

def read_txt(filename):
    try:
        with open(filename, 'r') as file:
            print("success")
        #     lines = file.readlines()
        # # Process each line
        # for line in lines:
        #     # Assuming your data is comma-separated, split the line into parts
        #     parts = line.split(',')
        #     # Now you can process each part as needed
        #     print(parts)
    except FileNotFoundError:
        print("The directory does not exist.")
    except PermissionError:
        print("You don't have permission to access this directory.")
    except Exception as e:
        print(f"An error occurred: {e}")


def list_files(directory):
    """
    Prints out all the files in the specified directory.
    
    :param directory: The path to the directory to list files from.
    """
    try:
        for item in os.listdir(directory):
            full_path = os.path.join(directory, item)
            if os.path.isfile(full_path):
                print(item)
    except FileNotFoundError:
        print("The directory does not exist.")
    except PermissionError:
        print("You don't have permission to access this directory.")
    except Exception as e:
        print(f"An error occurred: {e}")



def data_for_file(filename):
    """
    Returns the 2-dimensional table for the given CSV file.
    
    CSV files should have a header with attributes.  The header COMMENTS is ignored.
    All other attributes are kept and should have numeric values.
    
    Parameter filename: The file to parse
    Precondition: filename is a name of a CSV file.
    """
    raise NotImplementedError("todo implement")


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
    raise NotImplementedError("todo implement")

def edit_params(dir):
    # Step 1: Read the file into a dictionary
    params = {}

    with open('params.config', 'r') as file:
        for line in file:
            key, value = line.strip().split(':', 1)
            params[key] = value.strip()

    # Step 2: Edit or update the dictionary
    params['host_size'] = '2000'  # Example: updating host_size
    params['Infection_rate'] = '0.04'  # Example: updating Infection_rate
    params['new_param'] = 'new_value'  # Example: adding a new parameter

    # Step 3: Write the updated dictionary back to the file
    with open('params.config', 'w') as file:
        for key, value in params.items():
            file.write(f"{key}:{value}\n")
