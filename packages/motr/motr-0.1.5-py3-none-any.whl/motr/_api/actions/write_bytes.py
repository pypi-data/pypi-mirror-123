"""Module for writing predetermined data as a runtime action."""

from __future__ import annotations

import pathlib
import typing

import attr
import trio

import motr._api.requirements.action
import motr._api.requirements.target
import motr.core.result

if typing.TYPE_CHECKING:
    import motr._api.actions.io
    import motr._api.requirements.requirements


@attr.dataclass(frozen=True)
class WriteBytes:
    """Runtime action to write the specified data to the specified path."""

    path: pathlib.Path
    data: bytes  # Put the responsibility for encoding on the caller.

    async def __call__(
        self,
    ) -> typing.Tuple[motr.core.result.Result, typing.Mapping[str, str]]:
        """Write the bytes to the path, and report success or failure."""
        try:
            await trio.Path(self.path).write_bytes(self.data)
        except Exception:
            # Sure would be nice to put traceback information somewhere.
            return motr.core.result.Result.ABORTED, {}
        return motr.core.result.Result.PASSED, {}


def write_bytes(
    path: motr._api.actions.io.Input[pathlib.Path], data: bytes
) -> motr._api.requirements.requirements.Requirements:
    """Yield a requirement for a WriteBytes action, and its result."""
    action = WriteBytes(path.path, data)
    yield from motr._api.requirements.action.action(action)
    yield from motr._api.requirements.target.target(path.path, action)
