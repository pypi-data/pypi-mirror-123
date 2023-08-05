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
{'console_scripts': ['pysshm = pysshm.cli:run']}

setup_kwargs = {
    'name': 'pysshm',
    'version': '0.3.3',
    'description': 'SSM shell client, the python way',
    'long_description': '# pysshm\n\nConnect to a SSM session directly in your favorite terminal.\n\n## Install\n\nIn your terminal, run:\n\n```bash\n$ pip install pysshm\n```\n\nIn order to fully use pysshm, you **MUST** install the [session-manager-plugin](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html) from AWS.\n\n## Usage\n\n```bash\n$ pysshm --help\nUsage: pysshm [OPTIONS]\n\n  Connect to an EC2 instance over SSM, all in your favorite shell.\n\nOptions:\n  -p, --profile TEXT      AWS profile\n  -r, --region TEXT       AWS region (default: eu-west-3)\n  -i, --instance-id TEXT  Instance ID for direct connect\n  -d, --debug             Enable debug\n  --help                  Show this message and exit.\n```\n',
    'author': 'Pierre-Yves Gillier',
    'author_email': 'github@pygillier.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pygillier/pysshm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
