import importlib
from abc import ABC, abstractmethod
from typing import List

from how_about_no.core.logger import Logger


class VCSException(Exception):
    """
    This is an exception that should be raised in case the VCS validation fails.
    """


class BaseVCS(ABC):
    """This is a base class for all Version Control System implementations.

    In order to keep this library generic, it should be possible to use it
    against different Version Control Systems (VCSs). This class provides an
    interface that should be implemented by all child classes and can be used
    in the plugins.
    """

    def __init__(self):
        self._logger = Logger.get_logger()

    @abstractmethod
    def validate(self) -> None:
        """
        Validate whether or not the current repository can be managed by given
        VCS implementation.

        If the validation fails, VCSException should be raised.
        """

    @abstractmethod
    def get_current_branch_name(self) -> str:
        """Return the name of the branch that is currently checked out."""

    @abstractmethod
    def get_list_of_changed_files(self, branch_name: str) -> List[str]:
        """Return a list of all files changed comparing to given branch."""


def load_vcs(vcs_module_path: str) -> BaseVCS:
    """Load and return the version control system from given module.

    Arguments:
        vcs_module_path (str): The path of the VCS module.

    Returns:
        (BaseVCS)

    Raises:
        (VCSException): When it's not possible to load the VCS.
    """
    try:
        return importlib.import_module(vcs_module_path).VCS()
    except (AttributeError, ImportError, TypeError) as ex:
        raise VCSException("Given version control system could not be loaded.") from ex
