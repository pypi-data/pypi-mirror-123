from dataclasses import dataclass

from numpy import ubyte, add, frombuffer, unpackbits
from numpy.typing import NDArray


@dataclass(frozen=True, eq=True)
class PatternMeta:
    """
    A wrapper around a fixed series of 16 bytes that represents an eight by eight square
    for a two bit image, typically associated with the Nintendo Entertainment System.

    This format is derived from the
    `Picture Processing Unit <https://wiki.nesdev.org/w/index.php/PPU>`_: 'PPU'.
    The PPU functioned as a primitive graphics card for the NES, allowing a hard-wired
    implementation for graphics to be streamlined from the CPU onto the consumer's television.
    This development enabled a great advance in the sophistication of graphics and hardware.
    Prior consoles, such as the Atari 2600 had to
    `race the beam <https://www.youtube.com/watch?v=sJFnWZH5FXc>`_ to render graphics onto the
    screen.  With the fixed format of the PPU, much of the overhead that previously
    burdened the developer was reduced into a space in RAM devoted to a few flags and
    memory used for sprites and background graphics.  The core element of this was the `Tile`,
    which is synonymous with Pattern.  This class utilizes this format and fluffs the one
    dimensional byte array into a two dimensional array of bytes, which can easily be
    transposed into other picture formats for editing and viewing.  Likewise, it can flatten
    these two dimensional arrays back down into the format utilized by the PPU.

    See Also
    --------
    :class:`~nametable.Pattern.Pattern`

    Notes
    -----
    For large creation of patterns, it is recommended that :class:`~nametable.Pattern.Pattern`
    should be used instead.  Pattern will store multiple copies of the same pattern as
    one type, and enable more sophisticated use throughout the program.
    Specifically, it is easier to extend, due to not being immutable.

    Examples
    --------
    To create a pattern, provide a series of 16 bytes.

    >>> pattern = PatternMeta(bytes.fromhex("41 C2 44 48 10 20 40 80 01 02 04 08 16 21 42 87"))
    >>> pattern
    PatternMeta(b'...')
    """

    data: bytes

    WIDTH = 8
    HEIGHT = 8

    def __eq__(self, other) -> bool:
        return list(self.data) == list(other.data)

    def __ne__(self, other) -> bool:
        return list(self.data) != list(other.data)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.data.hex()})"

    @classmethod
    def from_numpy_array(cls, array: NDArray[ubyte]):
        """
        Flattens a two dimensional array into a fixed series of 16 bytes that represent
        a two bits per pixel pattern that was commonly used for the NES.  Each byte inside
        the two dimensional array is expected to contain only two bits.  If other bits are
        set, they will be strictly ignored, as the NES format does not enable such
        modifications.

        Parameters
        ----------
        array : NDArray[ubyte]
            The numpy array to be converted.

        Examples
        --------
        Any two dimension array of type ubyte, with the representation of two bits
        and a size of (8, 8) can be transferred back to a pattern.

        >>> pattern1 = PatternMeta(bytes.fromhex("41 C2 44 48 10 20 40 80 01 02 04 08 16 21 42 87"))
        >>> pattern2 = PatterMeta.from_numpy_array(pattern1.numpy_array)
        >>> pattern1 == pattern2
        True

        If more than two bits are represented inside an array, those bits will be truncated.

        >>> modified_array = pattern1.numpy_array
        >>> modified_array[0][0] = 0b1111
        >>> pattern3 = PatternMeta.from_numpy_array(modified_array)
        >>> pattern1 == pattern3
        False

        >>> modified_array[0][0] = 0b1100
        >>> pattern4 = PatternMeta.from_numpy_array(modified_array)
        >>> pattern1 == pattern4
        True

        """
        assert array.shape == (8, 8)

        a = array.flatten()
        bitmap = [element & 0b1 for element in a] + [(element & 0b10) >> 1 for element in a]
        ba = bytearray(16)
        for index, element in enumerate(bitmap):
            big_endian_offset = 8 * (index // 64)
            byte_offset = (index // 8) % 8
            bit_offset = abs(8 - (index % 8)) - 1
            ba[big_endian_offset + byte_offset] += element << bit_offset

        assert len(ba) == 16

        return cls(bytes(ba))

    @property
    def numpy_array(self) -> NDArray[ubyte]:
        """
        Fluffs the byte array into a two dimensional array with two bits per pixel,
        as specified in the
        `pattern format <https://wiki.nesdev.org/w/index.php?title=PPU_pattern_tables>`_.

        Returns
        -------
        NDArray[ubyte]
            The PatternMeta represented as an array.

        Notes
        -----
        The format of a pattern is represented by two fixed series of eight bytes.
        The series represent the first and second bit of the palette index of the
        pattern, respectively.  If the neither bit is set, the pixel is transparent.

        In the diagram below, '.' represents a transparent pixel.  Numbers 1, 2, 3
        represent the palette index for a given pattern.::

            Bit Planes                  Pixel Pattern
            [0x0] = 0x41 = 0b01000001
            [0x1] = 0xC2 = 0b11000010
            [0x2] = 0x44 = 0b01000100
            [0x3] = 0x48 = 0b01001000
            [0x4] = 0x10 = 0b00010000
            [0x5] = 0x20 = 0b00100000         .1.....3
            [0x6] = 0x40 = 0b01000000         11....3.
            [0x7] = 0x80 = 0b10000000  =====  .1...3..
                                              .1..3...
            [0x8] = 0x01 = 0b00000001  =====  ...3.22.
            [0x9] = 0x02 = 0b00000010         ..3....2
            [0xA] = 0x04 = 0b00000100         .3....2.
            [0xB] = 0x08 = 0b00001000         3....222
            [0xC] = 0x16 = 0b00010110
            [0xD] = 0x21 = 0b00100001
            [0xE] = 0x42 = 0b01000010
            [0xF] = 0x87 = 0b10000111

        Examples
        --------
        Any pattern can be transferred to a 2 dimensional array.

        >>> pattern = PatternMeta(bytes.fromhex("41 C2 44 48 10 20 40 80 01 02 04 08 16 21 42 87"))
        >>> pattern_array = pattern.numpy_array
        >>> pattern_array
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
        """
        assert len(self.data) == 16

        array = unpackbits(frombuffer(self.data, dtype=ubyte)).reshape((2, self.HEIGHT, self.WIDTH))
        array = add(array[0, :, :], array[1, :, :] * 2)

        assert array.shape == (8, 8)

        return array
