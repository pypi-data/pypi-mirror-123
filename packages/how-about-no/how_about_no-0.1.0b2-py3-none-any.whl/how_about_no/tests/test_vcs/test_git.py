import logging
from unittest.mock import patch

import pytest

from how_about_no.core.vcs import VCSException
from how_about_no.tests.base_tests import BaseVCSTest
from how_about_no.tests.fakes import get_fake_popen
from how_about_no.vcs.git import Git, get_git_executable_name


@pytest.mark.parametrize(
    "os_name, expected_result", (("posix", "git"), ("nt", "git.exe"))
)
def test_get_git_executable_name(os_name, expected_result):
    """
    Given the name of a operating system
    When we call get_git_executable_name
    Then we get a correct Git executable name.
    """
    with patch("how_about_no.vcs.git.os.name", os_name):
        assert get_git_executable_name() == expected_result


class TestGitVCSModule(BaseVCSTest):
    """Base tests for the Git VCS implementation."""

    vcs_path = "how_about_no.vcs.git"
    vcs_class_name = "Git"


class TestGetCurrentBranchName:
    """Tests for the Git `get_current_branch_name` method."""

    @pytest.fixture(autouse=True)
    def set_up(self):
        """Create a VCS object for each test."""
        self.vcs = Git()  # pylint: disable=attribute-defined-outside-init

    @patch("how_about_no.vcs.git.Popen", get_fake_popen(command_output="master\n"))
    def test_success(self):
        """
        Given git command returns a correct name of the branch
        When we call method `get_current_branch_name`
        Then we get the name of the branch as result.
        """
        assert self.vcs.get_current_branch_name() == "master"

    @patch("how_about_no.vcs.git.Popen", get_fake_popen(return_code=1))
    def test_incorrect_return_code(self, caplog):
        """
        Given git command returns a response with incorrect return code
        When we call method `get_current_branch_name`
        Then a VCSException error is raised and a correct error message is printed.
        """
        caplog.clear()

        with pytest.raises(VCSException):
            with caplog.at_level(logging.DEBUG):
                self.vcs.get_current_branch_name()

        assert (
            "It's not possible to fetch the name of the current branch." in caplog.text
        )

    @pytest.mark.parametrize("error", (IndexError, AttributeError))
    def test_raises_error(self, error, caplog):
        """
        Given executing the git command raises an error
        When we call method `get_current_branch_name`
        Then a VCSException error is raised and a correct error message is printed.
        """
        caplog.clear()

        with patch("how_about_no.vcs.git.Popen", get_fake_popen(side_effect=error)):
            with pytest.raises(VCSException):
                with caplog.at_level(logging.DEBUG):
                    self.vcs.get_current_branch_name()

        assert (
            "It's not possible to fetch the name of the current branch." in caplog.text
        )


class TestGetListOfChangedFiles:
    """Tests for the Git `get_list_of_changed_files` method."""

    @pytest.fixture(autouse=True)
    def set_up(self):
        """Create a VCS object for each test."""
        self.vcs = Git()  # pylint: disable=attribute-defined-outside-init

    @patch(
        "how_about_no.vcs.git.Popen", get_fake_popen(command_output="file1\nfile2\n")
    )
    def test_success(self):
        """
        Given git command returns a correct name of the branch
        When we call method `get_list_of_changed_files`
        Then we get the name of the branch as result.
        """
        assert self.vcs.get_list_of_changed_files("branch") == ["file1", "file2"]

    @patch("how_about_no.vcs.git.Popen", get_fake_popen(return_code=1))
    def test_incorrect_return_code(self, caplog):
        """
        Given git command returns a response with incorrect return code
        When we call method `get_list_of_changed_files`
        Then a VCSException error is raised and a correct error message is printed.
        """
        caplog.clear()

        with pytest.raises(VCSException):
            with caplog.at_level(logging.DEBUG):
                self.vcs.get_list_of_changed_files("branch")

        assert "It's not possible to fetch the list of changed files." in caplog.text

    @pytest.mark.parametrize("error", (IndexError, AttributeError))
    def test_raises_error(self, error, caplog):
        """
        Given executing the git command raises an error
        When we call method `get_list_of_changed_files`
        Then a VCSException error is raised and a correct error message is printed.
        """
        caplog.clear()

        with patch("how_about_no.vcs.git.Popen", get_fake_popen(side_effect=error)):
            with pytest.raises(VCSException):
                with caplog.at_level(logging.DEBUG):
                    self.vcs.get_list_of_changed_files("branch")

        assert "It's not possible to fetch the list of changed files." in caplog.text


class TestValidate:
    """Tests for the Git `validate` method."""

    @pytest.fixture(autouse=True)
    def set_up(self):
        """Create a VCS object for each test."""
        self.vcs = Git()  # pylint: disable=attribute-defined-outside-init

    @patch("how_about_no.vcs.git.Popen", get_fake_popen())
    @patch("how_about_no.vcs.git.which")
    def test_success(self, mock_which):
        """
        Given the git executable exists in the system PATH
        And the current working directory is a git repository
        When we call `validate` method
        Then it does not raise an error.
        """
        mock_which.return_value = "some_value"

        self.vcs.validate()

    @patch("how_about_no.vcs.git.Popen", get_fake_popen())
    @patch("how_about_no.vcs.git.which")
    def test_no_git_executable_found(self, mock_which):
        """
        Given the git executable does not exist in the system PATH
        When we call `validate` method
        Then it raises a VCSException error.
        """
        mock_which.return_value = None

        with pytest.raises(VCSException):
            self.vcs.validate()

    @patch("how_about_no.vcs.git.Popen", get_fake_popen(return_code=1))
    @patch("how_about_no.vcs.git.which")
    def test_no_git_repository_found(self, mock_which):
        """
        Given the git executable exists in the system PATH
        And the current working directory is not a git repository
        When we call `validate` method
        Then it raises a VCSException error.
        """
        mock_which.return_value = "some_value"

        with pytest.raises(VCSException):
            self.vcs.validate()
