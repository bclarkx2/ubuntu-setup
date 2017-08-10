#!/usr/bin/env python3

###############################################################################
# Imports                                                                     #
###############################################################################

from setup import SetupRepo
import pkg_util.common as comm


###############################################################################
# Helper functions                                                            #
###############################################################################

def displayStatus(status):
    if status:
        return "Dirty"
    else:
        return "Clean"


###############################################################################
# Main script                                                                 #
###############################################################################

def main():
    repo_dicts = comm.read_json_file(comm.setup_filepath)
    repos = SetupRepo.list_from(repo_dicts)

    for repo in repos:
        print("{:10s} : {:50.50s} : {:5s}".format(repo.name, repo.location, displayStatus(repo.status())))


if __name__ == '__main__':
    main()
