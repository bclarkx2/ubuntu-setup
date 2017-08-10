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

def pkg_update_list(folder, pkg_file):
    current = pkg.read_pkgs(folder, pkg_file)
    new = pkg.installed_pkgs()

    update = list(set(current + new))
    return update


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("folder",
                        choices=available_folders)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--dry-run",
                       action="store_true")
    group.add_argument("--new",
                       action="store_true")

    return parser.parse_args()


###############################################################################
# Main script                                                                 #
###############################################################################

def main():
    args = get_args()

    update_list = pkg_update_list(args.folder, pkg.PKGS)
    current_pkgs = pkg.read_pkgs(args.folder, pkg.PKGS)

    if args.dry_run:
        for pack in update_list:
            print(pack)
    elif args.new:
        new_list = list(set(pkg.installed_pkgs()) - set(current_pkgs))
        for pack in new_list:
            print(pack)
    else:
        pkg.set_pkgs(args.folder, pkg.PKGS, update_list)


if __name__ == '__main__':
    main()
