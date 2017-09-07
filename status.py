#!/usr/bin/env python3

###############################################################################
# Imports                                                                     #
###############################################################################

from setup import SetupRepo
import pkg_util.common as comm
import argparse


###############################################################################
# Constants                                                                   #
###############################################################################

STATUS_FMT_STRING = "{:10s} : {:50.50s} : {:5s}"
ORIGIN = "origin"


###############################################################################
# Actions                                                                     #
###############################################################################

def status():
    repos = get_repos()

    for repo in repos:
        print(STATUS_FMT_STRING
              .format(repo.name,
                      repo.location,
                      displayStatus(repo.status())))


def update():
    repos = get_repos()

    for repo in repos:
        if comm.yes_no("Update {}?".format(repo.name)):
            git_repo = repo.git_repo()
            remote = git_repo.remote(ORIGIN)
            remote.pull()


###############################################################################
# Helper functions                                                            #
###############################################################################

def displayStatus(status):
    if status:
        return "Dirty"
    else:
        return "Clean"


def get_repos():
    repo_dicts = comm.read_json_file(comm.setup_filepath)
    repos = SetupRepo.list_from(repo_dicts)
    return repos


def get_args():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--update", "-u",
                       action="store_true")
    return parser.parse_args()


###############################################################################
# Main script                                                                 #
###############################################################################

def main():

    args = get_args()

    if(args.update):
        update()
    else:
        status()


if __name__ == '__main__':
    main()
