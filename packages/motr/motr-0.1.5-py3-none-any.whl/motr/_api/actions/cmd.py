"""Module for the action of running a single command."""

from __future__ import annotations

import os
import types
import typing

import attr
import pyrsistent
import trio

import motr._api.actions.io
import motr._api.requirements.action
import motr._api.requirements.target
import motr.core.result

if typing.TYPE_CHECKING:
    import motr._api.requirements.requirements
    import motr.core.target

PathStr = typing.Union[str, os.PathLike[str]]
CmdArg = typing.Union[motr._api.actions.io.IOType[PathStr], PathStr]


@attr.dataclass(frozen=True)
class Cmd:
    """Runtime action representing a command-line call."""

    cmd: typing.Tuple[str, ...]
    env: pyrsistent.PMap[str, str] = pyrsistent.pmap()
    allowed_codes: pyrsistent.PSet[int] = pyrsistent.pset()

    async def __call__(
        self,
    ) -> typing.Tuple[motr.core.result.Result, typing.Mapping[str, str]]:
        """Run the command and return the outcome data."""
        cmd_result = await trio.run_process(
            self.cmd,
            capture_stdout=True,
            capture_stderr=True,
            check=False,
            env=dict(self.env),
        )
        returncode = cmd_result.returncode
        failed = bool(returncode)
        return motr.core.result.Result(
            (failed, failed and returncode not in self.allowed_codes)
        ), {
            "out": cmd_result.stdout.decode(),
            "err": cmd_result.stderr.decode(),
        }


def cmd_(
    cmd: typing.Sequence[CmdArg],
    *io: motr._api.actions.io.IOType[motr.core.target.CoerceToTarget],
    allowed_codes: typing.Collection[int] = frozenset(),
    env: typing.Mapping[str, CmdArg] = types.MappingProxyType({})
) -> motr._api.requirements.requirements.Requirements:
    """Yield a requirement of a Cmd action, and supporting requirements."""
    cmd_unwrapper: motr._api.actions.io.Unwrapper[
        PathStr
    ] = motr._api.actions.io.Unwrapper(cmd)
    env_unwrapper: motr._api.actions.io.Unwrapper[
        PathStr
    ] = motr._api.actions.io.Unwrapper(env.values())
    io_unwrapper: motr._api.actions.io.Unwrapper[
        motr.core.target.CoerceToTarget
    ] = motr._api.actions.io.Unwrapper(io)
    action = Cmd(
        tuple(os.fspath(path) for path in cmd_unwrapper.unwrapped()),
        allowed_codes=pyrsistent.pset(allowed_codes),
        env=pyrsistent.pmap(
            {
                key: os.fspath(val)
                for key, val in zip(env, env_unwrapper.unwrapped())
            }
        ),
    )
    yield from motr._api.requirements.action.action(
        action,
        *io_unwrapper.inputs(),
        *cmd_unwrapper.inputs(),
        *env_unwrapper.inputs(),
    )
    yield from _extra_targets(action, io_unwrapper)
    yield from _extra_targets(action, cmd_unwrapper)
    yield from _extra_targets(action, env_unwrapper)


def _extra_targets(
    action: motr.core.runner.RuntimeAction,
    unwrapper: typing.Union[
        motr._api.actions.io.Unwrapper[PathStr],
        motr._api.actions.io.Unwrapper[motr.core.target.CoerceToTarget],
    ],
) -> motr._api.requirements.requirements.Requirements:
    for target, names in unwrapper.outputs():
        yield from motr._api.requirements.target.target(target, action, *names)
