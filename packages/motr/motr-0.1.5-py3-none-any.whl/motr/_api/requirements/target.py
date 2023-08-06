from __future__ import annotations

import typing

import motr._api.requirements.name_target
import motr.core.registry
import motr.core.target

if typing.TYPE_CHECKING:
    import motr._api.requirements.requirements
    import motr.core.runner


def target(
    coerce_to_target: motr.core.target.CoerceToTarget,
    parent: motr.core.runner.RuntimeAction,
    *args: str
) -> motr._api.requirements.requirements.Requirements:
    """Yield the requirements associated with a Target."""
    target = motr.core.target.coerce(coerce_to_target)
    yield motr.core.registry.ActionOutput(parent, target)
    for arg in args:
        yield from motr._api.requirements.name_target.name_target(
            coerce_to_target, arg
        )
