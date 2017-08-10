# ubuntu-setup
Quick Debian-family Linux setup

## setup.py
Tool to quickly put a Debian-family install into a usable, handy state.

## Setup procedure
1. Execute setup.py
   * Provide as command line arguments the name of each pkg folder that you wish to install
   * ex: ./setup.py default dev
      * This will install all the packages in both pkgs/default and pkgs/dev
1. This script may require user input
   * You may have to provide sudo credentials
   * If one of the repos in setup.json is slated to install to an existing directory, then it will prompt you to confirm

## Customize
* setup.json
   * List of git repos to install
      * Each repo has the following attributes. [] indicates required.
         * [name]: the name of the git repo
         * [repo]: the URL for the git repo
         * [location]: the location on the local machine to clone the repo
      * script: the path to a script (relative to the repo root) that should be executed after the repo is    cloned
         * enabled: whether this repo should be installed
      * Notes
         * Any repos listed in setup.json will recursively install all submodules and check out the master    branch
         * If any git errors occur, the error will simply print to stdout and the script will skip to the next    repo
* pkgs
   * The pkgs directory is split into folders, each one representing a set of packages that can be installed individually or in combination with other pkg folders
   * Each folder contains the following files:
      * pkgs: List of apt packages to be installed
      * ignore_pkgs: List of apt packages to ignore, even if it appears in pkgs
      * python_pkgs: List of pip3 packages to install
   * Notes
      * The package install list is: set(pkgs) - set(ignore_pkgs)
      * You may use the convenience script below to edit the contents of these files, or you can do it by hand.
* current_pkg_files
   * writes files installed using apt or apt-get to stdout
* replace_pkgs.py [-h] [--dry-run] {available folders}
   * Arguments/options:
      * folder: this argument gives the folder that we should update the pkgs file for
         * Must be one of the available folders in the pkgs directory
      * modify the contents of pkgs to reflect exactly the packages installed on your computer
      * --dry-run: This option will print the list of packages to set, rather than write to file
   * Notes
      * If you want to add packages to multiple folders, you have to run this script once for each folder
* update_pkgs.py [-h] [--dry-run | --new] {available folders}
   * update the contents of pkgs to reflect the union of what was already there and the set of packages returned by current_pkgs_files
   * Arguments/options:
      * folder: this argument gives the folder that we should update the pkgs file for
         * Must be one of the available folders in the pkgs directory
      * --dry-run: print the list of *all* packages that will be set in the folder's pkgs file, rather than write to file
      * --new: print only the currently installed packages that will be *added* to the folder's pkgs file
   * Notes
      * If you want to add packages to multiple folders, you have to run this script once for each folder

## Typical Workflows
1. Add from current install
   1. While using your install, you add a couple packages.
   1. You decide that some of those pacakges would be nice to add to install when setting up a dev station
   1. Navigate to ubuntu-settings
   1. Run `update_packages.py dev --new` to get a list of packages that you have installed locally that are not in the dev folder's pkgs file
      * If you decide to add all the new packages:
         * Run `update_packages.py dev --dry-run` to see the final list of packages that will be written to the dev folder's pkgs folder
         * Run `update_packages.py dev` to overwrite the dev folder's pkgs folder with the updated list
      * If you decide to only add some packages:
         * Manually edit the dev folder's pkgs file to include the desired package
         * Use the output from the `--new` command as reference if you like
   1. Add the changed pkgs files to git
   1. Commit and push changes