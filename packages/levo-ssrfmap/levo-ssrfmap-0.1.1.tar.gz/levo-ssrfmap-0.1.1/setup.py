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
    'version': '0.1.1',
    'description': 'A packaged version of the SSRFmap CLI tool.',
    'long_description': None,
    'author': 'Swissky',
    'author_email': None,
    'maintainer': 'Akshath Kothari',
    'maintainer_email': 'akshath.kothari@levo.ai',
    'url': 'https://github.com/levoai/SSRFmap',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
