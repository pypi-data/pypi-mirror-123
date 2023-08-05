from unittest.mock import patch

from how_about_no.core import Logger


@patch("how_about_no.core.logger.logging")
def test_initialize(mock_logging):
    """
    When we call method `Logger.initialize`
    Then the logging `basicConfig` function is called with correct arguments.
    """
    Logger.initialize(level="sample")

    mock_logging.basicConfig.assert_called_once_with(
        level="sample", format="%(levelname)s - %(message)s"
    )


def test_get_existing_logger():
    """
    Given a logger with the given name already exists
    When we get a logger with the same name
    Then the same logger is returned.
    """
    logger = Logger.get_logger("sample")

    assert logger
    assert logger == Logger.get_logger("sample")


def test_get_new_logger():
    """
    Given a logger with the given name already exists
    When we get a logger with a different name
    Then a different logger is returned.
    """
    logger = Logger.get_logger("sample")

    assert logger
    assert logger != Logger.get_logger("another")
