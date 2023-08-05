import importlib
from abc import ABC

import pytest


class BasePluginTest(ABC):
    """Base class for testing the plugins."""

    plugin_path: str = None
    plugin_class_name: str = None
    check_implemented: bool = False
    populate_implemented: bool = False

    @pytest.fixture(autouse=True)
    def set_up(self):
        """Import the module before each test."""
        # pylint: disable=attribute-defined-outside-init
        self.module = importlib.import_module(self.plugin_path)

    def test_plugin_exported_correctly(self):
        """
        Given the path to the plugin module and the name of the plugin class
        When we import both plugin class and `PLUGIN` constant from the module
        Then both plugin class and `PLUGIN` object are the same.
        """
        assert getattr(self.module, self.plugin_class_name) == getattr(
            self.module, "PLUGIN"
        )

    def test_check_is_implemented(self, vcs):
        """
        Given the fact that the `check` method is or is not implemented in the plugin
        When we run `check` method from the plugin
        Then a NotImplementedError is or is not raised.
        """
        plugin = self.module.PLUGIN("branch", vcs())

        if self.check_implemented:
            plugin.check()
        else:
            with pytest.raises(NotImplementedError):
                plugin.check()

    def test_populate_is_implemented(self, vcs):
        """
        Given the fact that the `populate` method is or is not implemented in the plugin
        When we run `populate` method from the plugin
        Then a NotImplementedError is or is not raised.
        """
        plugin = self.module.PLUGIN("branch", vcs())

        if self.populate_implemented:
            plugin.populate(True)
        else:
            with pytest.raises(NotImplementedError):
                plugin.populate(True)


class BaseVCSTest(ABC):
    """Base class for testing the VCS implementations."""

    vcs_path: str = None
    vcs_class_name: str = None

    @pytest.fixture(autouse=True)
    def set_up(self):
        """Import the module before each test."""
        # pylint: disable=attribute-defined-outside-init
        self.module = importlib.import_module(self.vcs_path)

    def test_vcs_exported_correctly(self):
        """
        Given the path to the VCS module and the name of the VCS class
        When we import both VCS class and `VCS` constant from the module
        Then both VCS class and `VCS` object are the same.
        """
        assert getattr(self.module, self.vcs_class_name) == getattr(self.module, "VCS")
