import logging
import os
from unittest.mock import mock_open, patch

import pytest

from how_about_no.core import Config
from how_about_no.tests.data import SAMPLE_CONFIG_DICT


class TestLoadingConfiguration:
    """Tests for the core configuration module."""

    @patch.dict(os.environ, {"HOW_ABOUT_NO_CONFIG_FILE": ""}, clear=True)
    @patch("how_about_no.core.config.Config._load")
    def test_default_config_file_used(self, mock_load):  # pylint: disable=no-self-use
        """
        Given no custom path to the configuration file is set
        When we load the configuration
        Then the default path to the config file is used.
        """
        default_path = f"{os.getcwd()}/how_about_no.yaml"

        Config()

        mock_load.assert_called_once_with(default_path)

    @patch.dict(os.environ, {"HOW_ABOUT_NO_CONFIG_FILE": "SAMPLE_PATH"}, clear=True)
    @patch("how_about_no.core.config.os.path.exists")
    @patch("how_about_no.core.config.Config._load")
    def test_custom_non_existing_config_file_used(  # pylint: disable=no-self-use
        self, mock_load, mock_exists, caplog
    ):
        """
        Given a custom path to an existing configuration file is set
        When we load the configuration
        Then the custom path to the config file is used
        And a ValueError is raised.
        """
        mock_exists.return_value = False

        with caplog.at_level(logging.WARNING):
            with pytest.raises(ValueError):
                Config()

        mock_exists.assert_called_once_with("SAMPLE_PATH")
        mock_load.assert_not_called()

    @patch.dict(os.environ, {"HOW_ABOUT_NO_CONFIG_FILE": "SAMPLE_PATH"}, clear=True)
    @patch("how_about_no.core.config.os.path.exists")
    @patch("how_about_no.core.config.Config._load")
    def test_custom_existing_config_file_used(  # pylint: disable=no-self-use
        self, mock_load, mock_exists
    ):
        """
        Given a custom path to an existing configuration file is set
        When we load the configuration
        Then the custom path to the config file is used.
        """
        mock_exists.return_value = True

        Config()

        mock_exists.assert_called_once_with("SAMPLE_PATH")
        mock_load.assert_called_once_with("SAMPLE_PATH")

    @patch.dict(os.environ, {"HOW_ABOUT_NO_CONFIG_FILE": ""}, clear=True)
    @patch("how_about_no.core.config.os.path.exists")
    def test_config_loaded_correctly(  # pylint: disable=no-self-use
        self, mock_exists, config_file_content
    ):
        """
        Given the `open` function returns a file with some content
        When we load the configuration using that file
        Then the configuration is loaded and contains the data from that file.
        """
        mock_exists.return_value = True

        with patch("builtins.open", mock_open(read_data=config_file_content)):
            config = Config()

        assert config.configuration == SAMPLE_CONFIG_DICT


class TestMainBranchProperty:
    """Tests for property `main_branch`."""

    @patch("how_about_no.core.config.os.path.exists")
    @patch("how_about_no.core.config.Config._load")
    @pytest.mark.parametrize("configuration_value", (1, "abc", tuple(), set()))
    def test_with_configuration_not_set_to_dict(  # pylint: disable=no-self-use
        self, mock_load, mock_exists, configuration_value
    ):
        """
        Given the configuration object set to a certain value
        When we fetch the main branch using `main_branch` property
        Then we get a correct value as the result.
        """
        mock_exists.return_value = True
        mock_load.return_value = configuration_value

        config = Config()

        assert config.main_branch == "master"

    @patch("how_about_no.core.config.os.path.exists")
    @patch("how_about_no.core.config.Config._load")
    @pytest.mark.parametrize(
        "configuration_value, expected_result",
        (
            (1, "master"),
            ("abc", "abc"),
            (tuple(), "master"),
            ({}, "master"),
            (set(), "master"),
            (True, "master"),
            (False, "master"),
        ),
    )
    def test_with_configuration_set_to_dict(  # pylint: disable=no-self-use
        self, mock_load, mock_exists, configuration_value, expected_result
    ):
        """
        Given the `main_branch` setting set to a certain value
        When we fetch the main branch using `main_branch` property
        Then we get a correct value as the result.
        """
        mock_exists.return_value = True
        mock_load.return_value = {"main_branch": configuration_value}

        config = Config()

        assert config.main_branch == expected_result


class TestSkipBuildsOnMainBranchProperty:
    """Tests for property `skip_builds_on_main_branch`."""

    @patch("how_about_no.core.config.os.path.exists")
    @patch("how_about_no.core.config.Config._load")
    @pytest.mark.parametrize("configuration_value", (1, "abc", tuple(), set()))
    def test_with_configuration_not_set_to_dict(  # pylint: disable=no-self-use
        self, mock_load, mock_exists, configuration_value
    ):
        """
        Given the configuration object set to a certain value
        When we fetch the main branch using `skip_builds_on_main_branch` property
        Then we get a correct value as the result.
        """
        mock_exists.return_value = True
        mock_load.return_value = configuration_value

        config = Config()

        assert config.skip_builds_on_main_branch is False

    @patch("how_about_no.core.config.os.path.exists")
    @patch("how_about_no.core.config.Config._load")
    @pytest.mark.parametrize(
        "configuration_value, expected_result",
        (
            (1, False),
            ("abc", False),
            (tuple(), False),
            ({}, False),
            (set(), False),
            (True, True),
            (False, False),
        ),
    )
    def test_with_configuration_set_to_dict(  # pylint: disable=no-self-use
        self, mock_load, mock_exists, configuration_value, expected_result
    ):
        """
        Given the `skip_builds_on_main_branch` setting set to a certain value
        When we fetch the main branch using `skip_builds_on_main_branch` property
        Then we get a correct value as the result.
        """
        mock_exists.return_value = True
        mock_load.return_value = {"skip_builds_on_main_branch": configuration_value}

        config = Config()

        assert config.skip_builds_on_main_branch == expected_result


class TestLoggerLevelProperty:
    """Tests for property `logger_level`."""

    @patch("how_about_no.core.config.os.path.exists")
    @patch("how_about_no.core.config.Config._load")
    @pytest.mark.parametrize("configuration_value", (1, "abc", tuple(), set()))
    def test_with_configuration_not_set_to_dict(  # pylint: disable=no-self-use
        self, mock_load, mock_exists, configuration_value
    ):
        """
        Given the configuration object set to a certain value
        When we fetch the main branch using `logger_level` property
        Then we get a correct value as the result.
        """
        mock_exists.return_value = True
        mock_load.return_value = configuration_value

        config = Config()

        assert config.logger_level == "DEBUG"

    @patch("how_about_no.core.config.os.path.exists")
    @patch("how_about_no.core.config.Config._load")
    @pytest.mark.parametrize(
        "configuration_value, expected_result",
        (
            (1, "DEBUG"),
            ("abc", "abc"),
            (tuple(), "DEBUG"),
            ({}, "DEBUG"),
            (set(), "DEBUG"),
            (True, "DEBUG"),
            (False, "DEBUG"),
        ),
    )
    def test_with_configuration_set_to_dict(  # pylint: disable=no-self-use
        self, mock_load, mock_exists, configuration_value, expected_result
    ):
        """
        Given the `logger_level` setting set to a certain value
        When we fetch the main branch using `logger_level` property
        Then we get a correct value as the result.
        """
        mock_exists.return_value = True
        mock_load.return_value = {"logger_level": configuration_value}

        config = Config()

        assert config.logger_level == expected_result


class TestPluginsProperty:
    """Tests for property `plugins`."""

    @patch("how_about_no.core.config.os.path.exists")
    @patch("how_about_no.core.config.Config._load")
    @pytest.mark.parametrize("configuration_value", (1, "abc", tuple(), set()))
    def test_with_configuration_not_set_to_dict(  # pylint: disable=no-self-use
        self, mock_load, mock_exists, configuration_value
    ):
        """
        Given the configuration object set to a certain value
        When we fetch the main branch using `plugins` property
        Then we get a correct value as the result.
        """
        mock_exists.return_value = True
        mock_load.return_value = configuration_value

        config = Config()

        assert config.plugins == {}

    @patch("how_about_no.core.config.os.path.exists")
    @patch("how_about_no.core.config.Config._load")
    @pytest.mark.parametrize(
        "configuration_value, expected_result",
        (
            (1, {}),
            ("abc", {}),
            (tuple(), {}),
            ({"sample": "value"}, {"sample": "value"}),
            (set(), {}),
            (True, {}),
            (False, {}),
        ),
    )
    def test_with_configuration_set_to_dict(  # pylint: disable=no-self-use
        self, mock_load, mock_exists, configuration_value, expected_result
    ):
        """
        Given the `plugins` setting set to a certain value
        When we fetch the main branch using `plugins` property
        Then we get a correct value as the result.
        """
        mock_exists.return_value = True
        mock_load.return_value = {"plugins": configuration_value}

        config = Config()

        assert config.plugins == expected_result


class TestResultPolicyProperty:
    """Tests for property `result_policy`."""

    @patch("how_about_no.core.config.os.path.exists")
    @patch("how_about_no.core.config.Config._load")
    @pytest.mark.parametrize("configuration_value", (1, "abc", tuple(), set()))
    def test_with_configuration_not_set_to_dict(  # pylint: disable=no-self-use
        self, mock_load, mock_exists, configuration_value
    ):
        """
        Given the configuration object set to a certain value
        When we fetch the main branch using `result_policy` property
        Then we get a correct value as the result.
        """
        mock_exists.return_value = True
        mock_load.return_value = configuration_value

        config = Config()

        assert config.result_policy == "all"

    @patch("how_about_no.core.config.os.path.exists")
    @patch("how_about_no.core.config.Config._load")
    @pytest.mark.parametrize(
        "configuration_value, expected_result",
        (
            (1, "all"),
            ("abc", "all"),
            ("all", "all"),
            ("any", "any"),
            ("none", "none"),
            (tuple(), "all"),
            ({}, "all"),
            (set(), "all"),
            (True, "all"),
            (False, "all"),
        ),
    )
    def test_with_configuration_set_to_dict(  # pylint: disable=no-self-use
        self, mock_load, mock_exists, configuration_value, expected_result
    ):
        """
        Given the `result_policy` setting set to a certain value
        When we fetch the main branch using `result_policy` property
        Then we get a correct value as the result.
        """
        mock_exists.return_value = True
        mock_load.return_value = {"result_policy": configuration_value}

        config = Config()

        assert config.result_policy == expected_result
