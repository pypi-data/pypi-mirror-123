from typing import Protocol
from dataclasses import dataclass

from numpy import ubyte, concatenate
from numpy.typing import NDArray

from nametable.PatternTable import PatternTableProtocol


class BlockInvalidSizeException(ValueError):
    """
    Raised when the length of :attr:`~nametable.Block.BlockProtocol.patterns` is an
    invalid size for a :class:`~nametable.Block.BlockProtocol`.
    """


class PatternTableIndexException(IndexError):
    """
    Raised when the :py:class:`python:int` inside
    :attr:`~nametable.Block.BlockProtocol.patterns` is an invalid index into
    :attr:`~nametable.PatternTable.PatternTableProtocol.pattern_array` of
    :attr:`~nametable.Block.BlockProtocol.pattern_table`.
    """


class BlockProtocol(Protocol):
    """
    A representation of a combination of four instances of
    :class:`~nametable.Pattern.PatternProtocol`.  Despite sounding unintuitive, this format was
    widely adopted throughout NES development due to limitations of the
    `Picture Processing Unit <https://wiki.nesdev.org/w/index.php/PPU>`_: 'PPU' and memory
    space on the NES: The
    `PPU attribute tables <https://wiki.nesdev.org/w/index.php?title=PPU_attribute_tables>`_
    could only change the color attribute every 16 pixel in both dimensions, known as a 'Block'.
    Similarly, to store each Pattern of each Block as a list in memory would take up the
    kilobytes of memory.  By storing common sections of 2x2 Patterns, most programmers during
    this era found that memory required was dramatically reduced.

    Attributes
    ----------
    pattern_table: PatternTableProtocol
        The instance of :class:`~nametable.PatternTable.PatternTableProtocol` to serve as the
        lookup table of instances of :class:`~nametable.Pattern.PatternProtocol`.
    patterns: tuple[int, int, int, int]
        The indexes into :attr:`pattern_table` to create instances of
        :class:`~nametable.Pattern.PatternProtocol` from.

    See Also
    --------
    :class:`~nametable.PatternTable.PatternTableProtocol`
    :class:`~nametable.Block.Block`
    :class:`~nametable.Nametable.NametableProtocol`
    """

    pattern_table: PatternTableProtocol
    patterns: tuple[int, int, int, int]

    @property
    def numpy_array(self) -> NDArray[ubyte]:
        """
        Generates a two dimensional array with two bits per pixel, representing the respective
        instances of :class:`~nametable.Pattern.PatternProtocol`
        :attr:`~nametable.Pattern.PatternProtocol.numpy_array` concatenate together to form
        a 16 by 16 pixel grid.  The order of they are shown is top left, top right, bottom left,
        bottom right, respectively.

        Returns
        -------
        NDArray[ubyte]
            This instance represented as an array.

        See Also
        --------
        :class:`~nametable.Pattern.PatternProtocol`
        :class:`~nametable.PatternMeta.PatternMeta`
        """


@dataclass(frozen=True, eq=True)
class Block:
    """
    A generic implementation of :class:`~nametable.Block.BlockProtocol` that utilizes
    a simple :py:func:`~python:dataclasses.dataclass`.

    Attributes
    ----------
    pattern_table: PatternTableProtocol
        The instance of :class:`~nametable.PatternTable.PatternTableProtocol` to serve as the
        lookup table of instances of :class:`~nametable.Pattern.PatternProtocol`.
    patterns: tuple[int, int, int, int]
        The indexes into :attr:`pattern_table` to create instances of
        :class:`~nametable.Pattern.PatternProtocol` from.

    Raises
    ------
    BlockInvalidSizeException
        Raised if the length of :attr:`patterns` is not equal to four.
    PatternTableIndexException
        Raise if any index inside :attr:`patterns` would result in an
        :py:class:`python:IndexError`.

    Examples
    --------
    To create an instance of a Block.

    >>> Block(
    ...     PatternTable(
    ...         (
    ...             Pattern(PatternMeta
    ...                 (
    ...                     bytes.fromhex("41 C2 44 48 10 20 40 80 01 02 04 08 16 21 42 87"))
    ...                 ),
    ...         )
    ...     ),
    ...     (0, 0, 0, 0,)
    ... )
    Block(PatternTable((Pattern(PatternMeta(...)),)), (0, 0, 0, 0,))

    """

    pattern_table: PatternTableProtocol
    patterns: tuple[int, int, int, int]

    def __post_init__(self):
        if len(self.patterns) != 4:
            raise BlockInvalidSizeException(f"Block must only have four patterns, {len(self.patterns)} given")
        if any(pattern > len(self.pattern_table.pattern_array) for pattern in self.patterns):
            raise PatternTableIndexException(
                f"Invalid index to Pattern Table of size {len(self.pattern_table.pattern_array)}"
            )
        if any(pattern < 0 for pattern in self.patterns):
            raise PatternTableIndexException("Pattern indexes to Pattern Table must be positive")

    @property
    def numpy_array(self) -> NDArray[ubyte]:
        """
        Generates a two dimensional array with two bits per pixel, representing the respective
        instances of :class:`~nametable.Pattern.PatternProtocol`
        :attr:`~nametable.Pattern.PatternProtocol.numpy_array` concatenate together to form
        a 16 by 16 pixel grid.  The order of they are shown is top left, top right, bottom left,
        bottom right, respectively.

        Returns
        -------
        NDArray[ubyte]
            This instance represented as an array.

        See Also
        --------
        :class:`~nametable.Pattern.PatternProtocol`
        :class:`~nametable.PatternMeta.PatternMeta`

        Examples
        --------
        To create an instance of a Block.

        >>> block = Block(
        ...     PatternTable(
        ...         (
        ...             Pattern(PatternMeta
        ...                 (
        ...                     bytes.fromhex("41 C2 44 48 10 20 40 80 01 02 04 08 16 21 42 87"))
        ...                 ),
        ...         )
        ...     ),
        ...     (0, 0, 0, 0,)
        ... )
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
        """
        return concatenate(
            (
                concatenate(
                    (
                        self.pattern_table.pattern_array[self.patterns[0]].numpy_array,
                        self.pattern_table.pattern_array[self.patterns[1]].numpy_array,
                    )
                ),
                concatenate(
                    (
                        self.pattern_table.pattern_array[self.patterns[2]].numpy_array,
                        self.pattern_table.pattern_array[self.patterns[3]].numpy_array,
                    )
                ),
            ),
            axis=1,
        )
