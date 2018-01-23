#! /usr/bin/env python3

###############################################################################
# Imports                                                                     #
###############################################################################

import os
import shutil


###############################################################################
# Helpers                                                                     #
###############################################################################

def remove_subdirectories(base):

    for name in os.listdir(base):

        dirname = os.path.join(base, name)

        if os.path.isdir(dirname):
            shutil.rmtree(dirname)


###############################################################################
# Main script                                                                 #
###############################################################################

def main():

    home = os.environ["HOME"]
    remove_subdirectories(home)


if __name__ == '__main__':
    # main()
    print("running clear directories")
