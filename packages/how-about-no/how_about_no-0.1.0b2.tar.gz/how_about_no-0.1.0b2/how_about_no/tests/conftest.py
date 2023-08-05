from typing import List, Optional
from unittest.mock import Mock

import pytest

from how_about_no.core import Logger
from how_about_no.core.vcs import BaseVCS
from how_about_no.tests.data import SAMPLE_CONFIG_FILE_CONTENT
from how_about_no.tests.fakes import FakeConfig, FakePlugin, FakeVCS


@pytest.fixture(name="config_file_content")
def config_file_content_fixture():
    """Return sample content of a configuration file."""
    return SAMPLE_CONFIG_FILE_CONTENT


@pytest.fixture(name="vcs")
def vcs_fixture():
    """Sample VCS fixture."""

    def _inner(
        raise_validation_error: Optional[bool] = False,
        current_branch_name: Optional[str] = "sample_branch",
        changed_files: Optional[List[str]] = None,
    ):
        return FakeVCS(
            raise_validation_error=raise_validation_error,
            current_branch_name=current_branch_name,
            changed_files=changed_files,
        )

    return _inner


@pytest.fixture(name="plugin")
def plugin_fixture():
    """Sample plugin fixture."""

    def _inner(
        main_branch_name: str,
        vcs: BaseVCS,
        check_result: bool = True,
        is_check_implemented: bool = True,
        is_populate_implemented: bool = True,
        **kwargs,
    ):
        return FakePlugin(
            main_branch_name=main_branch_name,
            vcs=vcs,
            check_result=check_result,
            is_check_implemented=is_check_implemented,
            is_populate_implemented=is_populate_implemented,
            **kwargs,
        )

    return _inner


@pytest.fixture(name="plugin_mock")
def plugin_mock_fixture():
    """Sample plugin mock."""

    def _inner(main_branch_name: str, vcs: BaseVCS, result: Optional[bool] = True):
        mock = Mock(main_branch_name=main_branch_name, vcs=vcs)
        mock.check.return_value = result
        return mock

    return _inner


@pytest.fixture(name="config")
def config_fixture():
    """Sample config fixture."""

    def _inner(**kwargs):
        config = FakeConfig(**kwargs)
        Logger.initialize(config.logger_level)
        return config

    return _inner
