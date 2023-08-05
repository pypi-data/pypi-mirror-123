from typing import List, Optional, Type
from unittest.mock import Mock

from how_about_no.core import BasePlugin, BaseVCS, Config, Engine, VCSException
from how_about_no.tests.data import SAMPLE_CONFIG_DICT
from how_about_no.vcs.git import Git


class FakeVCS(BaseVCS):
    """A fake VCS implementation for testing purposes."""

    def __init__(
        self,
        raise_validation_error: Optional[bool] = False,
        current_branch_name: Optional[str] = "sample_branch",
        changed_files: Optional[List[str]] = None,
    ):
        super().__init__()
        self.raise_validation_error = raise_validation_error
        self.current_branch_name = current_branch_name
        self.changed_files = changed_files

    def validate(self) -> None:
        if self.raise_validation_error:
            raise VCSException()

    def get_current_branch_name(self) -> str:
        return self.current_branch_name

    def get_list_of_changed_files(self, branch_name: str) -> List[str]:
        return self.changed_files if self.changed_files else []


class FakePlugin(BasePlugin):
    """A fake plugin implementation for testing purposes."""

    def __init__(
        self,
        main_branch_name: str,
        vcs: BaseVCS,
        is_check_implemented: bool = True,
        is_populate_implemented: bool = True,
        **kwargs,
    ) -> None:
        super().__init__(main_branch_name, vcs, **kwargs)
        self._is_check_implemented = is_check_implemented
        self._is_populate_implemented = is_populate_implemented

    def check(self):
        if not self._is_check_implemented:
            raise NotImplementedError()

        result = getattr(self, "check_result", False)
        print(f"Check result: {result}")
        return result

    def populate(self, value: bool) -> None:
        if not self._is_populate_implemented:
            raise NotImplementedError()

        print(f"Populated value: {value}")


class FakeConfig(Config):
    """A fake configuration implementation for testing purposes."""

    def __init__(self, **kwargs) -> None:  # pylint: disable=super-init-not-called
        self._configuration = SAMPLE_CONFIG_DICT
        self._configuration.update(kwargs)


class FakeEngine(Engine):
    """A fake engine implementation for testing purposes."""

    def __init__(
        self, configuration: Config, vcs: BaseVCS, plugins: List[BasePlugin] = None
    ):
        self._defined_plugins = plugins or []
        super().__init__(configuration)

        self._vcs = vcs or Git()

    def _load_plugins(self, plugins: dict) -> List[BasePlugin]:
        return self._defined_plugins


def get_fake_popen(
    command_output: Optional[str] = None,
    return_code: Optional[int] = 0,
    side_effect: Optional[Type[Exception]] = None,
):
    """Return a fake class imitating the behavior of Popen class."""

    class _FakePopen:
        """A fake Popen implementation for testing purposes."""

        def __init__(self, *args, **kwargs):
            pass

        def __enter__(self):
            if side_effect:
                raise side_effect()

            mock_popen_result = Mock(returncode=return_code)
            mock_popen_result.communicate.return_value = (
                command_output.encode("utf-8") if command_output else "",
                None,
            )
            return mock_popen_result

        def __exit__(self, *args, **kwargs):
            pass

    return _FakePopen
