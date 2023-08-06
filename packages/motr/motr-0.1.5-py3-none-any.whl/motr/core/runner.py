"""The runtime logic module."""

from __future__ import annotations

import collections
import typing

import attr
import trio

import motr.core.exc
import motr.core.result

if typing.TYPE_CHECKING:
    import motr.core.registry
    import motr.core.target

RuntimeAction = typing.Callable[
    [],
    typing.Awaitable[
        typing.Tuple[motr.core.result.Result, typing.Mapping[str, str]]
    ],
]


@attr.dataclass(frozen=True)
class TaskWrapper:
    """Wrapper class that calls an action at most once."""

    started: trio.Event = attr.Factory(trio.Event)
    finished: trio.Event = attr.Factory(trio.Event)

    async def __call__(
        self,
        task: typing.Callable[[], typing.Awaitable[None]],
    ) -> None:
        """Perform the given task no more than once."""
        if self.started.is_set():
            await self.finished.wait()
            return
        self.started.set()
        try:
            await task()
        finally:
            self.finished.set()


@attr.dataclass(frozen=True)
class Target:
    """Container that matches requests for a target to the relevant action."""

    registry: motr.core.registry.Registry
    reporter: typing.Callable[[RuntimeAction], typing.ContextManager[None]]
    results: typing.Dict[
        motr.core.result.Result,
        typing.List[typing.Tuple[RuntimeAction, typing.Mapping[str, str]]],
    ]
    tasks: typing.DefaultDict[RuntimeAction, TaskWrapper] = attr.Factory(
        lambda: collections.defaultdict(TaskWrapper)
    )

    async def __call__(self, target: motr.core.target.Target) -> None:
        """Find and perform the action associated with the given target."""
        action = self.registry.parent(target)
        await self.tasks[action](Action(self, action))


@attr.dataclass(frozen=True)
class Action:
    """Wrapper that adapts a runtime action to the runner code."""

    target: Target
    action: RuntimeAction

    async def __call__(self) -> None:
        """Queue up all requirements, then carry out the action and report."""
        with self.target.reporter(self.action):
            async with trio.open_nursery() as nursery:
                for target in self.target.registry.inputs(self.action):
                    nursery.start_soon(self.target, target)
            result, data = await self.action()
            self.target.results[result].append((self.action, data))
            if result.aborted:
                raise motr.core.exc.MOTRTaskError(
                    f"Action {self.action!r} failed"
                )


async def run_all(
    request: typing.Callable[
        [motr.core.target.Target], typing.Awaitable[None]
    ],
    targets: typing.Iterable[motr.core.target.Target],
) -> None:
    """Map the given callable over all targets, asynchronously."""
    async with trio.open_nursery() as nursery:
        for target in targets:
            nursery.start_soon(request, target)
