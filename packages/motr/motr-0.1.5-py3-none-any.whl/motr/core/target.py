"""Module for defining runtime targets."""

import os
import typing

import attr

CoerceToString = typing.Union[os.PathLike[str], str]


@attr.dataclass(frozen=True)
class Token:
    """Base class for non-stringlike targets."""


@attr.dataclass(frozen=True)
class Deleted(Token):
    """Target indicating that a path was deleted."""

    path: str


Target = typing.Union[Token, str]
CoerceToTarget = typing.Union[Token, CoerceToString]


def deleted(path: CoerceToString) -> Target:
    """Return a Deleted target."""
    return Deleted(os.fspath(path))


def coerce(target: CoerceToTarget) -> Target:
    """Return the input, coerced to a Target-type value."""
    if isinstance(target, Token):
        return target
    return os.fspath(target)
