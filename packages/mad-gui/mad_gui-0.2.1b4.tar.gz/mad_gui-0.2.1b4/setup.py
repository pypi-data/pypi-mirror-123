# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mad_gui',
 'mad_gui.components',
 'mad_gui.components.dialogs',
 'mad_gui.components.dialogs.plugin_selection',
 'mad_gui.config',
 'mad_gui.models',
 'mad_gui.models.local',
 'mad_gui.plot_tools.labels',
 'mad_gui.plot_tools.plots',
 'mad_gui.plugins',
 'mad_gui.qt_designer',
 'mad_gui.utils',
 'mad_gui.windows']

package_data = \
{'': ['*'], 'mad_gui.qt_designer': ['images/*']}

install_requires = \
['PySide2==5.15.1',
 'pandas',
 'pyqtgraph==0.11.0',
 'typing-extensions>=3.10.0,<4.0.0']

entry_points = \
{'console_scripts': ['mad-gui = mad_gui:start_gui']}

setup_kwargs = {
    'name': 'mad-gui',
    'version': '0.2.1b4',
    'description': 'GUI for annotating and processing IMU data.',
    'long_description': '# MaD GUI\n**M**achine Learning \n**a**nd \n**D**ata Analytics \n**G**raphical \n**U**ser \n**I**nterface\n\n[![Test and Lint](https://github.com/mad-lab-fau/mad-gui/workflows/Test%20and%20Lint/badge.svg)](https://github.com/mad-lab-fau/mad-gui/actions/workflows/test_and_lint.yml)\n[![CodeFactor](https://www.codefactor.io/repository/github/mad-lab-fau/mad-gui/badge/main)](https://www.codefactor.io/repository/github/mad-lab-fau/mad-gui/overview/main)\n[![Documentation Status](https://readthedocs.org/projects/mad-gui/badge/?version=latest)](https://mad-gui.readthedocs.io/en/latest/?badge=latest)\n\n\n[![PyPI version shields.io](https://img.shields.io/pypi/v/mad-gui)](https://pypi.org/project/mad-gui/)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/mad-gui)\n\n![GitHub all releases](https://img.shields.io/github/downloads/mad-lab-fau/mad-gui/total?style=social)\n\n## What is it?\nThe MaD GUI is a framework for processing time series data. Its use-cases include visualization, annotation (manual or automated), and algorithmic processing of visualized data and annotations. More information:\n\n - [Documentation](https://mad-gui.readthedocs.io/en/latest/README.html) \n - [Github Repository](https://github.com/mad-lab-fau/mad-gui)\n - [YouTube Playlist](https://www.youtube.com/watch?v=akxcuFOesC8&list=PLf4GpKhBjGcswKIkNeahNt5nDxt8oXPue)\n',
    'author': 'Malte Ollenschlaeger',
    'author_email': 'malte.ollenschlaeger@fau.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mad-lab-fau/mad-gui',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<3.10',
}


setup(**setup_kwargs)
