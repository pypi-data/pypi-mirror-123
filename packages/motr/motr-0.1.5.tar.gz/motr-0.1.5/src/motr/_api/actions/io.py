from __future__ import annotations

import typing

import attr
import pyrsistent

T = typing.TypeVar("T")


@attr.dataclass(frozen=True)
class Output(typing.Generic[T]):
    """Wrapper class that represents a task result."""

    path: T
    names: pyrsistent.PVector[str] = pyrsistent.pvector()


@attr.dataclass(frozen=True)
class Input(typing.Generic[T]):
    """Wrapper class that represents a task requirement."""

    path: T

    def as_output(self, *args: str) -> Output[T]:
        """Return the wrapped value as a task result with the given names."""
        return Output(self.path, pyrsistent.pvector(args))


IOType = typing.Union[Input[T], Output[T]]

IO = Input, Output


@attr.dataclass(frozen=True)
class Unwrapper(typing.Generic[T]):
    """IO-unwrapping converter over an iterable of possibly-wrapped values."""

    iterable: typing.Iterable[typing.Union[T, IOType[T]]]

    def inputs(self) -> typing.Iterator[T]:
        """Return the underlying values of all Input items."""
        return (item.path for item in self.iterable if isinstance(item, Input))

    def outputs(
        self,
    ) -> typing.Iterator[typing.Tuple[T, typing.Sequence[str]]]:
        """Return the underlying value and the names of all Output items."""
        return (
            (item.path, item.names)
            for item in self.iterable
            if isinstance(item, Output)
        )

    def unwrapped(self) -> typing.Iterator[T]:
        """Return the underlying value of all items, in order."""
        return (
            item.path if isinstance(item, IO) else item
            for item in self.iterable
        )
