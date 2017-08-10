#!/usr/bin/env python3

###############################################################################
# Imports                                                                     #
###############################################################################

import json
import os
import subprocess
import shutil


###############################################################################
# Constants                                                                   #
###############################################################################

setup_filepath = "setup.json"
required_keys = "name", "repo", "location"

pkgs_dir = "pkgs"

pkgs_filepath = os.path.join(pkgs_dir, "pkgs")
ignore_pkgs_filepath = os.path.join(pkgs_dir, "ignore_pkgs")
python_pkgs_filepath = os.path.join(pkgs_dir, "python_pkgs")

SEP = "{:*^30}".format("")


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


class Package(object):

    def __init__(self, pkg_name):
        super(Package, self).__init__()
        self.pkg_name = pkg_name

    def is_installed(self):
        return subprocess.check_output(["dpkg", "-s", self.pkg_name])

    def install(self):
        subprocess.call(["sudo", "apt", "install", self.pkg_name])

    def title(self):
        title_parts = [SEP, "{:*^30}".format(" " + self.pkg_name + " "), SEP]
        return "\n".join(title_parts)

    def ensure(self):
        print()
        print(self.title())
        if not self.is_installed():
            self.install()
        else:
            print("Skipping: already installed!".format(self.pkg_name))


class PythonPackage(Package):

    def __init__(self, pkg_name):
        super(PythonPackage, self).__init__(pkg_name)

    def is_installed(self):
        try:
            import self.pkg_name
            return True
        except ImportError:
            return False

    def install(self):
        subprocess.call(["sudo", "pip3", "install", self.pkg_name])


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


def read_pkgs_file(filepath):
    with open(filepath) as pkgs_file:
        return [line.rstrip() for line in pkgs_file]


###############################################################################
# Worker functions                                                            #
###############################################################################

def update_pkgs():
    subprocess.call(["sudo", "apt", "update"])
    subprocess.call(["sudo", "apt", "upgrade"])


def install_pkgs():

    # sanity check: gitpython required to install pkgs
    PythonPackage("gitpython").ensure()

    # do a general update first, to avoid unnecessary work
    update_pkgs()

    pkgs = read_pkgs_file(pkgs_filepath)
    ignore_pkgs = read_pkgs_file(ignore_pkgs_filepath)

    install_set = set(pkgs) - set(ignore_pkgs)

    for pkg in install_set:
        Package(pkg).ensure()


def install_python_pkgs():

    # sanity check: pip is required to install python pkgs
    Package("python3-pip").ensure()

    for pkg in read_pkgs_file(python_pkgs_filepath):
        PythonPackage(pkg).ensure()


def install_repos():
    repo_dicts = read_json_file(setup_filepath)
    repos = [SetupRepo.of(repo_dict) for repo_dict in repo_dicts if repo_dict["enabled"]]

    for repo in repos:
        try:
            repo.unpack()
        except git.exc.GitError as err:
            print(err)


###############################################################################
# Main script                                                                 #
###############################################################################

def main():

    install_python_pkgs()
    install_pkgs()
    install_repos()


if __name__ == '__main__':
    main()
