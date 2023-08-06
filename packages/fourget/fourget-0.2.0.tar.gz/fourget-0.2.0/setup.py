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
    'version': '0.2.0',
    'description': 'Download/scrape media files from 4chan threads',
    'long_description': '# fourget\n\nDownload/scrape media files from 4chan threads\n\n![Demo](https://raw.githubusercontent.com/t-mart/fourget/master/docs/demo.gif)\n\n## Features\n\n- fast concurrent downloading with asyncio\n- skip download if already it already exists locally\n- progress bar\n\n## Example\n\n```shell\n$ fourget https://boards.4channel.org/g/thread/76759434\n```\n\n```shell\n$ fourget --help\n```\n\n## Installation\n\n```shell\n$ pip install fourget\n```\n\n## Releasing\n\n1. Bump the version number in `pyproject.toml`.\n2. Commit and tag with version number.\n\n   ```shell\n   # for example, if new version is 1.2.3\n   $ git commit -m "Bump version to 1.2.3"\n   $ git tag -a "1.2.3" -m "1.2.3"\n   ```\n\n3. Run `poetry publish --build`. (Will need to have configured PYPI token)\n',
    'author': 'Tim Martin',
    'author_email': 'tim@timmart.in',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/t-mart/fourget',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
