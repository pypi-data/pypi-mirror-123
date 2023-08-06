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
    'version': '0.1.1',
    'description': 'An OOP approach to represent nametables on the NES',
    'long_description': '\n\n.. purpose-statement-begin\n\n``nametable`` serves to bridge the gap between \n`Nintendo Entertainment System\'s <https://en.wikipedia.org/wiki/Nintendo_Entertainment_System>`_\n`Picture Processing Unit\'s <https://wiki.nesdev.org/w/index.php/PPU>`_\n`nametables <https://wiki.nesdev.org/w/index.php?title=PPU_nametables>`_ and Python.\n\nIts main goal is to create an `Object Oriented <https://en.wikipedia.org/wiki/Object-oriented_programming>`_\napproach to represent a nametable on the NES.\n\n.. purpose-statement-end\n\nIt provides the ability to create instances of \n:class:`~nametable.Pattern.Pattern` and :class:`~nametable.Block.Block` directly from memory \nand insert them into :class:`~nametable.PatternTable.PatternTable` and\n:class:`~nametable.Nametable.Nametable`, respectively.\n\n.. code-begin\n\n.. code-block:: python\n\n    >>> import nametable\n\n    >>> pattern = nametable.PatternMeta(bytes.fromhex("41 C2 44 48 10 20 40 80 01 02 04 08 16 21 42 87"))\n    >>> pattern.numpy_array\n    array(\n        [\n            [0, 1, 0, 0, 0, 0, 0, 3],\n            [1, 1, 0, 0, 0, 0, 3, 0],\n            [0, 1, 0, 0, 0, 3, 0, 0],\n            [0, 1, 0, 0, 3, 0, 0, 0],\n            [0, 0, 0, 3, 0, 2, 2, 0],\n            [0, 0, 3, 0, 0, 0, 0, 2],\n            [0, 3, 0, 0, 0, 0, 2, 0],\n            [3, 0, 0, 0, 0, 2, 2, 2],\n        ],\n        dtype=ubyte,\n    )\n\n    >>> pattern_table = nametable.PatternTable((nametable.Pattern(pattern),))\n    >>> block = nametable.Block(pattern_table, (0, 0, 0, 0))\n    >>> block.numpy_array\n    array(\n        [\n            [0, 1, 0, 0, 0, 0, 0, 3, 0, 1, 0, 0, 0, 0, 0, 3],\n            [1, 1, 0, 0, 0, 0, 3, 0, 1, 1, 0, 0, 0, 0, 3, 0],\n            [0, 1, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0, 0, 3, 0, 0],\n            [0, 1, 0, 0, 3, 0, 0, 0, 0, 1, 0, 0, 3, 0, 0, 0],\n            [0, 0, 0, 3, 0, 2, 2, 0, 0, 0, 0, 3, 0, 2, 2, 0],\n            [0, 0, 3, 0, 0, 0, 0, 2, 0, 0, 3, 0, 0, 0, 0, 2],\n            [0, 3, 0, 0, 0, 0, 2, 0, 0, 3, 0, 0, 0, 0, 2, 0],\n            [3, 0, 0, 0, 0, 2, 2, 2, 3, 0, 0, 0, 0, 2, 2, 2],\n            [0, 1, 0, 0, 0, 0, 0, 3, 0, 1, 0, 0, 0, 0, 0, 3],\n            [1, 1, 0, 0, 0, 0, 3, 0, 1, 1, 0, 0, 0, 0, 3, 0],\n            [0, 1, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0, 0, 3, 0, 0],\n            [0, 1, 0, 0, 3, 0, 0, 0, 0, 1, 0, 0, 3, 0, 0, 0],\n            [0, 0, 0, 3, 0, 2, 2, 0, 0, 0, 0, 3, 0, 2, 2, 0],\n            [0, 0, 3, 0, 0, 0, 0, 2, 0, 0, 3, 0, 0, 0, 0, 2],\n            [0, 3, 0, 0, 0, 0, 2, 0, 0, 3, 0, 0, 0, 0, 2, 0],\n            [3, 0, 0, 0, 0, 2, 2, 2, 3, 0, 0, 0, 0, 2, 2, 2],\n        ],\n        dtype=ubyte,\n    )\n\n    >>> nametable.Nametable((block,))\n    Nametable(Block(PatternTable((Pattern(PatternMeta(...)),)), (0, 0, 0, 0)),)\n\n.. code-end\n\n.. getting-help-begin\n\nGetting Help\n============\n\nPlease use the ``python-nametable`` tag on \n`StackOverflow <https://stackoverflow.com/questions/tagged/python-nametable>`_ to get help.\n\nAiding others and answers questions is a fantastic way to help!\n\n.. getting-help-end\n\n.. project-information-begin\n\nProject Information\n===================\n\n``nametable`` is released under the\n`GPL3 <https://tldrlegal.com/license/gnu-general-public-license-v3-(gpl-3)>`_ license.\nIts documentation is hosted on `Github IO <https://thejoesmo.github.io/nametable/>`_ and the\nrepository is hosted on `Github <https://github.com/TheJoeSmo/nametable>`_.  The latest release\nis hosted on `PyPI <https://pypi.org/project/nametable/>`_.  \n\n.. project-information-end',
    'author': 'TheJoeSmo',
    'author_email': 'joesmo.joesmo12@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9.7,<3.11',
}


setup(**setup_kwargs)
