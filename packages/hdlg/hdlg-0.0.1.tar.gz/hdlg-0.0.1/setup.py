# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hdlg', 'hdlg.ui']

package_data = \
{'': ['*'], 'hdlg.ui': ['icons/*']}

install_requires = \
['PySide2>=5.15.2,<6.0.0', 'appdirs>=1.4.4,<2.0.0', 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['hdlg = hdlg.hdlg:main']}

setup_kwargs = {
    'name': 'hdlg',
    'version': '0.0.1',
    'description': 'Modern cross-platform GUI for hdl-dump.',
    'long_description': "# HDLG\n\n[![Pull requests welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)](http://makeapullrequest.com)\n[![GPLv3 license](https://img.shields.io/badge/license-GPLv3-blue)](https://github.com/rlaphoenix/hdlg/blob/master/LICENSE)\n[![PyPI version](https://img.shields.io/pypi/v/hdlg)](https://pypi.org/project/hdlg)\n[![Python versions](https://img.shields.io/pypi/pyversions/hdlg)](https://pypi.org/project/hdlg)\n[![PyPI status](https://img.shields.io/pypi/status/hdlg)](https://pypi.org/project/hdlg)\n[![Contributors](https://img.shields.io/github/contributors/rlaphoenix/Slipstream)](https://github.com/rlaphoenix/hdlg/graphs/contributors)\n[![GitHub issues](https://img.shields.io/github/issues/rlaphoenix/hdlg)](https://github.com/rlaphoenix/hdlg/issues)\n![Build](https://github.com/rlaphoenix/hdlg/workflows/Build/badge.svg?branch=master)\n\nHDLG is a modern cross-platform GUI for hdl-dump with Batch installation capabilities.\n\n## Looking for Artwork\n\nThis project is looking for an Icon and Text Logo as well as a Banner artwork. If you have some free time and would\nlike to contribute artwork to the project, let me know!\n\n## Installation\n\n    pip install --user hdlg\n\nTo run hdlg, type `hdlg` into any terminal, command prompt, app launcher, or the start menu.\n\nIf you wish to manually install from the source, take a look at [Building](#building-source-and-wheel-distributions).\n\n## To-do\n\n- [ ] Craft initial GUI with Qt.\n- [ ] Create a file based settings system.\n- [ ] Add local PS2 HDD connection option.\n- [ ] Add remote PS2 HDD (samba) connection option.\n- [ ] List installed games of selected HDD.\n- [ ] Add button to install a new game to selected HDD.\n- [ ] Add PyInstaller support (PyInstaller spec file).\n- [ ] Add information about a PS2 HDD like size, space used, games installed, count games by game type (PS2 DVD/CD, PS1), etc.\n- [ ] Push to PyPI and add relevant Badges.\n\n## Working with the Source Code\n\nThis project requires [Poetry], so feel free to take advantage and use it for its various conveniences like\nbuilding sdist/wheel packages, creating and managing dependencies, virtual environments, and more.\n\nNote:\n\n- Source Code may have changes that may be old, not yet tested or stable, or may have regressions.\n- Only run or install from Source Code if you have a good reason. Examples would be to test for regressions, test\n  changes (either your own or other contributors), or to research the code (agreeing to the [LICENSE](LICENSE)).\n- [Poetry] is required as it's used as the [PEP 517] build system, virtual environment manager, dependency manager,\n  and more.\n\n  [Poetry]: <https://python-poetry.org/docs/#installation>\n  [PEP 517]: <https://www.python.org/dev/peps/pep-0517>\n\n### Install from Source Code\n\n    git clone https://github.com/rlaphoenix/hdlg.git\n    cd hdlg\n    pip install --user .\n\n### Building source and wheel distributions\n\n    poetry build\n\nYou can specify `-f` to build `sdist` or `wheel` only. Built files can be found in the `/dist` directory.\n\n### Packing with PyInstaller\n\n    python -m pip install --user pyinstaller\n    poetry run pyinstaller hdlg.spec\n    .\\dist\\hdlg.exe\n\nFeel free to apply any CLI options/switches you feel like, see `pyinstaller -h`.\n",
    'author': 'PHOENiX',
    'author_email': 'rlaphoenix@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rlaphoenix/hdlg',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<3.10',
}


setup(**setup_kwargs)
