import os
from shutil import which
from subprocess import PIPE, Popen
from typing import List

from how_about_no.core import BaseVCS, VCSException


def get_git_executable_name():
    """Return the name of the Git executable file."""
    return "git" if os.name == "posix" else "git.exe"


class Git(BaseVCS):
    """Git VCS implementation."""

    def __init__(self):
        super().__init__()

        self._exec_name = get_git_executable_name()

    def get_current_branch_name(self) -> str:
        """Return the name of the current Git branch.

        Returns:
            (str): The name of the current branch.

        Raises:
            (VCSException): When it's not possible to fetch the name
                of the current branch.
        """
        error_msg = "It's not possible to fetch the name of the current branch."

        try:
            with Popen(
                [self._exec_name, "branch", "--show-current"], stdout=PIPE
            ) as child:
                output = child.communicate()
                if child.returncode == 0:
                    return output[0].decode("utf-8").strip()

            self._logger.error(error_msg)
            raise VCSException(error_msg)
        except (IndexError, AttributeError) as error:
            self._logger.error(error_msg)
            raise VCSException(error_msg) from error

    def get_list_of_changed_files(self, branch_name: str) -> List[str]:
        """
        Return the list of all files that changed compared to a branch with the given
        name.

        Arguments:
            branch_name (str): The name of the branch to compare.

        Returns:
            (str): The name of the current branch.

        Raises:
            (VCSException): When it's not possible to fetch the list of changed
                files.
        """
        error_msg = "It's not possible to fetch the list of changed files."

        try:
            with Popen(
                [self._exec_name, "diff", branch_name, "--name-only"], stdout=PIPE
            ) as child:
                output = child.communicate()
                if child.returncode == 0:
                    return output[0].decode("utf-8").strip().split("\n")

            self._logger.error(error_msg)
            raise VCSException(error_msg)
        except (IndexError, AttributeError) as error:
            self._logger.error(error_msg)
            raise VCSException(error_msg) from error

    def _is_git_executable_available(self) -> bool:
        """Check whether or not the Git executable exists in the system."""
        return which(self._exec_name) is not None

    def _is_current_directory_a_git_repository(self) -> bool:
        """Check if the current directory is a Git repository."""
        with Popen(
            [self._exec_name, "rev-parse", "--is-inside-work-tree"], stdout=PIPE
        ) as child:
            child.communicate()
            return child.returncode == 0

    def validate(self) -> None:
        """
        Check if the `git` executable is reachable and that the working directory holds
        a Git repository.
        """
        if not self._is_git_executable_available():
            raise VCSException("Git executable is not available in the system PATH.")

        if not self._is_current_directory_a_git_repository():
            raise VCSException(
                "Current directory does not seem to be a Git repository."
            )


VCS = Git
