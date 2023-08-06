``nametable`` serves to bridge the gap between 
[Nintendo Entertainment System's](https://en.wikipedia.org/wiki/Nintendo_Entertainment_System)
[Picture Processing Unit's](https://wiki.nesdev.org/w/index.php/PPU)
[nametables](https://wiki.nesdev.org/w/index.php?title=PPU_nametables) and Python.

Its main goal is to create an [Object Oriented](https://en.wikipedia.org/wiki/Object-oriented_programming)
approach to represent a nametable on the NES.

It provides the ability to create instances of Pattern and Block directly from memory and inserts them into PatternTable and Nametable, respectively.

```python
    >>> import nametable

    >>> pattern = nametable.PatternMeta(bytes.fromhex("41 C2 44 48 10 20 40 80 01 02 04 08 16 21 42 87"))
    >>> pattern.numpy_array
    array(
        [
            [0, 1, 0, 0, 0, 0, 0, 3],
            [1, 1, 0, 0, 0, 0, 3, 0],
            [0, 1, 0, 0, 0, 3, 0, 0],
            [0, 1, 0, 0, 3, 0, 0, 0],
            [0, 0, 0, 3, 0, 2, 2, 0],
            [0, 0, 3, 0, 0, 0, 0, 2],
            [0, 3, 0, 0, 0, 0, 2, 0],
            [3, 0, 0, 0, 0, 2, 2, 2],
        ],
        dtype=ubyte,
    )

    >>> pattern_table = nametable.PatternTable((nametable.Pattern(pattern),))
    >>> block = nametable.Block(pattern_table, (0, 0, 0, 0))
    >>> block.numpy_array
    array(
        [
            [0, 1, 0, 0, 0, 0, 0, 3, 0, 1, 0, 0, 0, 0, 0, 3],
            [1, 1, 0, 0, 0, 0, 3, 0, 1, 1, 0, 0, 0, 0, 3, 0],
            [0, 1, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0, 0, 3, 0, 0],
            [0, 1, 0, 0, 3, 0, 0, 0, 0, 1, 0, 0, 3, 0, 0, 0],
            [0, 0, 0, 3, 0, 2, 2, 0, 0, 0, 0, 3, 0, 2, 2, 0],
            [0, 0, 3, 0, 0, 0, 0, 2, 0, 0, 3, 0, 0, 0, 0, 2],
            [0, 3, 0, 0, 0, 0, 2, 0, 0, 3, 0, 0, 0, 0, 2, 0],
            [3, 0, 0, 0, 0, 2, 2, 2, 3, 0, 0, 0, 0, 2, 2, 2],
            [0, 1, 0, 0, 0, 0, 0, 3, 0, 1, 0, 0, 0, 0, 0, 3],
            [1, 1, 0, 0, 0, 0, 3, 0, 1, 1, 0, 0, 0, 0, 3, 0],
            [0, 1, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0, 0, 3, 0, 0],
            [0, 1, 0, 0, 3, 0, 0, 0, 0, 1, 0, 0, 3, 0, 0, 0],
            [0, 0, 0, 3, 0, 2, 2, 0, 0, 0, 0, 3, 0, 2, 2, 0],
            [0, 0, 3, 0, 0, 0, 0, 2, 0, 0, 3, 0, 0, 0, 0, 2],
            [0, 3, 0, 0, 0, 0, 2, 0, 0, 3, 0, 0, 0, 0, 2, 0],
            [3, 0, 0, 0, 0, 2, 2, 2, 3, 0, 0, 0, 0, 2, 2, 2],
        ],
        dtype=ubyte,
    )

    >>> nametable.Nametable((block,))
    Nametable(Block(PatternTable((Pattern(PatternMeta(...)),)), (0, 0, 0, 0)),)
```

Getting Help
============

Please use the ``python-nametable`` tag on 
[StackOverflow](https://stackoverflow.com/questions/tagged/python-nametable) to get help.

Aiding others and answers questions is a fantastic way to help!

Project Information
===================

``nametable`` is released under the
[GPL3](https://tldrlegal.com/license/gnu-general-public-license-v3-(gpl-3)) license.
Its documentation is hosted on [Github](https://thejoesmo.github.io/nametable/) and the
repository is hosted on [Github](https://github.com/TheJoeSmo/nametable).  The latest release
is hosted on [PyPI](https://pypi.org/project/nametable/).  
