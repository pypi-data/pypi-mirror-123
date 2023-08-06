# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fourget']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=0.7.0,<0.8.0',
 'arrow>=1.2.0,<2.0.0',
 'attrs>=21.2.0,<22.0.0',
 'httpx==1.0.0b0',
 'tqdm>=4.62.3,<5.0.0',
 'typer>=0.4.0,<0.5.0',
 'yarl>=1.7.0,<2.0.0']

entry_points = \
{'console_scripts': ['fourget = fourget.__main__:app']}

setup_kwargs = {
    'name': 'fourget',
    'version': '0.1.0',
    'description': 'Download/scrape media files from 4chan threads',
    'long_description': None,
    'author': 'Tim Martin',
    'author_email': 'tim@timmart.in',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
