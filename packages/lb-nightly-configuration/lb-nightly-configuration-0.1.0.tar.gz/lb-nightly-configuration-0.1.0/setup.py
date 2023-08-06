# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lb', 'lb.nightly.configuration']

package_data = \
{'': ['*']}

install_requires = \
['gitpython>=3.1.3,<4.0.0', 'pyyaml>=5.3.1,<6.0.0', 'tabulate>=0.8.7,<0.9.0']

entry_points = \
{'console_scripts': ['lbn-check-config = lb.nightly.configuration:check_config']}

setup_kwargs = {
    'name': 'lb-nightly-configuration',
    'version': '0.1.0',
    'description': 'configuration of the LHCb Nightly Build System',
    'long_description': None,
    'author': 'Marco Clemencic',
    'author_email': 'marco.clemencic@cern.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
