from typing import Protocol
from dataclasses import dataclass

from numpy import ubyte
from numpy.typing import NDArray

from nametable.PatternMeta import PatternMeta
from nametable.Animator import AnimatedProtocol, AnimatorProtocol
from nametable.Pattern import PatternProtocol


class PatternAnimatedProtocol(PatternProtocol, AnimatedProtocol, Protocol):
    """
    A :class:`~nametable.Pattern.PatternProtocol` that determines the
    :class:`~nametable.PatternMeta.PatternMeta` that is represented by the frame inside
    :class:`~nametable.Animator.AnimatorProtocol`.

    Attributes
    ----------
    animator: AnimatorProtocol
        The instance of the animator controlling the frame shown.

    See Also
    --------
    :class:`~nametable.Animator.AnimatorProtocol`
    :class:`~nametable.Animator.Animator`
    :class:`~nametable.PatternAnimated.PatternAnimated`
    """


@dataclass
class PatternAnimated:
    """
    A generic implementation of :class:`~nametable.PatternAnimated.PatternAnimatedProtocol`
    that utilizes an instance of :class:`~nametable.Animator.AnimatorProtocol` to dictate
    the :class:`~nametable.PatternMeta.PatternMeta` meta for the instance from a
    :py:class:`python:tuple` of :class:`~nametable.Pattern.PatternProtocol`.

    Attributes
    ----------
    stack: tuple[PatternProtocol]
        A tuple of patterns that the instance's animator selects from for a given frame.
    animator: AnimatorProtocol
        The instance of the animator controlling the frame shown.

    Notes
    -----
    The user must ensure that the :attr:`animator` must never have a frame greater than
    the length of :attr:`stack`.
    """

    stack: tuple[PatternProtocol]
    animator: AnimatorProtocol

    @property
    def numpy_array(self) -> NDArray[ubyte]:
        """
        Provides an array that represents the pattern as a 2D matrix of the pixels of
        the pattern of the current :class:`nametable.Pattern.PatternProtocol` inside
        :attr:`stack`.

        Returns
        -------
        NDArray[ubyte]
            The array of the current :class:`nametable.Pattern.PatternProtocol` dictated by
            :attr:`animator`.

        See Also
        --------
        :class:`~nametable.Pattern.PatternProtocol`
        :class:`~nametable.Pattern.Pattern`

        Examples
        --------
        The animator can dynamically change the array provided

        >>> data = bytes.fromhex("41 C2 44 48 10 20 40 80 01 02 04 08 16 21 42 87")
        >>> pattern = PatternAnimated(
        ...     (Pattern(PatternMeta(data)), Pattern(PatternMeta(data[::-1]))),
        ...     Animator(0)
        ... )
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
        >>> pattern.animator.frame = 1
        >>> pattern.numpy_array
        array(
            [
                [0, 0, 0, 3, 0, 1, 0, 0],
                [0, 0, 3, 0, 1, 1, 0, 0],
                [0, 3, 0, 0, 0, 1, 0, 0],
                [3, 0, 0, 0, 0, 1, 0, 0],
                [0, 2, 2, 0, 0, 0, 0, 3],
                [0, 0, 0, 2, 0, 0, 1, 2],
                [0, 0, 2, 0, 0, 1, 2, 0],
                [0, 2, 2, 2, 2, 1, 1, 0],
            ],
            dtype=ubyte,
        )

        """
        return self.stack[self.animator.frame].numpy_array

    @property
    def meta(self) -> PatternMeta:
        """
        Provides the meta the wrapped meta class that the pattern of the current
        :class:`nametable.Pattern.PatternProtocol` inside :attr:`stack` is representing.

        Returns
        -------
        PatternMeta
            The current :class:`~nametable.PatternMeta.PatternMeta` that this instance
            is representing, dictated by :attr:`animator`.

        See Also
        --------
        :class:`~nametable.Pattern.PatternProtocol`
        :class:`~nametable.Pattern.Pattern`
        :class:`~nametable.PatternMeta.PatternMeta`

        Examples
        --------
        The animator can dynamically change the meta provided

        >>> data = bytes.fromhex("41 C2 44 48 10 20 40 80 01 02 04 08 16 21 42 87")
        >>> pattern = PatternAnimated(
        ...     (Pattern(PatternMeta(data)), Pattern(PatternMeta(data[::-1]))),
        ...     Animator(0)
        ... )
        >>> pattern.meta
        PatternMeta(data)
        >>> pattern.animator.frame = 1
        >>> pattern.meta
        PatternMeta(data[::-1])

        """
        return self.stack[self.animator.frame].meta
