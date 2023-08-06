# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bibscrap', 'bibscrap.cli', 'bibscrap.cli.commands']

package_data = \
{'': ['*']}

install_requires = \
['cleo>=1.0.0a4,<2.0.0', 'scrapy>=2.5.1,<3.0.0', 'single-source>=0.2.0,<0.3.0']

extras_require = \
{'dev': ['black>=21.9b0,<22.0',
         'pre-commit>=2.15.0,<3.0.0',
         'tox>=4.0.0a9,<5.0.0',
         'darglint>=1.8.0,<2.0.0',
         'pytest>=6.2.5,<7.0.0',
         'coverage>=6.0.2,<7.0.0',
         'codecov>=2.1.12,<3.0.0'],
 'docs': ['Sphinx>=4.2.0,<5.0.0',
          'sphinx-rtd-theme>=1.0.0,<2.0.0',
          'sphinxcontrib-bibtex>=2.4.1,<3.0.0']}

entry_points = \
{'console_scripts': ['bibscrap = bibscrap.cli.app:main']}

setup_kwargs = {
    'name': 'bibscrap',
    'version': '0.1.0a1',
    'description': 'Semi-automated tools for systematic literature reviews.',
    'long_description': "========\nbibscrap\n========\n\n.. image:: https://img.shields.io/pypi/v/bibscrap?style=flat\n   :target: https://pypi.org/project/bibscrap/\n   :alt: PyPI version\n\n.. image:: https://app.travis-ci.com/cotterell/bibscrap.svg\n   :target: https://app.travis-ci.com/cotterell/bibscrap\n\n.. image:: https://readthedocs.org/projects/bibscrap/badge/?version=latest\n   :target: https://bibscrap.readthedocs.io/en/latest/\n   :alt: bibscrap's documentation\n\n\n.. image:: https://codecov.io/gh/cotterell/bibscrap/branch/main/graph/badge.svg?token=TQQWS0OQ0E\n   :target: https://codecov.io/gh/cotterell/bibscrap\n   :alt: Code coverage\n\n.. image:: https://img.shields.io/pypi/l/bibscrap.svg\n   :target: https://github.com/cotterell/bibscrap/blob/master/LICENSE.rst\n   :alt: MIT license\n\n.. image:: https://img.shields.io/badge/code%20style-black-161b22.svg\n   :target: https://github.com/psf/black\n   :alt: Code style: black\n\nOverview\n========\n\nThe **bibscrap** package provides semi-automated tools for systematic literature reviews.\n\nRequirements\n============\n\n* Python 3.9+\n\nInstall\n=======\n\nTo install Bibscrap using **pipenv**::\n\n  $ pipenv install --pre bibscrap\n\nTo install Bibscrap using **pip**::\n\n  $ pip install --pre bibscrap\n\nDocumentation\n=============\n\nDocumentation is available online at https://bibscrap.readthedocs.io/ and in the\n``docs`` directory.\n\nContributors: Getting Started\n=============================\n\nTo download the development version of **bibscrap**, follow the instructions\nprovided below::\n\n  $ git clone https://github.com/cotterell/bibscrap.git\n  $ cd bibscrap\n  $ poetry install -v\n\nIf you are part of the **bibscrap** development team, then you should also\ninstall the development packages::\n\n  $ pre-commit install\n\nContributors\n============\n\n=====================  ==========================================================  ============\nContributor            GitHub                                                      Role\n=====================  ==========================================================  ============\nAidan Killer           `@aikill <https://github.com/aikill>`_                      Developer\nJack Solomon           `@jbs26156 <https://github.com/jbs26156>`_                  Developer\nMatthew Pooser         `@mpooser <https://github.com/mpooser>`_                    Developer\nMichael E. Cotterell   `@mepcotterell <https://github.com/mepcotterell>`_          Maintainer\nMitchell Casleton      `@MitchellCasleton <https://github.com/MitchellCasleton>`_  Developer\nMy Nguyen              `@mynguyen0628 <https://github.com/mynguyen0628>`_          Developer\n=====================  ==========================================================  ============\n",
    'author': 'Michael E. Cotterell',
    'author_email': 'mepcotterell@gmail.com',
    'maintainer': 'Michael E. Cotterell',
    'maintainer_email': 'mepcotterell@gmail.com',
    'url': 'https://github.com/cotterell/bibscrap',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
