from typing import Protocol
from dataclasses import dataclass

from nametable.Animator import AnimatedProtocol, AnimatorProtocol
from nametable.PatternTable import PatternTableProtocol
from nametable.Pattern import Pattern


class PatternTableAnimatedProtocol(PatternTableProtocol, AnimatedProtocol, Protocol):
    """
    A :class:`~nametable.PatternTable.PatternTableProtocol` that determines the
    :attr:`~nametable.PatternTable.PatternTableProtocol.pattern_array` from
    :class:`~nametable.Animator.AnimatorProtocol` denoted by
    :class:`~nametable.Animator.AnimatedProtocol`.

    Attributes
    ----------
    pattern_array: tuple[Pattern, ...]
        A group of Patterns used for quickly indexing :class:`~nametable.Block.BlockProtocol`.
    animator: AnimatorProtocol
        The instance of the animator controlling the frame shown.

    See Also
    --------
    :class:`~nametable.PatternTable.PatternTable`
    """


@dataclass
class PatternTableAnimated:
    """
    A generic implementation of
    :class:`~nametable.PatternTableAnimated.PatternTableAnimatedProtocol` that determines
    the :attr:`pattern_tables` from the :attr:`~nametable.Animator.Animator.frame` specified
    inside :class:`~nametable.Animator.AnimatorProtocol`.

    Attributes
    ----------
    pattern_array: tuple[Pattern, ...]
        A group of Patterns used for quickly indexing :class:`~nametable.Block.BlockProtocol`.
    animator: AnimatorProtocol
        The instance of the animator controlling the frame shown.

    See Also
    --------
    :class:`~nametable.PatternTableAnimated.PatternTableAnimatedProtocol`
    :class:`~nametable.PatternTable.PatternTable`
    """

    pattern_tables: tuple[PatternTableProtocol]
    animator: AnimatorProtocol

    @property
    def pattern_array(self) -> tuple[Pattern, ...]:
        return self.pattern_tables[self.animator.frame].pattern_array
