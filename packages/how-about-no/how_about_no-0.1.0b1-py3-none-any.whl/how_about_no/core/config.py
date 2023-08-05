import os
from typing import Any, Dict, Union

import yaml


class Config:
    """Class that holds the configuration from the configuration file."""

    _default_path: str = os.path.join(os.getcwd(), "how_about_no.yaml")
    _env_variable_name: str = "HOW_ABOUT_NO_CONFIG_FILE"
    _configuration: dict = None

    def __init__(self) -> None:
        """Load the configuration from the file.

        The default path of the configuration file is `./how_about_no.yaml`. If the
        default configuration file does not exist then the default settings will be
        used.

        If the environment variable `HOW_ABOUT_NO_CONFIG_FILE` is set, that path will be
        used instead. In that case, a ValueError error will be raised if the
        configuration file does not exist.

        Why it behaves like this? Well, it should be possible to use the library without
        defining the configuration file, so if it's not there then it's fine and we can
        expect to get the default values in that case. On the other hand, if there is a
        custom config file path defined then we assume the user wants to use his custom
        file and we should let him know that the provided path is incorrect if the
        specified file does not exist.
        """
        custom_path = os.getenv(self._env_variable_name)
        if custom_path:
            if not os.path.exists(custom_path):
                raise ValueError(
                    "Defined path to the configuration file is incorrect "
                    f"({custom_path}). Please make sure the file exists and "
                    "try again."
                )

            self._configuration = self._load(custom_path)
        else:
            if os.path.exists(self._default_path):
                self._configuration = self._load(self._default_path)

    def _load(self, file_path: str) -> Any:  # pylint: disable=no-self-use
        """Load and return the configuration from given file.

        Arguments:
            file_path (str): The path of the configuration file.
        """
        try:
            with open(file_path, encoding="utf-8") as config_file:
                return yaml.load(config_file, yaml.Loader)
        except Exception:  # pylint: disable=broad-except
            # If loading the configuration fails for any reason, return None.
            return None

    @property
    def configuration(self) -> Union[Dict, None]:
        """Return the configuration object."""
        return self._configuration

    @property
    def main_branch(self) -> str:
        """Return the value of the `main_branch` setting.

        If it's not defined or it's not a string then the default value will be
        returned.

        Default value: master.
        """
        default_value = "master"

        if not isinstance(self._configuration, dict):
            return default_value

        value = self._configuration.get("main_branch")
        return value if isinstance(value, str) else default_value

    @property
    def skip_builds_on_main_branch(self) -> bool:
        """Return the value of the `skip_builds_on_main_branch` setting.

        If it's not defined or it's not a boolean then the default value will be
        returned.

        Default value: False.
        """
        default_value = False

        if not isinstance(self._configuration, dict):
            return default_value

        value = self._configuration.get("skip_builds_on_main_branch")
        return value if isinstance(value, bool) else default_value

    @property
    def logger_level(self) -> str:
        """Return the value of the `logger_level` setting.

        If it's not defined or it's not a string then the default value will be
        returned.

        Default value: DEBUG.
        """
        default_value = "DEBUG"

        if not isinstance(self._configuration, dict):
            return default_value

        value = self._configuration.get("logger_level")
        return value if isinstance(value, str) else default_value

    @property
    def plugins(self) -> Dict:
        """Return the value of the `plugins` setting.

        If it's not defined or it's not a dictionary then the default value will be
        returned.

        Default value: {} (empty dictionary).
        """
        default_value = {}

        if not isinstance(self._configuration, dict):
            return default_value

        value = self._configuration.get("plugins")
        return value if isinstance(value, dict) else default_value

    @property
    def vcs(self) -> str:
        """Return the value of the `vcs` setting.

        If it's not defined or it's not a string then the default value will be
        returned.

        Default value: master.
        """
        default_value = "how_about_no.vcs.git"

        if not isinstance(self._configuration, dict):
            return default_value

        value = self._configuration.get("vcs")
        return value if isinstance(value, str) else default_value

    @property
    def result_policy(self) -> str:
        """Return the value of the `result_policy` setting.

        If it's not defined or it's not one of available values then the default value
        will be returned.

        Default value: all.
        """
        default_value = "all"

        if not isinstance(self._configuration, dict):
            return default_value

        value = self._configuration.get("result_policy")
        return value if value in ["all", "any", "none"] else default_value
