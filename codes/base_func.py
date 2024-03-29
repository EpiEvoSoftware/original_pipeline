import json, os, argparse
from error_handling import CustomizedError

def read_params(path_config, default_config):
    """
    Reads configuration parameters from JSON files and merges with default parameters defined in he template dictionary.

    Parameters:
        path_config (str): Full path to configuration file.
        default_config (str): Relative path to the template (e.g., "base_params.json", "slim_only_template.json")
    """
    # Read default template
    default_config = open(os.path.join(os.path.dirname(__file__), default_config), "r")
    default_param_dict = json.loads(default_config.read())
    # Read the user defined parameters
    config = open(path_config, "r")
    usr_param_dict = json.loads(config.read())
    # Update the template with user information
    default_param_dict.update(usr_param_dict)

    return default_param_dict

def read_params_simonly(path_config):
    # Remeber to get rid of
    default_config = open(os.path.join(os.path.dirname(__file__), "slim_only_template.json"), "r")
    pass


def str2bool(v):
    """
    Returns boolean value represented by the given str / bool.

    Parameters:
        v (str / bool): A string representing the boolean value.
    """
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    raise argparse.ArgumentTypeError('Boolean value expected.')

def dump_json(json2dump):
    """
    Writes a JSON object to the SLiM config file.

    Parameters:
        json2dump: A dictionary rerpesenting the JSON object to be dumped.
    """
    out_config_path = os.path.join(json2dump["BasicRunConfiguration"]["cwdir"], "params.json")
    with open(out_config_path, 'w') as out_config:
        json.dump(json2dump, out_config, indent = 4)

def check_config(config_dict):
    pass








