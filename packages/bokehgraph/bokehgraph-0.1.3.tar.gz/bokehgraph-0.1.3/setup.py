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
    'version': '0.1.3',
    'description': 'Interactive Graph visualization for networkX Graphs',
    'long_description': '# bokeh-graph\nInteractive Graph visualization for networkX Graphs\n\n# Basic Usage\n```python\nfrom bokehgraph import BokehGraph\nimport networkx as nx\n\ngraph = nx.karate_club_graph()\n\nplot = BokehGraph(graph)\nplot.draw()\n```\n\n## Jupyter Notebooks\nTo show graphs inlined in Jupyter Notebooks set the `inline` parameter\n```python\nplot = BokehGraph(graph, width=300, height=300, inline=True)\n```\n\n## Draw parameters\n\nThe `BokehGraph.draw()` method has a couple of parameters to individualize the resulting plot:\n```\nnode_color="firebrick"\nSet node color to any valid bokeh color (only respected if color_by is not set)\n\npalette=None\nSet palette to any valid bokeh color palette.\nA list of palettes can be found under: https://docs.bokeh.org/en/latest/docs/reference/palettes.html\n\ncolor_by=None\nSet to a node attribute to color nodes by this attribute\n\nedge_color="navy"\nSet node color to any valid bokeh color\n\nedge_alpha=0.17\nSet edge alpha to a value between [0,1]\n\nnode_alpha=0.7\nSet edge alpha to a value between [0,1]\n\nnode_size=9\nSet node size\n\nmax_colors=-1\nSet a maximum number of colors for color_by (or -1 to use as many colors as possible).\nThis must be < 256 and lower than the maximum number of colors of your selected palette.\nIt will divide the attribute space into evenly spaced to colors.\n```',
    'author': 'Lukas Erhard',
    'author_email': 'luerhard@googlemail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/luerhard/bokehgraph',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
