[![Build Status](https://travis-ci.org/ritikmishra/talon-slack-utils.svg?branch=master)](https://travis-ci.org/ritikmishra/talon-slack-utils)
# Team 2502 Slack Utils

Some useful slack utils

### Includes

* Fun \(The /think endpoint)

* BitCoin data \(the /exchange endpoint)


Dependencies inside `runtime.txt`

Designed to run on Heroku

### Setup

`sh sudoless_setup.sh`

This command will install nodejs, pip, and all the requirements onto a mac with limited privileges (i.e school macs). Otherwise, install nodejs in the manner best for your platform, and run
`pip install -r requirements.txt`

### PyCharm setup

`sudoless_setup.sh` installs your modules to a folder in your home directory. PyCharm doesn't know that. To make sure that it knows where all the modules are, complete the following steps:

1. Navigate to Preferences -> Project: talon-slack-utils -> Project Interpreter -> the ellipsis next to the dropdown -> more -> the flowchart-y symbol to the right of the funnel at the bottom of the new window -> plus sign. In the event that Project: talon-slack-utils doesn't show up, open talon-slack-utils in a new window all on its own and try again.

2. now navigate to `/Users/yourstudentid/python_packages` and click ok

3. done
