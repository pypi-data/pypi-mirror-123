from typing import Protocol
from dataclasses import dataclass


class AnimatorProtocol(Protocol):
    """
    A class that handles the changing one an integer, representing the frame
    that the :class:`~nametable.Animator.AnimatedProtocol` is on.

    Attributes
    ----------
    frame: The current frame that the :class:`~nametable.Animator.AnimatedProtocol` is on.

    See Also
    --------
    :class:`~nametable.Animator.AnimatedProtocol`
    :class:`~nametable.Animator.Animator`
    """

    frame: int


class AnimatedProtocol(Protocol):
    """
    A class that ensures that the animator dictates which frame is being shown for
    an animated object.

    Attributes
    ----------
    animator: The instance of the animator controlling the frame shown.

    See Also
    --------
    :class:`~nametable.Animator.AnimatorProtocol`
    :class:`~nametable.Animator.Animator`
    """

    animator: AnimatorProtocol


@dataclass
class Animator:
    """
    A generic implementation of :class:`~nametable.Animator.AnimatorProtocol` that utilizes
    a simple :py:func:`~python:dataclasses.dataclass`.

    Attributes
    ----------
    frame: int
        The current frame that the :class:`~nametable.Animator.AnimatedProtocol` is on.

    See Also
    --------
    :class:`~nametable.Animator.AnimatorProtocol`
    :class:`~nametable.Animator.AnimatedProtocol`
    """

    frame: int
