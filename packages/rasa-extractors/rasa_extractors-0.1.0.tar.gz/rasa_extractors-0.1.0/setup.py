# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rasa_extractors']

package_data = \
{'': ['*']}

install_requires = \
['flashtext>=2.7,<3.0', 'rasa==2.8.4']

setup_kwargs = {
    'name': 'rasa-extractors',
    'version': '0.1.0',
    'description': '',
    'long_description': '# rasa_extractors\n\n## Motivation\n\nProvide a dumpyard for rasa extractors without annoying dependencies.\n\n## License\n\nThis project is licensed under the MIT license.\n',
    'author': '4thel00z',
    'author_email': '4thel00z@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/4thel00z/rasa_extractors',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
