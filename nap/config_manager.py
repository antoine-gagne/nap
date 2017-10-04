#!/usr/bin/env python3

import configparser
import os
import sys

main_path = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(main_path, 'config.ini')
config = configparser.ConfigParser()
config.read(config_path)


def set_default_config():
    config["app"]["db_file"] = "datadb.db"
    config["app"]["edit_launch_command"] = "vi"
    with open(config_path, 'w') as configfile:
        config.write(configfile)


def set_test_config():
    config["app"]["db_file"] = "testdb.db"
    config["app"]["edit_launch_command"] = "fake"
    with open(config_path, 'w') as configfile:
        config.write(configfile)

if __name__ == "__main__":
    if sys.argv[1] == "test":
        set_test_config()
    elif sys.argv[1] == "default":
        set_default_config()