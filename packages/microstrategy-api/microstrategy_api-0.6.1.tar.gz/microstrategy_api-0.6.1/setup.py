# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['microstrategy_api',
 'microstrategy_api.microstrategy_selenium',
 'microstrategy_api.mstr_rest_api_facade',
 'microstrategy_api.selenium_driver',
 'microstrategy_api.task_proc']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'microstrategy-api',
    'version': '0.6.1',
    'description': 'Python API library for interacting with MicroStrategy Intelligence Server and/or MicroStrategy Web Server.',
    'long_description': '# MicroStrategy Python API\n\n[![pypi](https://img.shields.io/pypi/v/mstr-python-api.svg)](https://pypi.org/project/config-wrangler/)\n[![license](https://img.shields.io/github/license/arcann/mstr_python_api.svg)](https://github.com/arcann/mstr_python_api/blob/master/license.txt)\n\n\nPython API library for interacting with MicroStrategy Intelligence Server and/or MicroStrategy Web Server.\n\nSupported MicroStrategy sub-APIs\n\n - TaskProc API\n - COM API\n - REST API (Work in progress)\n\n## Installation\n\nInstall using `pip install -U mstr-python-api` or `conda install mstr-python-api -c conda-forge`.\n\n# Examples\n\nSee `examples` folder',
    'author': 'Derek Wood',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/arcann/mstr_python_api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
