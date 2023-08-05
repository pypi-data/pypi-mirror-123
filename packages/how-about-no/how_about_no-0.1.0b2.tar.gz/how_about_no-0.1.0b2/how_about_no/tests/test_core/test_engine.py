import logging
from unittest.mock import Mock, PropertyMock, patch

import pytest

from how_about_no.tests.fakes import FakeEngine

MSG_PROCESSING_STARTED = "Processing started."
MSG_PROCESSING_FINISHED = "Processing finished."
MGS_CURRENT_BRANCH_IS_MAIN = "The current branch is the main repository branch."
MGS_BUILD_WILL_BE_SKIPPED = "The build will be skipped."
MGS_BUILD_WILL_NOT_BE_SKIPPED = "The build will not be skipped."
MSG_POPULATING_STARTED = "Populating the result using loaded plugins started."
MSG_POPULATING_FINISHED = "Populating the result using loaded plugins finished."
MGS_POPULATED_VALUE = "Populated value:"
MSG_CHECK_STARTED = "Checking all plugins for the output started."
MSG_CHECK_FINISHED = "Checking all plugins for the output finished."
MGS_CHECK_RESULT = "Check result:"
MGS_NO_PLUGINS_LOADED = "No plugins have been loaded, the build will not be skipped."


@patch("how_about_no.core.engine.load_vcs", Mock())
def test_current_branch_is_main_dont_skip_build(caplog, capsys, vcs, plugin, config):
    """
    Given the current branch of the repository is the main branch
    And we don't skip the builds on the main branch
    When we run `process` method
    Then the builds are not skipped
    And expected messages are printed.
    """
    caplog.clear()
    main_branch_name = "sample_branch"

    sample_config = config(main_branch=main_branch_name)
    sample_vcs = vcs()
    sample_plugin = plugin(main_branch_name=main_branch_name, vcs=sample_vcs)

    engine = FakeEngine(
        configuration=sample_config, vcs=sample_vcs, plugins=[sample_plugin]
    )

    with caplog.at_level(logging.DEBUG):
        engine.process()

    stdout, _ = capsys.readouterr()

    assert MSG_PROCESSING_STARTED in caplog.text
    assert MSG_PROCESSING_FINISHED in caplog.text
    assert MGS_CURRENT_BRANCH_IS_MAIN in caplog.text
    assert MGS_BUILD_WILL_NOT_BE_SKIPPED in caplog.text
    assert MGS_POPULATED_VALUE in stdout
    assert MGS_CHECK_RESULT not in stdout


@patch("how_about_no.core.engine.load_vcs", Mock())
def test_current_branch_is_main_skip_build(caplog, capsys, vcs, plugin, config):
    """
    Given the current branch of the repository is the main branch
    And we skip the builds on the main branch
    When we run `process` method
    Then the builds are skipped
    And expected messages are printed.
    """
    caplog.clear()
    main_branch_name = "sample_branch"

    sample_config = config(
        main_branch=main_branch_name, skip_builds_on_main_branch=True
    )
    sample_vcs = vcs()
    sample_plugin = plugin(main_branch_name=main_branch_name, vcs=sample_vcs)

    engine = FakeEngine(
        configuration=sample_config, vcs=sample_vcs, plugins=[sample_plugin]
    )

    with caplog.at_level(logging.DEBUG):
        engine.process()

    stdout, _ = capsys.readouterr()

    assert MSG_PROCESSING_STARTED in caplog.text
    assert MSG_PROCESSING_FINISHED in caplog.text
    assert MGS_CURRENT_BRANCH_IS_MAIN in caplog.text
    assert MGS_BUILD_WILL_BE_SKIPPED in caplog.text
    assert MGS_POPULATED_VALUE in stdout
    assert MGS_CHECK_RESULT not in stdout


@patch("how_about_no.core.engine.load_vcs", Mock())
def test_check_and_populate(caplog, capsys, vcs, plugin, config):
    """
    Given the current branch of the repository is not the main branch
    When we run `process` method
    Then the all plugins are used to check and populate the results
    And expected messages are printed.
    """
    caplog.clear()
    main_branch_name = "sample_branch"

    sample_config = config(main_branch=main_branch_name)
    sample_vcs = vcs(current_branch_name="another_branch")
    sample_plugin = plugin(main_branch_name=main_branch_name, vcs=sample_vcs)

    engine = FakeEngine(
        configuration=sample_config, vcs=sample_vcs, plugins=[sample_plugin]
    )

    with caplog.at_level(logging.DEBUG):
        engine.process()

    stdout, _ = capsys.readouterr()

    assert MSG_PROCESSING_STARTED in caplog.text
    assert MSG_PROCESSING_FINISHED in caplog.text
    assert MGS_CURRENT_BRANCH_IS_MAIN not in caplog.text
    assert MSG_POPULATING_STARTED in caplog.text
    assert MSG_POPULATING_FINISHED in caplog.text
    assert MGS_POPULATED_VALUE in stdout
    assert MSG_CHECK_STARTED in caplog.text
    assert MSG_CHECK_FINISHED in caplog.text
    assert MGS_CHECK_RESULT in stdout


@patch("how_about_no.core.engine.load_vcs", Mock())
def test_all_plugins_are_used(vcs, config, plugin_mock):
    """
    Given the current branch of the repository is not the main branch
    When we run `process` method
    Then the all plugins are used to check and populate the results.
    """
    main_branch_name = "sample_branch"

    sample_config = config(main_branch=main_branch_name)
    sample_vcs = vcs(current_branch_name="another_branch")
    plugins = [
        plugin_mock(main_branch_name=main_branch_name, vcs=vcs),
        plugin_mock(main_branch_name=main_branch_name, vcs=vcs),
        plugin_mock(main_branch_name=main_branch_name, vcs=vcs),
    ]

    engine = FakeEngine(configuration=sample_config, vcs=sample_vcs, plugins=plugins)

    engine.process()

    for plugin in plugins:
        plugin.check.assert_called_once()
        plugin.populate.assert_called_once()


@patch("how_about_no.core.engine.load_vcs", Mock())
def test_no_plugins_loaded(caplog, vcs, config):
    """
    Given no plugins have been loaded
    When we run `process` method
    Then the processing will not start
    And expected message is printed.
    """
    caplog.clear()

    engine = FakeEngine(configuration=config(), vcs=vcs(), plugins=[])

    with caplog.at_level(logging.DEBUG):
        engine.process()

    assert MGS_NO_PLUGINS_LOADED in caplog.text
    assert MSG_PROCESSING_STARTED not in caplog.text


@pytest.mark.parametrize(
    "result_policy, plugin_one_result, plugin_two_result, expected_result",
    (
        ("all", True, True, True),
        ("all", True, False, False),
        ("all", False, False, False),
        ("any", True, True, True),
        ("any", True, False, True),
        ("any", False, False, False),
        ("none", True, True, False),
        ("none", True, False, False),
        ("none", False, False, True),
    ),
)
@patch("how_about_no.core.engine.load_vcs", Mock())
def test_result_is_correct(  # pylint: disable=too-many-arguments
    vcs,
    config,
    plugin_mock,
    result_policy,
    plugin_one_result,
    plugin_two_result,
    expected_result,
):
    """
    Given the current branch of the repository is not the main branch
    And there are multiple plugins defined
    And the `check` method from each plugin returns defined value
    And the result policy is defined
    When we run `process` method
    Then all plugins populate the correct overall result.
    """
    main_branch_name = "sample_branch"

    sample_config = config(main_branch=main_branch_name, result_policy=result_policy)
    sample_vcs = vcs(current_branch_name="another_branch")
    plugins = [
        plugin_mock(
            main_branch_name=main_branch_name, vcs=vcs, result=plugin_one_result
        ),
        plugin_mock(
            main_branch_name=main_branch_name, vcs=vcs, result=plugin_two_result
        ),
    ]

    engine = FakeEngine(configuration=sample_config, vcs=sample_vcs, plugins=plugins)

    engine.process()

    for plugin in plugins:
        plugin.check.assert_called_once()
        plugin.populate.assert_called_once_with(expected_result)


@patch("how_about_no.core.engine.load_vcs", Mock())
def test_incorrect_result_policy(vcs, config, plugin_mock):
    """
    Given the current branch of the repository is not the main branch
    And there are multiple plugins defined
    And the value of `result_policy` is incorrect
    When we run `process` method
    Then a SystemExit error is raised.
    """
    main_branch_name = "sample_branch"

    sample_config = config(main_branch=main_branch_name)

    sample_vcs = vcs(current_branch_name="another_branch")
    plugins = [
        plugin_mock(main_branch_name=main_branch_name, vcs=sample_vcs),
        plugin_mock(main_branch_name=main_branch_name, vcs=sample_vcs),
    ]

    engine = FakeEngine(configuration=sample_config, vcs=sample_vcs, plugins=plugins)

    with patch(
        "how_about_no.core.config.Config.result_policy", new_callable=PropertyMock
    ) as mock_result_policy:
        mock_result_policy.return_value = "wrong_value"

        with pytest.raises(SystemExit):
            engine.process()
