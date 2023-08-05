# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['csc_recorder']

package_data = \
{'': ['*'], 'csc_recorder': ['CSC/templates/*']}

install_requires = \
['Jinja2>=3.0.2,<4.0.0', 'requests>=2.26.0,<3.0.0', 'xmltodict>=0.12.0,<0.13.0']

setup_kwargs = {
    'name': 'csc-recorder',
    'version': '0.1.2',
    'description': 'CSC eRecording python wrapper',
    'long_description': '',
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Lenders-Cooperative/CSCRecorder',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
