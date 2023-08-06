from typing import Protocol
from weakref import WeakKeyDictionary

from numpy import ubyte
from numpy.typing import NDArray

from nametable.PatternMeta import PatternMeta


class PatternProtocol(Protocol):
    """
    An `Object Oriented <https://en.wikipedia.org/wiki/Object-oriented_programming>`_
    wrapper around :class:`~nametable.PatternMeta.PatternMeta`.
    This class enables easier extensions and edits on
    :class:`~nametable.PatternMeta.PatternMeta` without needing to understand the
    internals of the NES.

    See Also
    --------
    :class:`~nametable.PatternMeta.PatternMeta`
    :class:`~nametable.Pattern.Pattern`
    :class:`~nametable.PatternAnimated.PatternAnimatedProtocol`
    :class:`~nametable.PatternAnimated.PatternAnimated`
    """

    @property
    def meta(self) -> PatternMeta:
        """
        Provides the wrapped meta class that the instance is representing.

        Returns
        -------
        PatternMeta
            The current :class:`~nametable.PatternMeta.PatternMeta` that this instance
            is representing.
        """

    @property
    def numpy_array(self) -> NDArray[ubyte]:
        """
        Provides a Numpy array that represents the pattern as a 2D matrix of the pixels of
        the pattern.

        Returns
        -------
        NDArray[ubyte]
            The array is equivalent to the meta that the instance is representing.

        Notes
        -----
        The purpose of extending the responsibility of creating an array to this instance
        is to provide additional ability to cache and utilize other techniques to
        improve performance.

        See Also
        --------
        :class:`~nametable.PatternMeta.PatternMeta`
        """


class Pattern:
    """
    A generic implementation of :class:`~nametable.Pattern.PatternProtocol`.

    See Also
    --------
    :class:`~nametable.Pattern.PatternProtocol`
    :class:`~nametable.PatternMeta.PatternMeta`
    :class:`~nametable.PatternAnimated.PatternAnimated`
    """

    _patterns = WeakKeyDictionary()

    def __new__(cls, meta: PatternMeta):
        """
        As Patterns will often be copied and are immutable, this method ensures that only
        a single copy will be stored inside memory.

        Parameters
        ----------
        meta : PatternMeta
            The meta instance to be hashed.

        Examples
        --------
        To create an instance, simply provide an instance of PatternMeta and be instantiated.

        >>> Pattern(PatternMeta(bytes.fromhex("41 C2 44 48 10 20 40 80 01 02 04 08 16 21 42 87")))
        Pattern(PatternMeta(bytes.fromhex("41 C2 44 48 10 20 40 80 01 02 04 08 16 21 42 87")))

        """
        if meta not in cls._patterns:
            instance = super().__new__(cls)
            cls._patterns[meta] = instance
        return cls._patterns[meta]

    def __init__(self, meta: PatternMeta):
        """
        Generates an instance from a instance of :class:`~nametable.PatternMeta.PatternMeta`.
        This instance will proxy its methods to enable better performance.

        Parameters
        ----------
        meta : PatternMeta
            The meta instance that represents the contents of this instance.
        """
        self._meta = meta
        self._numpy_array = None

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._meta})"

    @classmethod
    def from_numpy_array(cls, array: NDArray[ubyte]):
        """
        Wraps :meth:`~nametable.PatternMeta.PatternMeta.from_numpy_array` to create an
        instance directly.

        Parameters
        ----------
        array : NDArray[ubyte]
            The numpy array to be converted.

        See Also
        --------
        :class:`~nametable.Pattern.PatternProtocol`
        """
        return cls(PatternMeta.from_numpy_array(array))

    @property
    def numpy_array(self) -> NDArray[ubyte]:
        """
        Provides a Numpy array that represents the pattern as a 2D matrix of the pixels of
        the pattern.

        Returns
        -------
        NDArray[ubyte]
            The array is equivalent to the meta that the instance is representing.

        Notes
        -----
        The instance ensures that array provided is identical to the wrapped meta it represents.

        This method is more efficient than the meta instance, with the results being cached,
        dramatically reducing math operations for large-scale operations.

        The array provided should never be modified.  If it is modified, this will interfere
        with the caching of the Pattern and may cause undesired artifacts.

        Examples
        --------
        When creating the instance, the class will check if the an equivalent instance of meta
        was already utilized to create this class.  If one exists, it will return the instance
        of the already instantiated Pattern, otherwise it will create a new instance and cache
        it into a weak reference dictionary for future instantiations.

        >>> meta = PatternMeta(bytes.fromhex("41 C2 44 48 10 20 40 80 01 02 04 08 16 21 42 87"))
        >>> pattern1 = Pattern(meta)
        >>> pattern2 = Pattern(meta)
        >>> pattern1 is pattern2
        True

        Likewise, when creating an array, the Pattern will cache the result after its first
        creation.  The following code will only result in one execution of a numpy array.

        >>> pattern1.numpy_array
        ...
        >>> pattern2.numpy_array
        ...
        """
        if self._numpy_array is None:
            self._numpy_array = self.meta.numpy_array
        return self._numpy_array

    @property
    def meta(self) -> PatternMeta:
        """
        Provides the wrapped meta class that the instance is representing.

        Returns
        -------
        PatternMeta
            The current :class:`~nametable.PatternMeta.PatternMeta` that this instance
            is representing.
        """
        return self._meta
