# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kyujipy']

package_data = \
{'': ['*']}

install_requires = \
['cson>=0.8,<0.9', 'poetry>=1.1.11,<2.0.0']

setup_kwargs = {
    'name': 'kyujipy',
    'version': '0.5.6',
    'description': 'A Python library to convert Japanese texts from Shinjitai to Kyujitai and vice versa',
    'long_description': '# kyujipy\n\n[![PyPI version](https://badge.fury.io/py/kyujipy.svg)](https://badge.fury.io/py/kyujipy)\n\n[kyujipy](https://github.com/DrTurnon/kyujipy) is a  Python library to convert Japanese texts from\n[Shinjitai](https://en.wikipedia.org/wiki/Shinjitai) (新字体) to\n[Kyūjitai](https://en.wikipedia.org/wiki/Ky%C5%ABjitai), (舊字體) and vice versa.\n\n[kyujipy](https://github.com/DrTurnon/kyujipy) is based on the\n[kyujitai.js](https://github.com/hakatashi/kyujitai.js) project, originally authored by\n[Koki Takahashi](https://github.com/hakatashi).\n\n\n## Installation (via [Pip](http://www.pip-installer.org/))\n\n    $ pip install kyujipy\n\n\n## Usage\n\nIn Python shell (or inside Python script):\n\n    \n    # Import main class\n    >>> from kyujipy import KyujitaiConverter\n    \n    # Instantiate Shinjitai <-> Kyujitai converter\n    >>> converter = KyujitaiConverter()\n    \n    # Convert a text from Shinjitai to Kyujitai\n    >>> print(converter.shinjitai_to_kyujitai("新字体"))\n    新字體\n    \n    # Convert a text from Kyujitai to Shinjitai\n    >>> print(converter.kyujitai_to_shinjitai("舊字體"))\n    旧字体\n\n\n## API Reference\n\n* __shinjitai_to_kyujitai(string)__\n\nConvert a text from Shinjitai (新字体) to Kyūjitai (舊字體)\n\n* __kyujitai_to_shinjitai(string)__\n\nConvert a text from Kyūjitai (舊字體) to Shinjitai (新字体)\n\n\n## License\n\n[kyujipy](https://github.com/DrTurnon/kyujipy) is licensed under the MIT license.\n\n© 2017-2021 [Emmanuel Ternon](https://github.com/DrTurnon)\n',
    'author': 'Emmanuel Ternon',
    'author_email': 'emmanuel.ternon@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DrTurnon/kyujipy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
