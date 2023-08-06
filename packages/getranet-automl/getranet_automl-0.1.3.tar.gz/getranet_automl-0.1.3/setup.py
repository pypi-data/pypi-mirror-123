# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['getranet_automl',
 'getranet_automl.exceptions',
 'getranet_automl.speech',
 'getranet_automl.storage',
 'getranet_automl.translate']

package_data = \
{'': ['*']}

install_requires = \
['google-cloud-speech>=2.9.3,<3.0.0',
 'google-cloud-storage>=1.42.3,<2.0.0',
 'google-cloud-translate>=3.4.1,<4.0.0',
 'pydub>=0.25.1,<0.26.0',
 'python-docx>=0.8.11,<0.9.0',
 'srt>=3.5.0,<4.0.0',
 'starlette>=0.16.0,<0.17.0']

setup_kwargs = {
    'name': 'getranet-automl',
    'version': '0.1.3',
    'description': 'Wrapper for important language-centric Google APIs',
    'long_description': None,
    'author': 'GeTraNet',
    'author_email': 'dev@getranet.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
