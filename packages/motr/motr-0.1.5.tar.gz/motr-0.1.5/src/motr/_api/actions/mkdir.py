"""Module for creating directories as a runtime action."""

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
class Mkdir:
    """Runtime action to create a directory."""

    path: pathlib.Path

    async def __call__(
        self,
    ) -> typing.Tuple[motr.core.result.Result, typing.Mapping[str, str]]:
        """Create the directory and report success or failure."""
        try:
            await trio.Path(self.path).mkdir(parents=True, exist_ok=True)
        except Exception:
            return motr.core.result.Result.ABORTED, {}
        return motr.core.result.Result.PASSED, {}


def mkdir(
    path: motr._api.actions.io.Input[pathlib.Path],
) -> motr._api.requirements.requirements.Requirements:
    """Yield a requirement for a Mkdir, and its outputs."""
    action = Mkdir(path.path)
    yield from motr._api.requirements.action.action(action)
    yield from motr._api.requirements.target.target(path.path, action)
