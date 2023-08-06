# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bokehgraph']

package_data = \
{'': ['*']}

install_requires = \
['bokeh>=2.4.1,<3.0.0', 'networkx>=2,<3']

setup_kwargs = {
    'name': 'bokehgraph',
    'version': '0.1.1',
    'description': 'Interactive Graph visualization for networkX Graphs',
    'long_description': None,
    'author': 'Lukas Erhard',
    'author_email': 'luerhard@googlemail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
