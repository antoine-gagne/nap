"""Utils for functions"""

import os
import configparser

def get_config_object():
    project_path = 'nap/config.ini'
    full_path = os.path.abspath(project_path)
    config = configparser.ConfigParser()
    config.read(full_path)
    return config