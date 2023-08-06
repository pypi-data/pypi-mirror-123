from __future__ import annotations

import typing

import motr.core.registry
import motr.core.target_name

if typing.TYPE_CHECKING:
    import motr._api.requirements.requirements


def skipped_name(
    name: str,
) -> motr._api.requirements.requirements.Requirements:
    """Yield the requirements associated with skipping a target name."""
    target_name = motr.core.target_name.coerce(name)
    yield motr.core.registry.SkippedName(target_name)
