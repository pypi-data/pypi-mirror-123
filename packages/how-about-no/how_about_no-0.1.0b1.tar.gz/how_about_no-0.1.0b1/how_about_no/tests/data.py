SAMPLE_CONFIG_FILE_CONTENT = "\n".join(
    [
        "main_branch: sample_branch",
        "skip_builds_on_main_branch: false",
        "logger_level: ERROR",
        "vcs: vcs.git",
        "result_policy: all",
        "plugins:",
        "  sample_plugin:",
        "    option_1: text",
        "    option_2: 123",
    ]
)

SAMPLE_CONFIG_DICT = {
    "main_branch": "sample_branch",
    "skip_builds_on_main_branch": False,
    "logger_level": "ERROR",
    "vcs": "vcs.git",
    "result_policy": "all",
    "plugins": {"sample_plugin": {"option_1": "text", "option_2": 123}},
}
