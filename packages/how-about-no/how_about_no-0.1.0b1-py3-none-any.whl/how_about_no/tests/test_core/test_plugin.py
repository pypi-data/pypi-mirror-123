from how_about_no.tests.fakes import FakePlugin, FakeVCS


def test_plugin_initialization():
    """
    Given a VCS, branch name and one more custom field
    When we initialize a plugin using these values
    Then the plugin is initialized correctly and all given values are set.
    """
    vcs = FakeVCS()
    plugin = FakePlugin(main_branch_name="sample_branch", vcs=vcs, check_result=True)

    assert plugin.main_branch_name == "sample_branch"
    assert plugin.vcs == vcs

    # Check if the dynamic property has been set
    assert plugin.check_result is True  # pylint: disable=no-member
