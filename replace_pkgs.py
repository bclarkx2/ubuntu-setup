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
    parser.add_argument("folder",
                        choices=available_folders)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--dry-run",
                       action="store_true")
    return parser.parse_args()


###############################################################################
# Main script                                                                 #
###############################################################################

def main():
    args = get_args()

    installed = pkg.installed_pkgs()

    if args.dry_run:
        for pack in installed:
            print(pack)
    else:
        pkg.set_pkgs(args.folder, pkg.PKGS, installed)


if __name__ == '__main__':
    main()
