# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['task_status']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0', 'python-dateutil>=2.8.2,<3.0.0']

entry_points = \
{'console_scripts': ['task-status = task_status.task_status:main']}

setup_kwargs = {
    'name': 'task-status',
    'version': '0.2.3',
    'description': 'Utility to get status data built from taskwarrior',
    'long_description': None,
    'author': 'Alex Kelly',
    'author_email': 'alex.kelly@franklin.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
