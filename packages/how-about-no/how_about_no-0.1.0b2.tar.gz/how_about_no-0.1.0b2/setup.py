# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['how_about_no',
 'how_about_no.core',
 'how_about_no.plugins',
 'how_about_no.plugins.ci',
 'how_about_no.plugins.vcs',
 'how_about_no.tests',
 'how_about_no.tests.test_core',
 'how_about_no.tests.test_plugins',
 'how_about_no.tests.test_plugins.test_ci',
 'how_about_no.tests.test_plugins.test_vcs',
 'how_about_no.tests.test_vcs',
 'how_about_no.vcs']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0']

entry_points = \
{'console_scripts': ['how-about-no = how_about_no:main']}

setup_kwargs = {
    'name': 'how-about-no',
    'version': '0.1.0b2',
    'description': "Let's your CI/CD tool know when the build can be skipped.",
    'long_description': '# How about no\n\n![tests][tests]\n![black][black]\n![pylint][pylint]\n![isort][isort]\n\n![how_about_no][how_about_no]\n\n*Image source: https://knowyourmeme.com/photos/129577-how-about-no*\n\nThe sole purpose of this library is to let your CI/CD tool know whether or not the\nbuild it\'s about to run is necessary.\n\nPlease note that there is no stable release yet, and the documentation will be added\nshortly.\n\n\n\n[tests]: https://github.com/mateuszcisek/how_about_no/actions/workflows/tests.yaml/badge.svg "tests"\n[black]: https://github.com/mateuszcisek/how_about_no/actions/workflows/linting_black.yaml/badge.svg "black"\n[pylint]: https://github.com/mateuszcisek/how_about_no/actions/workflows/linting_pylint.yaml/badge.svg "pylint"\n[isort]: https://github.com/mateuszcisek/how_about_no/actions/workflows/linting_isort.yaml/badge.svg "isort"\n[how_about_no]: how_about_no.jpg "how about no"\n',
    'author': 'Mateusz Cisek',
    'author_email': 'cismat@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mateuszcisek/how_about_no',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
