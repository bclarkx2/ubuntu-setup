#! /usr/bin/env python3

###############################################################################
# Imports                                                                     #
###############################################################################

import os
import stat
import socket


###############################################################################
# Constants                                                                   #
###############################################################################

HOME = os.getenv("HOME")

LOCAL_DIR = os.path.join(HOME, "local")
LOCAL_BIN = os.path.join(LOCAL_DIR, "bin")
LOCAL_DOTFILES = os.path.join(LOCAL_DIR, "dotfiles")


###############################################################################
# Helper functions                                                            #
###############################################################################

def ensure_dir(directory):
    os.makedirs(directory, exist_ok=True)


def make_executable(filepath):
    st = os.stat(filepath)
    os.chmod(filepath, st.st_mode | stat.S_IEXEC)


def make_all_local_dirs():
    ensure_dir(LOCAL_DIR)
    ensure_dir(LOCAL_BIN)
    ensure_dir(LOCAL_DOTFILES)


def local_pwd():

    hostname = socket.gethostname()

    script = """\
#! /usr/bin/env bash

~/bin/short_pwd.py "{}"
"""\
        .format(hostname)

    filename = "short_pwd.py"
    filepath = os.path.join(LOCAL_BIN, filename)

    with open(filepath, 'w') as pwd_file:
        pwd_file.write(script)

    make_executable(filepath)


def local_bash_vars():

    filename = ".bash_variables"
    filepath = os.path.join(LOCAL_DOTFILES, filename)

    open(filepath, 'w').close()


###############################################################################
# Main script                                                                 #
###############################################################################

def main():

    make_all_local_dirs()
    local_pwd()
    local_bash_vars()


if __name__ == '__main__':
    main()
