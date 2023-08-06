from __future__ import annotations

import typing

import motr.core.registry
import motr.core.target
import motr.core.target_name

if typing.TYPE_CHECKING:
    import motr._api.requirements.requirements


def name_target(
    coerce_to_target: motr.core.target.CoerceToTarget, name: str
) -> motr._api.requirements.requirements.Requirements:
    """Yield the requirements associated with naming a Target."""
    target = motr.core.target.coerce(coerce_to_target)
    target_name = motr.core.target_name.coerce(name)
    yield motr.core.registry.TargetName(target, target_name)
