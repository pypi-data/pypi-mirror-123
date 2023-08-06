# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lk_qtquick_scaffold',
 'lk_qtquick_scaffold.experimental_features',
 'lk_qtquick_scaffold.pyside',
 'lk_qtquick_scaffold.qmlside',
 'lk_qtquick_scaffold.qmlside.hot_loader',
 'lk_qtquick_scaffold.qmlside.layout_helper']

package_data = \
{'': ['*'],
 'lk_qtquick_scaffold': ['theme/LightClean/*',
                         'theme/LightClean/LCBackground/*',
                         'theme/LightClean/LCButtons/*',
                         'theme/LightClean/LCStyle/*',
                         'theme/LightClean/rss/*']}

install_requires = \
['lk-lambdex', 'lk-logger', 'lk-utils', 'pyside6']

setup_kwargs = {
    'name': 'lk-qtquick-scaffold',
    'version': '1.0.0',
    'description': 'A flexible toolset for improving QML coding experience in PySide6 development.',
    'long_description': None,
    'author': 'Likianta',
    'author_email': 'likianta@foxmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
