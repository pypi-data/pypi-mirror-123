# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyleft']

package_data = \
{'': ['*']}

install_requires = \
['pathspec>=0.9.0,<0.10.0', 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['pyleft = pyleft.console:run']}

setup_kwargs = {
    'name': 'pyleft',
    'version': '0.1.3',
    'description': 'Python type annotation existence checker',
    'long_description': '# PyLeft\n\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![GitHub license](https://img.shields.io/github/license/NathanVaughn/pyleft)](https://github.com/NathanVaughn/pyleft/blob/master/LICENSE)\n[![PyPi versions](https://img.shields.io/pypi/pyversions/pyleft)](https://pypi.org/project/pyleft)\n[![PyPi downloads](https://img.shields.io/pypi/dm/pyleft)](https://pypi.org/project/pyleft)\n\nPython type annotation existence checker\n\n----\n\n`pyleft` is a complement to Microsoft\'s [pyright](https://github.com/microsoft/pyright) \ntool. While `pyright` does an excellent job at type checking your Python code, \nit doesn\'t check to make sure type hints exist. If you forget to add type hints\nto a function, `pyright` will usually see no problems with it. This tool checks\nto make sure all of your code *has* type hints, while leaving it to `pyright` to make\nsure they are actually correct.\n\n## Installation\n\nPyLeft requires Python 3.6.2+.\n\n`pip install pyleft`\n\n## Usage\n\nPyLeft is a Python module that can be run via `python -m`. Just provide the directories\nor files to recursively check.\n\n`python -m pyleft .`\n\nThe module will exit with an exit code of 0 if all type hints are present, or 1\nif there are any issues.\n\n## Options\n\n- `files`: List of filenames and/or directories to recursively check.\n- `--exclude`: (optional) List of patterns to exclude, in `.gitignore` format. Takes predecence over `files`.\n- `--no-gitignore`: (optional) Don\'t use the exclusions from the .gitignore from the current working directory.\n- `--quiet`: (optional) Don\'t print any output to STDOUT.\n- `--verbose`: (optional) Print debugging information to STDERR.\n\n## Configuration\n\nConfiguration is done through the `pyproject.toml` file.\n\n```toml\n[tool.pyleft]\n# "files" in the configuration file are added to the option given on the command line\n# This can either be a list, or a space separated string\nfiles = ["extra/directory/"]\n# This can either be a list, or a space separated string\nexclude = ["*_pb2.py"]\nno-gitignore = true\nquiet = true\nverbose = true\n```\n\n## Design Decisions\n\nOnly files with a `.py` extension are checked.\n\nThe `__init__` and `__new__` methods of a class are not required to \nhave return type hints. `pyright` automatically assumes this to be `None`.\n\nThe first (`self`) argument of any class method is not required to have a type hint.\n\nThe first (`cls`) argument of any class `@property` or `@classmethod` or `__new__` \nmethod is not required to have a type hint.\n\nAny variable argument list (`*arg`) or keyword argument dict (`**kwarg`) \nis not required to have a type hint.\n\n## Disclaimer\n\nThis project is not affiliated in any way with Microsoft.',
    'author': 'Nathan Vaughn',
    'author_email': 'nvaughn51@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/NathanVaughn/pyleft',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)
