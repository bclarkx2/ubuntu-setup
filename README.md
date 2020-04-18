# ubuntu-setup
Tool to quickly put a Debian-family Linux install into a usable, handy state.

If you can't throw your laptop off a bridge and have your new workstation fully
configured by the time the laptop hits the water, then you need this tool.


## Getting Started 

### Pre-reqs
In order to run this tool, you will need a machine with the following
characteristics:
- Uses `apt` and `snap` for package management
- Has `bash` installed
- The ability to clone from Github over SSH


### Installation
Clone this repository:

`git clone git@github.com:bclarkx2/ubuntu-setup`


## Usage
See the help menu for a description of the command line flags:

`./setup --help`

Edit the files in the various subdirectories if you want to customize what is
available to be installed.

Execute the setup script. Here is a sample command:

`./setup --interactive`



## Built With
Version 2 of this tool is written in bash (version 1 was a clunky Python
mess).


## Versioning
Versioning strategy: [SemVer](http://semver.org/)

For the versions available, see the [tags on this repository](https://github.com/bclarkx2/ubuntu-setup/tags).


## Authors
* **Brian Clark** - Primary author


## License 
This project is licensed under the MIT license - see the
[LICENSE.md](LICENSE.md) for details.


## Acknowledgements
Shout out to the [Google shell
guide](https://google.github.io/styleguide/shellguide.html)!

