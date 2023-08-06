# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ssrfmap', 'ssrfmap.core', 'ssrfmap.handlers', 'ssrfmap.modules']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['ssrfmap = ssrfmap.cli:ssrfmap']}

setup_kwargs = {
    'name': 'levo-ssrfmap',
    'version': '0.1.0',
    'description': 'A packaged version of the SSRFmap CLI tool.',
    'long_description': None,
    'author': 'Akshath Kothari',
    'author_email': 'akshath.kothari@levo.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
