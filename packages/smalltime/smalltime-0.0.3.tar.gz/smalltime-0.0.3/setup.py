# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['smalltime']

package_data = \
{'': ['*']}

install_requires = \
['ansicolors>=1.1.8,<2.0.0', 'shortuuid>=1.0.1,<2.0.0']

entry_points = \
{'console_scripts': ['st = smalltime.cli:main']}

setup_kwargs = {
    'name': 'smalltime',
    'version': '0.0.3',
    'description': 'A small python timing package for a packaging demonstration',
    'long_description': '# smalltime\n\n<p align="center">\n    <img src="https://github.com/nicklambourne/smalltime/raw/master/docs/source/_static/img/smalltime.png" width="250px"/>\n</p>\n\n---\n\n![GitHub](https://img.shields.io/github/license/nicklambourne/smalltime)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/smalltime)]()\n![PyPI](https://img.shields.io/pypi/v/smalltime)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/smalltime)\n[![Test](https://github.com/nicklambourne/smalltime/actions/workflows/test.yml/badge.svg)](https://github.com/nicklambourne/smalltime/actions/workflows/test.yml)\n[![codecov](https://codecov.io/gh/nicklambourne/smalltime/branch/master/graph/badge.svg?token=QBZ9WK9PFA)](https://codecov.io/gh/nicklambourne/smalltime)\n[![Read the Docs](https://img.shields.io/readthedocs/smalltime)](https://smalltime.readthedocs.io/en/latest/)\n<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>\n\n## What is it?\n`smalltime` is a quick and dirty library for timing Python function, sections of code and arbitrary programs on the command line.\n\n---\n\n## Requirements\n`smalltime` requires Python >= 3.6.2.\n\nSee [`pyproject.toml`](https://github.com/nicklambourne/smalltime/blob/master/pyproject.toml) for dependencies and dev dependencies.\n\n---\n\n## Installation\n\nVia [`poetry`](https://python-poetry.org/):\n```bash\npoetry add smalltime\n```\n\nVia `pip`:\n```bash\npip install smalltime\n```\n\n---\n\n## Basic Usage\n### In Python Code\n#### In-Line\n```python\nimport smalltime\n\ntimer = smalltime.Timer(name="hello world timer")\ntimer.start()\nprint("Hello, ", end="")\nprint("World!")\ntimer.stop()\n```\n\n#### Via Decorator\n```python\nimport smalltime\nimport subprocess\n\n@smalltime.timed(name="thing_timer")\ndef thing_you_want_to_time():\n    subprocess.call(["python", "-c", "\\"import this\\""])\n\n\nthing_you_want_to_time()\n```\n\n### From the Command Line\nN.B.: Assumes installation via Poetry and an active [Poetry shell](https://python-poetry.org/docs/cli/#shell).\n```bash\n# Usage: st <program> [args]\nst sleep 10\nStarting counter (BNM8rBqP)\nCounter stopped (BNM8rBqP): 10007777130ns elapsed\n```\n\n---\n\n## Can I use this in my project?\nYes, please do! The code is all open source and BSD-3-Clause licensed.\n\n---',
    'author': 'nicklambourne',
    'author_email': 'dev@ndl.im',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
