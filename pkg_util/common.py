
###############################################################################
# Imports                                                                     #
###############################################################################

import os
import json
import shutil


###############################################################################
# Constants                                                                   #
###############################################################################

setup_filepath = "setup.json"
required_keys = "name", "repo", "location"


###############################################################################
# Utility functions                                                           #
###############################################################################

def read_json_file(filepath):
    with open(filepath) as json_file:
        return json.load(json_file)


def clear_dir(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)


def yes_no(question):
    reply = input("{} (y/n):".format(question)).lower().strip()
    if reply.startswith("y"):
        return True
    elif reply.startswith("n"):
        return False
    else:
        return yes_no(question)
