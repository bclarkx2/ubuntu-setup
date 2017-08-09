#!/usr/bin/env python3

###############################################################################
# Imports                                                                     #
###############################################################################

import json
import os
import git
import subprocess
import shutil


###############################################################################
# Constants                                                                   #
###############################################################################

setup_filepath = "setup.json"
required_keys = "name", "repo", "location"


###############################################################################
# Class definitions                                                           #
###############################################################################

class SetupRepo(object):

    def __init__(self, attr_dict):
        super(SetupRepo, self).__init__()
        self.__dict__.update(attr_dict)
        self.location = os.path.expanduser(self.location)

    @staticmethod
    def of(attr_dict):
        if not all(key in attr_dict for key in required_keys):
            raise ValueError("Missing key!")
        return SetupRepo(attr_dict)

    def okay_to_write(self):
        if os.path.isdir(self.location):
            return yes_no("Overwrite {}?".format(self.location))
        else:
            return True

    def msg(self, format_str):
        formatted = format_str.format(**self.__dict__)
        print(formatted)

    def unpack(self):

        if not self.okay_to_write():
            self.msg("Skipping {name}")
            return

        clear_dir(self.location)
        repo = git.Repo.clone_from(self.repo, self.location, recursive=True)

        # need to checkout to master
        # TODO allow support for different branches
        if repo.submodules:
            checkout_all_submodules_to_master(repo)

        self.msg("Success! Cloned {name} to {location}")

        if self.script:
            self.msg("Executing script {script}")
            full_script = os.path.join(self.location, self.script)
            subprocess.call([full_script])


###############################################################################
# Helper functions                                                            #
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


def checkout_all_submodules_to_master(repo):
    for submodule in repo.submodules:
        checkout_submodule_master(submodule)


def checkout_submodule_master(submodule):
    repo = submodule.module()
    repo.heads.master.checkout()


###############################################################################
# Main script                                                                 #
###############################################################################

def main():

    repo_dicts = read_json_file(setup_filepath)

    repos = [SetupRepo.of(repo_dict) for repo_dict in repo_dicts if repo_dict["enabled"]]

    for repo in repos:
        try:
            repo.unpack()
        except git.exc.GitError as err:
            print(err)


if __name__ == '__main__':
    main()
