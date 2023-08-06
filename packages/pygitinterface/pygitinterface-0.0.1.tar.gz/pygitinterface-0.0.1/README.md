## Git Interface for Python
Welcome to the git repository for the Python-Git Interface. The GitInterface class provides an easy-to-use function set for dealing with the Git Bash from Python.


With GitInterface, you can save yourself from having to repetitively type in git commands. GitInterface makes tasks that require upload/download with git easy to automate using Python. GitInterface provides support for basic git commands with more on the way!

To use this module, you should have the git bash downloaded and a repository setup and ready to be automated. Now you can just import the class and git started.

## Contents
|File            |Description                   |
|---             |---                           |
|README          |this file                     |
|git_interface.py|houses the GitInterface class.|

## Currently Supported git Commands
|Comamnd         |Description                   |
|---             |---                           |
|add			 |add files to staging area	|
|branch			 |create a branch of current branch|
|checkout		 |checkout a branch|
|commit			 |commit changes to local repository|
|pull            |pull updates from remote repository|
|push            |send updates to remote repository |
|rebase			 |rebase branch with another branch|
|status 		 |get the status of the local repository|

## Example
```
from git_interface import GitInterface

g = GitInterface('C:/your_local_repository_path')
g.commit('Bug fixes')
g.push('master')
```
