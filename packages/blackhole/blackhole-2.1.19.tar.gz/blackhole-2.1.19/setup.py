# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['blackhole']

package_data = \
{'': ['*']}

extras_require = \
{'dev': ['uvloop>=0.14.0,<0.15.0',
         'setproctitle>=1.1.10,<2.0.0',
         'coverage>=5.1,<6.0',
         'pytest>=5.4.2,<6.0.0',
         'pytest-asyncio>=0.12.0,<0.13.0',
         'pytest-cov>=2.8.1,<3.0.0',
         'pytest-clarity>=0.3.0-alpha.0,<0.4.0',
         'sphinx>=3.0.3,<4.0.0',
         'guzzle_sphinx_theme>=0.7.11,<0.8.0',
         'tox>=3.15.0,<4.0.0',
         'pre-commit>=2.4.0,<3.0.0',
         'interrogate>=1.3.0,<2.0.0',
         'pyroma>=2.6,<3.0',
         'bandit>=1.6.2,<2.0.0',
         'black>=20.8b1,<21.0',
         'flake8>=3.8.3,<4.0.0',
         'flake8-bugbear>=20.1.4,<21.0.0',
         'flake8-isort>=4.0.0,<5.0.0',
         'flake8-commas>=2.0.0,<3.0.0',
         'pydocstyle>=5.1.0,<6.0.0',
         'doc8>=0.8.1,<0.9.0',
         'codespell>=2.1.0,<3.0.0',
         'vulture>=2.3,<3.0'],
 'docs': ['sphinx>=3.0.3,<4.0.0', 'guzzle_sphinx_theme>=0.7.11,<0.8.0'],
 'setproctitle': ['setproctitle>=1.1.10,<2.0.0'],
 'tests': ['coverage>=5.1,<6.0',
           'pytest>=5.4.2,<6.0.0',
           'pytest-asyncio>=0.12.0,<0.13.0',
           'pytest-cov>=2.8.1,<3.0.0',
           'pytest-clarity>=0.3.0-alpha.0,<0.4.0',
           'interrogate>=1.3.0,<2.0.0',
           'pyroma>=2.6,<3.0',
           'bandit>=1.6.2,<2.0.0',
           'black>=20.8b1,<21.0',
           'flake8>=3.8.3,<4.0.0',
           'flake8-bugbear>=20.1.4,<21.0.0',
           'flake8-isort>=4.0.0,<5.0.0',
           'flake8-commas>=2.0.0,<3.0.0',
           'pydocstyle>=5.1.0,<6.0.0',
           'doc8>=0.8.1,<0.9.0',
           'codespell>=2.1.0,<3.0.0',
           'vulture>=2.3,<3.0'],
 'uvloop': ['uvloop>=0.14.0,<0.15.0']}

entry_points = \
{'console_scripts': ['blackhole = blackhole.application:run',
                     'blackhole_config = '
                     'blackhole.application:blackhole_config']}

setup_kwargs = {
    'name': 'blackhole',
    'version': '2.1.19',
    'description': 'Blackhole is an MTA (message transfer agent) that (figuratively) pipes all mail to /dev/null.',
    'long_description': "=========\nBlackhole\n=========\n\n.. image:: https://img.shields.io/github/workflow/status/kura/blackhole/CI?style=for-the-badge&label=tests&logo=githubactions\n    :target: https://github.com/kura/blackhole/actions/workflows/ci.yml\n    :alt: Build status of the master branch\n\n.. image:: https://img.shields.io/codecov/c/github/kura/blackhole/master.svg?style=for-the-badge&label=coverage&logo=codecov\n    :target: https://codecov.io/github/kura/blackhole/\n    :alt: Test coverage\n\nBlackhole is an `MTA (message transfer agent)\n<https://en.wikipedia.org/wiki/Message_transfer_agent>`_ that (figuratively)\npipes all mail to /dev/null, built on top of `asyncio\n<https://docs.python.org/3/library/asyncio.html>`_ and utilises `async def <https://docs.python.org/3/reference/compound_stmts.html#async-def>`_\nand `await\n<https://docs.python.org/3/reference/expressions.html#await>`_ statements\navailable in `Python 3.5 <https://docs.python.org/3/whatsnew/3.5.html>`_.\n\nWhile Blackhole is an MTA, none of the actions performed via SMTP or SMTPS are\nactually processed, and no email is delivered. You can tell Blackhole how to\nhandle mail that it receives. It can accept all of it, bounce it all, or\nrandomly do either of those two actions.\n\nThink of Blackhole sort of like a honeypot in terms of how it handles mail, but\nit's specifically designed with testing in mind.\n\nPython support\n==============\n\n- Python 3.7+\n- PyPy 3.7+\n- Pyston 2.2+\n\nDocumentation\n=============\n\nYou can find the latest documentation `here\n<https://kura.gg/blackhole/>`_.\n\nIf you would like to contribute, please read the `contributors guide\n<https://kura.gg/blackhole/overview.html#contributing>`_.\n\nThe latest build status on GitHub `<https://github.com/kura/blackhole/actions/workflows/ci.yml>`_.\n\nAnd the test coverage report on `codecov\n<https://codecov.io/github/kura/blackhole/>`_.\n\nChangelog\n=========\n\nYou can find a list of changes `on the\nblackhole website <https://kura.gg/blackhole/changelog.html>`_.\n",
    'author': 'Kura',
    'author_email': 'kura@kura.gg',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://kura.gg/blackhole/',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>3.7,<4',
}


setup(**setup_kwargs)
