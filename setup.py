#!/usr/bin/env python3

###############################################################################
# Imports                                                                     #
###############################################################################

import os
import subprocess

import pkg_util.pkg as pkg
import pkg_util.common as comm
from pkg_util.pkg import PkgArgumentParser

try:
    import git
except ImportError:
    print("skipping git import")


###############################################################################
# Constants                                                                   #
###############################################################################

default_folder = "default"

SEP = "{:*^30}".format("")

SCRIPT_DIR = "scripts"


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
        if not all(key in attr_dict for key in comm.required_keys):
            raise ValueError("Missing key!")
        return SetupRepo(attr_dict)

    @staticmethod
    def list_from(repo_dicts):
        return [SetupRepo.of(repo_dict) for repo_dict in repo_dicts if repo_dict["enabled"]]

    def okay_to_write(self):
        if os.path.isdir(self.location):
            return comm.yes_no("Overwrite {}?".format(self.location))
        else:
            return True

    def msg(self, format_str):
        formatted = format_str.format(**self.__dict__)
        print(formatted)

    def unpack(self):

        if not self.okay_to_write():
            self.msg("Skipping {name}")
            return

        comm.clear_dir(self.location)
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

    def status(self):
        return self.git_repo().is_dirty()

    def git_repo(self):
        return git.Repo(self.location)


class Package(object):

    def __init__(self, pkg_name):
        super(Package, self).__init__()
        self.pkg_name = pkg_name

    def is_installed(self):
        returncode = subprocess.call(["dpkg", "-s", self.pkg_name],
                                     stdout=subprocess.DEVNULL,
                                     stderr=subprocess.DEVNULL)
        return returncode == 0

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


###############################################################################
# Helper functions                                                            #
###############################################################################

def checkout_all_submodules_to_master(repo):
    for submodule in repo.submodules:
        checkout_submodule_master(submodule)


def checkout_submodule_master(submodule):
    repo = submodule.module()
    repo.heads.master.checkout()


def build_pkgs_list(folders):
    listed_pkgs = []
    ignore_pkgs = []

    for folder in folders:
        listed_pkgs += pkg.read_pkgs(folder, pkg.PKGS)
        ignore_pkgs += pkg.read_pkgs(folder, pkg.IGNORE_PKGS)

    pkgs = set(set(listed_pkgs) - set(ignore_pkgs))

    return pkgs


###############################################################################
# Worker functions                                                            #
###############################################################################

def update_pkgs():
    subprocess.call(["sudo", "apt", "update"])
    subprocess.call(["sudo", "apt", "upgrade"])


def install_pkgs(pkgs):

    # sanity check: gitpython required to install pkgs
    PythonPackage("gitpython").ensure()

    # do a general update first, to avoid unnecessary work
    update_pkgs()

    for pack in pkgs:
        Package(pack).ensure()


def install_python_pkgs(pkgs):

    # sanity check: pip is required to install python pkgs
    Package("python3-pip").ensure()

    for pypack in pkgs:
        PythonPackage(pypack).ensure()


def install_repos():
    repo_dicts = comm.read_json_file(comm.setup_filepath)
    repos = SetupRepo.list_from(repo_dicts)

    for repo in repos:
        try:
            repo.unpack()
        except git.exc.GitError as err:
            print(err)


def run_scripts():

    scripts = [os.path.join(SCRIPT_DIR, f)
               for f in os.listdir(SCRIPT_DIR)
               if f.endswith(".py")]

    for script in scripts:
        subprocess.call(["python3", script])


def get_args():
    args = PkgArgumentParser().parse_args()

    if not args.folders:
        args.folders = [default_folder]

    return args


###############################################################################
# Main script                                                                 #
###############################################################################

def main():

    args = get_args()

    pkgs, python_pkgs = build_pkgs_list(args.folders)

    install_python_pkgs(python_pkgs)
    install_pkgs(pkgs)
    install_repos()


if __name__ == '__main__':
    main()
