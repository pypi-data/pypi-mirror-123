from __future__ import annotations

import typing

import motr.core.registry
import motr.core.target

if typing.TYPE_CHECKING:
    import motr._api.requirements.requirements
    import motr.core.runner


def action(
    runtime_action: motr.core.runner.RuntimeAction,
    *args: motr.core.target.CoerceToTarget,
) -> motr._api.requirements.requirements.Requirements:
    """Yield the requirements associated with a runtime action."""
    yield motr.core.registry.Action(runtime_action)
    for arg in args:
        target = motr.core.target.coerce(arg)
        yield motr.core.registry.ActionInput(runtime_action, target)
