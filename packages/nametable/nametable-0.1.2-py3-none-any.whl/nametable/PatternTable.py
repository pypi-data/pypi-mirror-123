from typing import Protocol
from dataclasses import dataclass

from nametable.Pattern import Pattern


class PatternTableProtocol(Protocol):
    """
    A wrapper around a :py:class:`python:tuple` of :class:`~nametable.Pattern.Pattern` that
    represent the field of possible Patterns available on a given item.  This enabled a byte to
    index the range of patterns on the PPU to form :class:`~nametable.Block.BlockProtocol` on
    the `Picture Processing Unit <https://wiki.nesdev.org/w/index.php/PPU>`_:.

    Attributes
    ----------
    pattern_array: tuple[Pattern, ...]
        A group of Patterns used for quickly indexing :class:`~nametable.Block.BlockProtocol`.

    See Also
    --------
    :class:`~nametable.Pattern.Pattern`
    :class:`~nametable.PatternTable.PatternTable`
    :class:`~nametable.Block.BlockProtocol`
    :class:`~nametable.Nametable.Nametable`
    """

    pattern_array: tuple[Pattern, ...]


@dataclass(frozen=True, eq=True)
class PatternTable:
    """
    A generic implementation of :class:`~nametable.PatternTable.PatternTableProtocol` that
    utilizes a simple :py:func:`~python:dataclasses.dataclass`.

    Attributes
    ----------
    pattern_array: tuple[Pattern, ...]
        A group of Patterns used for quickly indexing :class:`~nametable.Block.BlockProtocol`.

    See Also
    --------
    :class:`~nametable.PatternTable.PatternTableProtocol`
    :class:`~nametable.Pattern.Pattern`
    """

    pattern_array: tuple[Pattern, ...]
