from __future__ import annotations

import typing

import motr.core.registry

if typing.TYPE_CHECKING:
    import motr._api.requirements.requirements


def build(
    requirements: motr._api.requirements.requirements.Requirements,
) -> motr.core.registry.Registry:
    """Return a registry created from a sequence of requirements."""
    registry = motr.core.registry.Registry()
    for requirement in requirements:
        registry = registry.require(requirement)
    return registry
