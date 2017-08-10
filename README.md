# ubuntu-setup
Quick Debian-family Linux setup

**setup.py:**
Tool to quickly put a Debian-family install into a usable, handy state.

**Setup procedure:**
* Execute setup.py
* This script may require user input
   * You may have to provide sudo credentials
   * If one of the repos in setup.json is slated to install to an existing directory, then it will prompt you to confirm

**Customize:**
* setup.json
* List of git repos to install
   * Each repo has the following attributes. [] indicates required.
      * [name]: the name of the git repo
      * [repo]: the URL for the git repo
      * [location]: the location on the local machine to clone the repo
      * script: the path to a script (relative to the repo root) that should be executed after the repo is cloned
      * enabled: whether this repo should be installed
   * Notes
      * Any repos listed in setup.json will recursively install all submodules and check out the master branch
      * If any git errors occur, the error will simply print to stdout and the script will skip to the next repo
* pkgs
   * Each file in the pkgs directory is a newline delimited list of packages
   * files:
      * pkgs: List of apt packages to be installed
      * ignore_pkgs: List of apt packages to ignore, even if it appears in pkgs
      * python_pkgs: List of pip3 packages to install
   * Notes
      * The package install list is: set(pkgs) - set(ignore_pkgs)
      * You may use the convenience script below to edit the contents of these files, or you can do it by hand.
* current_pkg_files
   * writes files installed using apt to stdout
* replace_pkgs.py
   * modify the contents of pkgs to reflect exactly the packages installed on your computer
* update_pkgs.py
   * update the contents of pkgs to reflect the union of what was already there and the set of packages returned by current_pkgs_files
