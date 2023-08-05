# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['egit']

package_data = \
{'': ['*'], 'egit': ['config/*', 'logs/*', 'target/*']}

install_requires = \
['GitPython>=3.1.18,<4.0.0', 'PyYAML>=5.4.1,<6.0.0']

extras_require = \
{':extra == "test"': ['black>=21.6b0,<22.0'],
 'dev': ['pip>=21.1.3,<22.0.0',
         'toml>=0.10.2,<0.11.0',
         'tox>=3.23.1,<4.0.0',
         'twine>=3.4.1,<4.0.0',
         'virtualenv>=20.4.7,<21.0.0'],
 'doc': ['mkdocs>=1.2.1,<2.0.0',
         'mkdocs-autorefs>=0.2.1,<0.3.0',
         'mkdocs-include-markdown-plugin>=3.1.4,<4.0.0',
         'mkdocs-material>=7.1.9,<8.0.0',
         'mkdocs-material-extensions>=1.0.1,<2.0.0',
         'mkdocstrings>=0.15.2,<0.16.0'],
 'test': ['flake8>=3.9.2,<4.0.0',
          'isort>=5.9.1,<6.0.0',
          'pytest>=6.2.4,<7.0.0',
          'pytest-cov>=2.12.1,<3.0.0']}

entry_points = \
{'console_scripts': ['egit = egit:main']}

setup_kwargs = {
    'name': 'egit',
    'version': '2.0.0',
    'description': 'e(g)it is an app for replacing text in files across multiple GitHub repositories.',
    'long_description': "# e(g)it\n\n_e(g)it is an app for replacing text in files across multiple GitHub repositories._\n\n[![CodeQL](https://github.com/datadlog/egit/actions/workflows/codeql-analysis.yml/badge.svg?branch=main)](https://github.com/datadlog/egit/actions/workflows/codeql-analysis.yml) [![PyPI version](https://badge.fury.io/py/egit.svg)](https://badge.fury.io/py/egit) [![Total alerts](https://img.shields.io/lgtm/alerts/g/datadlog/egit.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/datadlog/egit/alerts/) [![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/datadlog/egit.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/datadlog/egit/context:python)\n## Features\n\n-   Clones the configured Github repositories to your local.\n-   From a specified base branch, creates a feature branch.\n-   Replaces the content in files if it finds the matching text exists in the local repositories, if there is a file pattern specified in the configuration file, the app replaces only in those files.\n-   Commits the changes and creates a pull request for code review.\n\n## Tech\n\ne(g)it uses a number of open source projects to work properly:\n\n-   [Python] - Python for the backend.\n-   [GitPython] - Python library used to interact with git repositories.\n-   [PyYAML] - PyYAML features a complete YAML 1.1 parser.\n-   [MkDocs] - MkDocs is a fast, simple and downright gorgeous static site generator that's geared towards building project documentation.\n-   [Flake8] - Flake8 is a great toolkit for checking your code base against coding style (PEP8), programming errors and to check cyclomatic complexity.\n-   [Tox] - Tox is a generic virtualenv management and test command line tool.\n-   [Twine] - Twine is a utility for publishing Python packages on PyPI.\n-   [CodeQL] - CodeQL is the analysis engine used by developers to automate security checks, and by security researchers to perform variant analysis.\n-   [VSCode] - Visual Studio Code is a source-code editor.\n\n## Documentation\n\nCheck out the following website for further information **[egit]**\n\n## License\n\nMIT\n\n[egit]: https://datadlog.github.io/egit/\n[python]: https://www.python.org/\n[gitpython]: https://gitpython.readthedocs.io/en/stable/tutorial.html\n[pyyaml]: https://pyyaml.org/wiki/PyYAML\n[mkdocs]: https://www.mkdocs.org/\n[flake8]: https://flake8.pycqa.org/en/latest/\n[tox]: https://tox.readthedocs.io/en/latest/\n[twine]: https://twine.readthedocs.io/en/latest/\n[codeql]: https://securitylab.github.com/tools/codeql/\n[vscode]: https://code.visualstudio.com/\n",
    'author': 'Naveen Thurimerla',
    'author_email': 'nawinto99@gmail.com',
    'maintainer': 'Naveen Thurimerla',
    'maintainer_email': 'nawinto99@gmail.com',
    'url': 'https://github.com/datadlog/egit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
