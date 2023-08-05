import logging

from how_about_no.tests.base_tests import BasePluginTest


class TestChangedFilesPlugin(BasePluginTest):
    """Test for the changed files plugin."""

    plugin_path = "how_about_no.plugins.vcs.changed_files"
    plugin_class_name = "ChangedFiles"
    check_implemented = True

    def test_check_no_changed_files(self, vcs, caplog):
        """
        Given no files have been changed comparing to the main branch
        When we call `check` method
        Then the result is True and a correct message is printed.
        """
        caplog.clear()

        plugin = self.module.PLUGIN("branch", vcs(changed_files=[]))

        with caplog.at_level(logging.DEBUG):
            result = plugin.check()

        assert result is True
        assert "No files have been changed, the build can be skipped." in caplog.text

    def test_check_no_patterns(self, vcs, caplog):
        """
        Given a plugin with no regex patterns configured
        When we call `check` method
        Then the result is False and a correct message is printed.
        """
        caplog.clear()

        plugin = self.module.PLUGIN(
            "branch", vcs(changed_files=["sample"]), patterns=[]
        )

        with caplog.at_level(logging.DEBUG):
            result = plugin.check()

        assert result is False
        assert (
            "No regex patterns have been provided, the build cannot be skipped."
            in caplog.text
        )

    def test_file_name_matches_patterns(self, vcs, caplog):
        """
        Given a file changed comparing to the main branch
        And a plugin regex pattern matching the name of the changed file
        When we call `check` method
        Then the result is True and a correct message is printed.
        """
        caplog.clear()

        plugin = self.module.PLUGIN(
            "branch", vcs(changed_files=["sample"]), patterns=["^sample$"]
        )

        with caplog.at_level(logging.DEBUG):
            result = plugin.check()

        assert result is True
        assert (
            "All files match at least one of the provided regex patterns."
            in caplog.text
        )

    def test_file_name_doesnt_match_patterns(self, vcs, caplog):
        """
        Given a file changed comparing to the main branch
        And a plugin regex pattern not matching the name of the changed file
        When we call `check` method
        Then the result is False and a correct message is printed.
        """
        caplog.clear()

        plugin = self.module.PLUGIN(
            "branch", vcs(changed_files=["sample"]), patterns=["^another$", "^pattern"]
        )

        with caplog.at_level(logging.DEBUG):
            result = plugin.check()

        assert result is False
        assert (
            "File `sample` does not match any of the provided regex patterns."
            in caplog.text
        )
