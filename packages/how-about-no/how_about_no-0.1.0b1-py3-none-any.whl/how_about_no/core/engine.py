import sys
from typing import List

from how_about_no.core.config import Config
from how_about_no.core.logger import Logger
from how_about_no.core.plugin import BasePlugin, load_plugin
from how_about_no.core.vcs import BaseVCS, load_vcs

RESULT_POLICY_FUNCTIONS = {
    "all": all,
    "any": any,
    "none": lambda values: all(not value for value in values),
}


class Engine:
    """
    Main class executing the checks and populating the value using handlers.
    """

    _plugins: List[BasePlugin] = None
    _vcs: BaseVCS = None

    def __init__(self, configuration: Config):
        """
        Validate whether or not the current working directory is a VCS repository and
        load all plugins defined in the configuration file.
        """
        self._logger = Logger.get_logger()
        self._configuration = configuration

        self._vcs = load_vcs(self._configuration.vcs)
        self._plugins = self._load_plugins(self._configuration.plugins)

    def _load_plugins(self, plugins: dict) -> List[BasePlugin]:
        """Load all plugins.

        Arguments:
            plugins (dict): A dictionary with all defined plugins. The key of each entry
                is the name of the plugin, the value is it's configuration.
        """
        self._logger.debug("Loading plugins started.")

        result = []

        for plugin_name, plugin_configuration in plugins.items():
            plugin = load_plugin(
                plugin_name,
                main_branch_name=self._configuration.main_branch,
                vcs=self._vcs,
                **plugin_configuration,
            )
            if not plugin:
                self._logger.warning("Plugin %s has not been loaded.", plugin_name)
                continue

            result.append(plugin)
            self._logger.debug("Plugin %s has been loaded.", plugin_name)

        self._logger.debug("Loading plugins finished.\n")

        return result

    def _is_current_main_branch(self) -> bool:
        """
        Checks whether or not the current branch in the repository is the main branch.
        """
        return self._vcs.get_current_branch_name() == self._configuration.main_branch

    def _check(self) -> bool:
        """Run the check using all loaded plugins.

        If all plugins decide that the build should be skipped then it will be.

        If the `check` method has not been implemented in a plugin then it will be
        skipped.

        Returns:
            (bool): The result of the check.
        """
        self._logger.debug("Checking all plugins for the output started.")
        result = []

        for plugin in self._plugins:
            try:
                result.append(plugin.check())
            except NotImplementedError:
                self._logger.debug(
                    "Method `check` has not been implemented in plugin %s. Skipping.",
                    plugin.__class__.__module__,
                )

        self._logger.debug("Checking all plugins for the output finished.\n")

        return result

    def _populate_result(self, result: bool) -> None:
        """Populate the result of the check using all loaded plugins.

        If the `populate` method has not been implemented in a plugin then it will be
        skipped.
        """
        self._logger.debug("Populating the result using loaded plugins started.")

        for plugin in self._plugins:
            try:
                plugin.populate(result)
            except NotImplementedError:
                self._logger.debug(
                    "Method `populate` has not been implemented in plugin %s."
                    " Skipping.",
                    plugin.__class__.__module__,
                )

        self._logger.debug("Populating the result using loaded plugins finished.\n")

    def _calculate_result(self, values: List[bool]) -> bool:
        """Calculate the final result.

        The result is calculated based on the result of method `check` from all plugins
        and seleted result policy.

        Arguments:
            values (List[bool]): The results from plugins.

        Returns:
            (bool)

        Raises:
            (SystemExit): When the value of the result policy is incorrect. This should
                not happen unless the Configuration class has been changed.
        """
        result_policy = self._configuration.result_policy
        result_policy_fun = RESULT_POLICY_FUNCTIONS.get(result_policy)
        if not result_policy_fun:
            self._logger.error("Incorrect result policy value: %s", result_policy)
            sys.exit(1)

        result = result_policy_fun(values)

        self._logger.info("The build will %sbe skipped.\n", "" if result else "not ")

        return result

    def process(self) -> None:
        """Run the check using all loaded plugins and optional configuration file."""
        if not self._plugins:
            self._logger.warning(
                "No plugins have been loaded, the build will not be skipped."
            )
            return

        self._logger.debug("Processing started.\n")

        if self._is_current_main_branch():
            # Skip the builds on the main branch if the configuration says so
            result = self._configuration.skip_builds_on_main_branch
            self._logger.debug(
                "The current branch is the main repository branch. The build will %s"
                "be skipped.",
                "" if result else "not ",
            )
        else:
            # Fetch the result based on the output of all plugins
            result = self._calculate_result(self._check())

        # Populate the output using all plugins.
        self._populate_result(result)

        self._logger.debug("Processing finished.")
