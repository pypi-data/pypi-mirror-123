# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['flosy']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8.2,<2.0.0']

extras_require = \
{'docs': ['sphinx<4',
          'sphinx-rtd-theme>=0.5.2,<0.6.0',
          'sphinx-autodoc-typehints>=1.12.0,<2.0.0']}

setup_kwargs = {
    'name': 'flosy',
    'version': '0.0.1',
    'description': 'A fastApi based osquery management adapter with Loki persistence',
    'long_description': None,
    'author': 'Eduard Thamm',
    'author_email': 'eduard.thamm@prisma-capacity.eu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
