import re
from typing import List

from how_about_no.core import BasePlugin


class ChangedFiles(BasePlugin):
    """Changed files plugin.

    If checks the list of all files changed compared to the main VCS branch against
    provided regex patterns. If all files match at least one of provided patterns,
    the result of the check is True, otherwise it's False.
    """

    def _get_regex_patterns(self):
        """
        Return the regex patterns that will be used to determine whether or not the
        build should be skipped.
        """
        return getattr(self, "patterns", [])

    def _does_file_path_match(  # pylint: disable=no-self-use
        self, file_path: str, patterns: List[str]
    ) -> bool:
        """Check if the name of the file match any of the provided regex patterns.

        Arguments:
            file_path (str): The path of the file to check.
            patterns (List[str]): A list of patterns to test.

        Returns:
            (bool): Flag indicating wether or not the name of the file match any of the
                provided regex patterns.
        """
        for pattern in patterns:
            if re.match(pattern, file_path):
                return True

        return False

    def check(self) -> bool:
        """Check if the files changed in the current branch can be ignored.

        Returns:
            (bool): Flag indicating whether or not the build should be skipped.
        """
        changed_files = self.vcs.get_list_of_changed_files(self.main_branch_name)
        if not changed_files:
            # If no files have been changed then we can skip the build.
            self._logger.debug("No files have been changed, the build can be skipped.")
            return True

        patterns = self._get_regex_patterns()
        if not patterns:
            # If there are no patterns provided then we cannot skip the build.
            self._logger.debug(
                "No regex patterns have been provided, the build cannot be skipped."
            )
            return False

        for file_path in changed_files:
            if not self._does_file_path_match(file_path, patterns):
                # If at least one files does not match any of the provided regex
                # patterns then we cannot skip the build.
                self._logger.debug(
                    f"File `{file_path}` does not match any of the provided regex"
                    " patterns."
                )
                return False

        # All files match at least one pattern, therefore we can skip the build.
        self._logger.debug(
            "All files match at least one of the provided regex patterns."
        )
        return True


PLUGIN = ChangedFiles
