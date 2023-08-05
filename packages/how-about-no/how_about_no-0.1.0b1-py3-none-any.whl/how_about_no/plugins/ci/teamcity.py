import sys

from how_about_no.core import BasePlugin


class Teamcity(BasePlugin):
    """Teamcity plugin.

    It is used to populate the result of the check to a Teamcity variable.
    """

    def _get_variable_name(self) -> str:
        """Return the name of the variable to set on Teamcity."""
        return str(getattr(self, "variable_name", "env.SKIP_BUILDS"))

    def populate(self, value: bool) -> None:
        """Set the value of a Teamcity variable to the given value.

        Arguments:
            value (bool): The value to set.
        """
        variable = self._get_variable_name()
        sys.stdout.write(
            f"##teamcity[setParameter name='{variable}' value='{value}']\n"
        )


PLUGIN = Teamcity
