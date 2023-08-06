"""Helpers for wrapping TargetNames around user-provided data."""

import typing

TargetName = typing.NewType("TargetName", str)


def coerce(name: str) -> TargetName:
    """Return the TargetName from the given name.

    This could do all sorts of modifications.
    """
    return TargetName(name)
