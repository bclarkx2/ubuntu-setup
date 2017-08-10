
###############################################################################
# Imports                                                                     #
###############################################################################

import os
import argparse
import subprocess

###############################################################################
# Constants                                                                   #
###############################################################################

PKGS_DIR = "pkgs"

PKGS = "pkgs"
IGNORE_PKGS = "ignore_pkgs"
PYTHON_PKGS = "python_pkgs"

pkg_list_script = "current_pkg_list"


###############################################################################
# Class definitions                                                           #
###############################################################################

class PkgArgumentParser(argparse.ArgumentParser):

    def __init__(self):
        super(PkgArgumentParser, self).__init__()
        self.add_argument("folders",
                          nargs="*",
                          help="pkgs folders to update")


###############################################################################
# Utility functions                                                           #
###############################################################################

def pkg_file(folder, pkgs_filename):
    return os.path.join(PKGS_DIR, folder, pkgs_filename)


def set_pkgs(folder, pkgs_filename, pkgs):
    with open(pkg_file(folder, pkgs_filename), 'w') as pkgs_file:
        for pkg in pkgs:
            pkgs_file.write("{}{}".format(pkg, os.linesep))


def installed_pkgs():
    output = subprocess.check_output(["bash", pkg_list_script])
    output_str = output.decode()
    pkgs = output_str.split("\n")
    return list(filter(bool, pkgs))


def read_pkgs(folder, pkgs_filename):
    try:
        with open(pkg_file(folder, pkgs_filename)) as pkgs_file:
            return [line.rstrip() for line in pkgs_file if line != "\n"]
    except FileNotFoundError:
        return []
