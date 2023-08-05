import pytest

from how_about_no.tests.base_tests import BasePluginTest


class TestTeamcityPlugin(BasePluginTest):
    """Test for the Teamcity plugin."""

    plugin_path = "how_about_no.plugins.ci.teamcity"
    plugin_class_name = "Teamcity"
    populate_implemented = True

    @pytest.mark.parametrize("value", (True, False))
    def test_populate_message_is_correct(self, vcs, capsys, value):
        """
        Given the value to populate with the plugin
        When we call `populate` method and pass that value as an argument
        Then a correct message will be printed.
        """
        plugin = self.module.PLUGIN("branch", vcs)
        plugin.populate(value)

        stdout, _ = capsys.readouterr()
        assert (
            f"##teamcity[setParameter name='env.SKIP_BUILDS' value='{value}']" in stdout
        )

    def test_custom_variable_name(self, vcs, capsys):
        """
        Given a custom variable name that should be used when populating the values
        When we call `populate` method
        Then a correct message with that variable name will be printed.
        """
        plugin = self.module.PLUGIN("branch", vcs, variable_name="example")
        plugin.populate(True)

        stdout, _ = capsys.readouterr()
        assert "##teamcity[setParameter name='example' value='True']" in stdout
