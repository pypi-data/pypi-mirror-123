# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nametable']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.21.2,<2.0.0']

setup_kwargs = {
    'name': 'nametable',
    'version': '0.1.2',
    'description': 'An OOP approach to represent nametables on the NES',
    'long_description': '``nametable`` serves to bridge the gap between \n[Nintendo Entertainment System\'s](https://en.wikipedia.org/wiki/Nintendo_Entertainment_System)\n[Picture Processing Unit\'s](https://wiki.nesdev.org/w/index.php/PPU)\n[nametables](https://wiki.nesdev.org/w/index.php?title=PPU_nametables) and Python.\n\nIts main goal is to create an [Object Oriented](https://en.wikipedia.org/wiki/Object-oriented_programming)\napproach to represent a nametable on the NES.\n\nIt provides the ability to create instances of Pattern and Block directly from memory and inserts them into PatternTable and Nametable, respectively.\n\n```python\n    >>> import nametable\n\n    >>> pattern = nametable.PatternMeta(bytes.fromhex("41 C2 44 48 10 20 40 80 01 02 04 08 16 21 42 87"))\n    >>> pattern.numpy_array\n    array(\n        [\n            [0, 1, 0, 0, 0, 0, 0, 3],\n            [1, 1, 0, 0, 0, 0, 3, 0],\n            [0, 1, 0, 0, 0, 3, 0, 0],\n            [0, 1, 0, 0, 3, 0, 0, 0],\n            [0, 0, 0, 3, 0, 2, 2, 0],\n            [0, 0, 3, 0, 0, 0, 0, 2],\n            [0, 3, 0, 0, 0, 0, 2, 0],\n            [3, 0, 0, 0, 0, 2, 2, 2],\n        ],\n        dtype=ubyte,\n    )\n\n    >>> pattern_table = nametable.PatternTable((nametable.Pattern(pattern),))\n    >>> block = nametable.Block(pattern_table, (0, 0, 0, 0))\n    >>> block.numpy_array\n    array(\n        [\n            [0, 1, 0, 0, 0, 0, 0, 3, 0, 1, 0, 0, 0, 0, 0, 3],\n            [1, 1, 0, 0, 0, 0, 3, 0, 1, 1, 0, 0, 0, 0, 3, 0],\n            [0, 1, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0, 0, 3, 0, 0],\n            [0, 1, 0, 0, 3, 0, 0, 0, 0, 1, 0, 0, 3, 0, 0, 0],\n            [0, 0, 0, 3, 0, 2, 2, 0, 0, 0, 0, 3, 0, 2, 2, 0],\n            [0, 0, 3, 0, 0, 0, 0, 2, 0, 0, 3, 0, 0, 0, 0, 2],\n            [0, 3, 0, 0, 0, 0, 2, 0, 0, 3, 0, 0, 0, 0, 2, 0],\n            [3, 0, 0, 0, 0, 2, 2, 2, 3, 0, 0, 0, 0, 2, 2, 2],\n            [0, 1, 0, 0, 0, 0, 0, 3, 0, 1, 0, 0, 0, 0, 0, 3],\n            [1, 1, 0, 0, 0, 0, 3, 0, 1, 1, 0, 0, 0, 0, 3, 0],\n            [0, 1, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0, 0, 3, 0, 0],\n            [0, 1, 0, 0, 3, 0, 0, 0, 0, 1, 0, 0, 3, 0, 0, 0],\n            [0, 0, 0, 3, 0, 2, 2, 0, 0, 0, 0, 3, 0, 2, 2, 0],\n            [0, 0, 3, 0, 0, 0, 0, 2, 0, 0, 3, 0, 0, 0, 0, 2],\n            [0, 3, 0, 0, 0, 0, 2, 0, 0, 3, 0, 0, 0, 0, 2, 0],\n            [3, 0, 0, 0, 0, 2, 2, 2, 3, 0, 0, 0, 0, 2, 2, 2],\n        ],\n        dtype=ubyte,\n    )\n\n    >>> nametable.Nametable((block,))\n    Nametable(Block(PatternTable((Pattern(PatternMeta(...)),)), (0, 0, 0, 0)),)\n```\n\nGetting Help\n============\n\nPlease use the ``python-nametable`` tag on \n[StackOverflow](https://stackoverflow.com/questions/tagged/python-nametable) to get help.\n\nAiding others and answers questions is a fantastic way to help!\n\nProject Information\n===================\n\n``nametable`` is released under the\n[GPL3](https://tldrlegal.com/license/gnu-general-public-license-v3-(gpl-3)) license.\nIts documentation is hosted on [Github](https://thejoesmo.github.io/nametable/) and the\nrepository is hosted on [Github](https://github.com/TheJoeSmo/nametable).  The latest release\nis hosted on [PyPI](https://pypi.org/project/nametable/).  \n',
    'author': 'TheJoeSmo',
    'author_email': 'joesmo.joesmo12@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9.0,<3.11',
}


setup(**setup_kwargs)
