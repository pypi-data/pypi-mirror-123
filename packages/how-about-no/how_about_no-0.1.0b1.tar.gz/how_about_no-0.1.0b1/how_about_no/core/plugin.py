import importlib
from abc import ABC
from typing import Union

from how_about_no.core.logger import Logger
from how_about_no.core.vcs import BaseVCS


class BasePlugin(ABC):
    """A base class for the all plugins.

    A plugin can be used in two different ways: checking whether or not the builds
    should be skipped and populating that information further so it can be used in
    external system, eg. CI/CD.

    A basic implementation of a sample plugin can look like this:

        class SamplePlugin(BasePlugin):

            def check(self) -> bool:
                return False

            def populate(self, value: bool) -> None:
                print(value)

    Please note that the engine will gather the results of `check` methods of all
    plugins before deciding whether or not the builds can be skipped, so the value
    passed to method `populate` does not have to be the same as the value returned from
    method `check`.
    """

    def __init__(self, main_branch_name: str, vcs: BaseVCS, **kwargs) -> None:
        """Initialize the plugin.

        Child classes should override this method to validate the configuration or set
        default values for selected configuration options.

        Arguments:
            main_branch_name (str): The name of the main branch.
            vcs (BaseVCS): The Version Control System that should be used in the plugin.
            kwargs: Holds the plugin configuration loaded from the configuration file.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

        self.main_branch_name = main_branch_name
        self.vcs = vcs

        self._logger = Logger.get_logger()

    def check(self) -> bool:
        """Indicate whether or not the builds can be skipped.

        It returns `False` by default as it may not be implemented in a child class, and
        it does not make sense to cancel the builds because of that.

        Returns:
            (bool)
        """
        raise NotImplementedError()

    def populate(self, value: bool) -> None:  # pylint: disable=unused-argument
        """Populate the result of all checks further."""
        raise NotImplementedError()


def load_plugin(
    plugin_name: str, main_branch_name: str, vcs: BaseVCS, **kwargs
) -> Union[BasePlugin, None]:
    """Load the plugin with given name.

    Arguments:
        plugin_name (str): The name of the plugin to import.
        main_branch_name (str): The name of the main branch.
        vcs (BaseVCS): The Version Control System that should be used in the plugin.
        kwargs: Holds the plugin configuration loaded from the configuration file.

    Returns:
        (Union[BasePlugin, None]): The plugin class or None if not loaded for any
            reason.
    """
    try:
        plugin_class = importlib.import_module(plugin_name).PLUGIN
        return plugin_class(main_branch_name=main_branch_name, vcs=vcs, **kwargs)
    except (AttributeError, ImportError, TypeError):
        return None
