#!/usr/bin/env python3


###############################################################################
# Imports                                                                     #
###############################################################################

import subprocess
import os


###############################################################################
# Constants                                                                   #
###############################################################################

pkg_list_script = "current_pkg_list"
pkgs_filepath = "pkgs/pkgs"


###############################################################################
# Helper functions                                                            #
###############################################################################

def set_pkgs(pkgs):
    with open(pkgs_filepath, 'w') as pkgs_file:
        for pkg in pkgs:
            pkgs_file.write("{}{}".format(pkg, os.linesep))


def installed_pkgs():
    output = subprocess.check_output(["bash", pkg_list_script])
    output_str = output.decode()
    pkgs = output_str.split("\n")
    return list(filter(bool, pkgs))


def current_pkgs():
    with open(pkgs_filepath) as pkgs_file:
        return [line.rstrip() for line in pkgs_file if line != "\n"]


def update_pkgs():

    current = current_pkgs()
    new = installed_pkgs()

    updated = set(current + new)

    set_pkgs(updated)


###############################################################################
# Main script                                                                 #
###############################################################################

if __name__ == '__main__':
    update_pkgs()
