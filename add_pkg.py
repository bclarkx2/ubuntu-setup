#!/usr/bin/env python3


###############################################################################
# Imports                                                                     #
###############################################################################

import argparse
import os
import pkg_util.pkg as pkg


###############################################################################
# Constants                                                                   #
###############################################################################

available_folders = os.listdir(pkg.PKGS_DIR)


###############################################################################
# Helper functions                                                            #
###############################################################################

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("new_pkg")
    parser.add_argument("folders",
                        choices=available_folders,
                        nargs="*")

    return parser.parse_args()


###############################################################################
# Main script                                                                 #
###############################################################################

def main():
    args = get_args()

    for folder in args.folders:
        pkg.add_pkg(folder, pkg.PKGS, args.new_pkg)


if __name__ == '__main__':
    main()
