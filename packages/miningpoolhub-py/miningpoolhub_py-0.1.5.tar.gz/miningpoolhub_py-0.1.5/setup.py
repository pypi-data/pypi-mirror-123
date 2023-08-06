# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['miningpoolhub_py']

package_data = \
{'': ['*']}

install_requires = \
['python-dotenv>=0.19.1,<0.20.0', 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'miningpoolhub-py',
    'version': '0.1.5',
    'description': 'A Python wrapper for the Mining Pool Hub REST API',
    'long_description': '# miningpoolhub_py\nA Python wrapper for the Mining Pool Hub REST API\n\n## Install\n`pip install miningpoolhub_py`',
    'author': 'CoryKrol',
    'author_email': '16892390+CoryKrol@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/CoryKrol/miningpoolhub_py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
