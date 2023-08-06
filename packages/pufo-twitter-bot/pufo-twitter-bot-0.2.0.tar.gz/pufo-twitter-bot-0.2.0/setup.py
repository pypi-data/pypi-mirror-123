# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pufo_twitter_bot',
 'pufo_twitter_bot.authors',
 'pufo_twitter_bot.books',
 'pufo_twitter_bot.bot']

package_data = \
{'': ['*'], 'pufo_twitter_bot': ['data/*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0',
 'click>=7.0,<8.0',
 'desert>=2020.11.18,<2021.0.0',
 'marshmallow>=3.11.1,<4.0.0',
 'requests>=2.25.1,<3.0.0',
 'tweepy>=3.10.0,<4.0.0']

entry_points = \
{'console_scripts': ['pufo-twitter-bot = pufo_twitter_bot.__main__:main']}

setup_kwargs = {
    'name': 'pufo-twitter-bot',
    'version': '0.2.0',
    'description': 'Pufo Twitter Bot',
    'long_description': "Pufo Twitter Bot 🛸\n====================\n\n|PyPI| |Python Version| |License|\n\n|Read the Docs| |Tests| |Codecov|\n\n|pre-commit| |Black|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/pufo-twitter-bot.svg\n   :target: https://pypi.org/project/pufo-twitter-bot/\n   :alt: PyPI\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/pufo-twitter-bot\n   :target: https://pypi.org/project/pufo-twitter-bot\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/pypi/l/pufo-twitter-bot\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/pufo-twitter-bot/latest.svg?label=Read%20the%20Docs\n   :target: https://pufo-twitter-bot.readthedocs.io/\n   :alt: Read the documentation at https://pufo-twitter-bot.readthedocs.io/\n.. |Tests| image:: https://github.com/mjt91/pufo-twitter-bot/workflows/Tests/badge.svg\n   :target: https://github.com/mjt91/pufo-twitter-bot/actions?workflow=Tests\n   :alt: Tests\n.. |Codecov| image:: https://codecov.io/gh/mjt91/pufo-twitter-bot/branch/main/graph/badge.svg\n   :target: https://codecov.io/gh/mjt91/pufo-twitter-bot\n   :alt: Codecov\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n\n\nFeatures 🚀\n-----------\nThis is an command-line app to create randomly created book titles to author combinations.\nThe interface provides the possibility to tweet the list on twitter.\n\n* Creates a list of random book titels and author combinations\n* Parameters to tune are\n   * `count` for number of author/titles\n   * `gender` for the gender of the authors\n\nBook titles are in german for now. Multilanguage support maybe coming in the future.\n\n\nRequirements 📋\n---------------\n\n* python>=3.7,<3.10\n* twitter devloper account (to post to twitter)\n\n\nInstallation 🔨\n----------------\n\nYou can install *Pufo Twitter Bot* via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install pufo-twitter-bot\n\n\nUsage\n-----\n\nBasic usage:\n\n.. code:: console\n\n   $ pufo-twitter-bot --count 2 --gender m\n   >> 1. Der Büffel - Florentin Titze\n   >> 2. Platte Tüte - Stefan Will\n\nPlease see the `Command-line Reference <Usage_>`_ for details.\n\n\nContributing\n------------\n\nContributions are very welcome.\nTo learn more, see the `Contributor Guide`_.\n\n\nLicense\n-------\n\nDistributed under the terms of the `MIT license`_,\n*Pufo Twitter Bot* is free and open source software.\n\n\nIssues 📌\n---------\n\nIf you encounter any problems,\nplease `file an issue`_ along with a detailed description.\n\n\nCredits\n-------\n\nRandom book titles are taken from `buchtitelgenerator.de`_\nThis project would not be possible without the authors of this site for\nletting me use their data. Herewith I express my deepest thanks.\n\nRandom author names generated from two origins:\n\n* randomname.de_\n* offenedaten-koeln_\n\nThe names data is distributed under the Creative Commons license (see: `cc licenses`_)\n\n\nSupport\n-------\n\nGet me a `coffee`_ ☕  or `beer`_ 🍺\n\n\nThis project was generated from `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_ template.\n\n.. _cc licenses: https://github.com/santisoler/cc-licenses\n.. _buchtitelgenerator.de: https://www.buchtitelgenerator.de/\n.. _randomname.de: https://randomname.de/\n.. _offenedaten-koeln: https://offenedaten-koeln.de/\n.. _@cjolowicz: https://github.com/cjolowicz\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _MIT license: https://opensource.org/licenses/MIT\n.. _PyPI: https://pypi.org/\n.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _file an issue: https://github.com/mjt91/pufo-twitter-bot/issues\n.. _pip: https://pip.pypa.io/\n.. _beer: https://www.buymeacoffee.com/mjt91\n.. _coffee: https://www.buymeacoffee.com/mjt91\n.. github-only\n.. _Contributor Guide: CONTRIBUTING.rst\n.. _Usage: https://pufo-twitter-bot.readthedocs.io/en/latest/usage.html\n",
    'author': 'Marius Theiss',
    'author_email': 'justusbersten@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mjt91/pufo-twitter-bot',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
