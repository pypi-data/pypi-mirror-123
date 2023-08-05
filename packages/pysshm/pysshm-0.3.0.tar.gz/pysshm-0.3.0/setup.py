# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pysshm']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.18.58,<2.0.0',
 'click>=8.0.3,<9.0.0',
 'loguru>=0.5.3,<0.6.0',
 'pick>=1.0.0,<2.0.0']

entry_points = \
{'console_scripts': ['sshm = pysshm.cli:run']}

setup_kwargs = {
    'name': 'pysshm',
    'version': '0.3.0',
    'description': 'SSM shell client, the python way',
    'long_description': None,
    'author': 'Pierre-Yves Gillier',
    'author_email': 'github@pygillier.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
