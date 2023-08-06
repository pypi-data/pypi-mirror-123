"""
This file is part of Git-Python-Interface which is released under the MIT License.
See file LICENSE.txt or go to https://github.com/jocon15/Git-Python-Interface/blob/master/LICENSE for full license details.
"""
import subprocess


class GitInterface:

    def __init__(self, cwd, repo_cite='github'):
        self.repo_cite = repo_cite
        self.cwd = cwd

    def add(self, tag='-A'):
        # can be file or a switch
        tag = str(tag)
        if not tag:
            raise Exception('Please enter a file name or a switch')
        self._create_process(['git', 'add', tag])

    def branch(self, src_branch_name, dst_branch_name):
        src_branch_name = str(src_branch_name)
        dst_branch_name = str(dst_branch_name)
        if not src_branch_name:
            raise Exception('Please enter a branch name.')
        if not dst_branch_name:
            raise Exception('Please enter a new branch name.')
        self._create_process(
            ['git', 'branch', src_branch_name, dst_branch_name])

    def checkout(self, branch_name):
        branch_name = str(branch_name)
        if not branch_name:
            raise Exception('Please enter a branch name')
        self._create_process(['git', 'checkout', branch_name])

    def commit(self, message=None):
        message = str(message)
        self._create_process(['git', 'commit', '-m', f'{message}'])

    def pull(self, branch_name):
        if not branch_name:
            self._create_process(['git', 'pull', self.repo_cite, branch_name])
        else:
            self._create_process(['git', 'pull'])

    def push(self, branch_name):
        if branch_name:
            self._create_process(['git', 'push', self.repo_cite, branch_name])
        else:
            self._create_process(['git', 'push'])

    def rebase(self, rebase_branch_name):
        rebase_branch_name = str(rebase_branch_name)
        if not rebase_branch_name:
            raise Exception('Please enter a branch name')
        self._create_process(['git', 'rebase', rebase_branch_name])
        raise NotImplementedError

    def status(self):
        self._create_process(['git', 'status'])

    def _create_process(self, args):
        """Create subprocess from args"""
        if type(args) != list:
            raise Exception('Args must be a list.')
        if not args:
            raise Exception('No args passed.')
        subprocess.Popen(args, cwd=self.cwd, shell=False)
