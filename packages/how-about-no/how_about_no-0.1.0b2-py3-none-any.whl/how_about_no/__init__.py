from how_about_no.core import Config, Engine, Logger


def main() -> None:
    """Run the engine."""
    config = Config()
    Logger.initialize(config.logger_level)
    Engine(config).process()


if __name__ == "__main__":
    main()
