# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dizzle']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.25,<2.0.0',
 'icecream>=2.1.1,<3.0.0',
 'openpyxl>=3.0.9,<4.0.0',
 'orjson>=3.6.4,<4.0.0',
 'pandas>=1.3.3,<2.0.0',
 'python-dotenv>=0.19.0,<0.20.0',
 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'dizzle',
    'version': '0.2.0',
    'description': 'Tools to normalize and interact with data of various formats.',
    'long_description': '# dizzle\n\n![dizzle.png](https://raw.githubusercontent.com/4thel00z/logos/master/dizzle.png)\n\n## Motivation\n\nThis is the place where I store handy helpers to normalize data or handle them\nin regards to databases etc.\n\n## License\n\nThis project is licensed under the GPL-3 license.\n',
    'author': '4thel00z',
    'author_email': '4thel00z@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/4thel00z/dizzle',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
