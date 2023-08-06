"""Tests of the registry module."""

import re

import attr
import pytest


def exact_match(full_string):
    """Return a regex fragment that precisely matches the input string."""
    return f"^{re.escape(full_string)}$"


@attr.dataclass(frozen=True)
class null_action:
    """Helper class for stubbing Actions."""

    result: object


def test_import(registry):
    """Test that the registry module can be imported."""
    assert registry


def test_deleted(target):
    """Test that Deleted Tokens can be created."""
    assert target.deleted("path/to/file")


def test_not_implemented(registry):
    """Test the fallback case for the require() method."""
    testing_registry = registry.Registry()
    with pytest.raises(NotImplementedError):
        testing_registry.require(None)


def test_add_target_with_non_added_parent(registry):
    """Test that the parent of a string target must be added first."""
    testing_registry = registry.Registry()
    with pytest.raises(
        ValueError,
        match=exact_match(
            "Cannot add target 'test_target' with parent action 'action'."
            " Parent action 'action' has not been added to the registry."
        ),
    ):
        testing_registry.require(
            registry.ActionOutput("action", "test_target")
        )


def test_add_deleted_with_non_added_parent(registry, target):
    """Test that the parent of a token target must be added first."""
    testing_registry = registry.Registry()
    target = target.deleted("path/to/file")
    with pytest.raises(
        ValueError,
        match=exact_match(
            "Cannot add target Deleted(path='path/to/file') with parent "
            "action 'action'."
            " Parent action 'action' has not been added to the registry."
        ),
    ):
        testing_registry.require(registry.ActionOutput("action", target))


def test_add_target_with_different_parent(registry):
    """Test that a target cannot have two parent actions."""
    action = null_action(None)
    testing_registry = (
        registry.Registry()
        .require(registry.Action(action))
        .require(registry.ActionOutput(action, "test_target"))
    )
    with pytest.raises(
        ValueError,
        match=exact_match(
            "Cannot add target 'test_target' with parent action 'action'."
            " Target 'test_target' already has parent action"
            " null_action(result=None)."
        ),
    ):
        testing_registry.require(
            registry.ActionOutput("action", "test_target")
        )


def test_name_target(registry):
    """Test that targets can't be named before being added to the registry."""
    testing_registry = registry.Registry()
    with pytest.raises(
        ValueError,
        match=exact_match(
            "Cannot name target 'test_target' 'test_target'."
            " Target 'test_target' has not been added to the registry."
        ),
    ):
        testing_registry.require(
            registry.TargetName("test_target", "test_target")
        )


# Does this make sense?
def test_skip_non_existent_target(registry):
    """Test that unused target names cannot be skipped.

    I'm not sure if this is the proper behavior.
    """
    testing_registry = registry.Registry()
    with pytest.raises(
        ValueError,
        match=exact_match(
            "Cannot skip name 'test_target'."
            " Name 'test_target' has not been assigned to any target."
        ),
    ):
        testing_registry.require(registry.SkippedName("test_target"))


def test_add_deleted_via_api(api):
    """Test that the api.target function works."""
    for requirement in api.target(api.deleted("path"), "parent"):
        assert requirement


def test_add_action_twice(registry):
    """Test that adding actions to the registry is idempotent."""
    action = null_action(None)
    testing_registry = registry.Registry().require(registry.Action(action))
    assert testing_registry == testing_registry.require(
        registry.Action(action)
    )


def test_add_input_out_of_order(registry):
    """Test that a target cannot be a requirement of an unknown action."""
    testing_registry = registry.Registry()
    with pytest.raises(
        ValueError,
        match=exact_match(
            "Cannot add target 'test_input' as an input to action"
            " 'test_action'. Action 'test_action' has not been added to the"
            " registry."
        ),
    ):
        testing_registry.require(
            registry.ActionInput("test_action", "test_input")
        )


def test_add_to_wrong_child(registry):
    """Test that only the most recently added action can have a new target."""
    action_1 = null_action(1)
    action_2 = null_action(2)
    testing_registry = (
        registry.Registry()
        .require(registry.Action(action_1))
        .require(registry.Action(action_2))
        .require(registry.ActionOutput(action_2, "test_input"))
    )
    with pytest.raises(
        ValueError,
        match=exact_match(
            "Cannot add target 'test_input' as an input to action"
            " null_action(result=1). The most recently added action is"
            " null_action(result=2)."
        ),
    ):
        testing_registry.require(registry.ActionInput(action_1, "test_input"))


def test_add_input_not_added(registry):
    """Test that an action cannot require an untracked target."""
    action = null_action(None)
    testing_registry = registry.Registry().require(registry.Action(action))
    with pytest.raises(
        ValueError,
        match=exact_match(
            "Cannot add target 'test_target' as an input to action"
            " null_action(result=None)."
            " Target 'test_target' has not been added to the registry."
        ),
    ):
        testing_registry.require(registry.ActionInput(action, "test_target"))


def test_add_cycle(registry):
    """Test that an action cannot depend on its own output."""
    action = null_action(None)
    testing_registry = (
        registry.Registry()
        .require(registry.Action(action))
        .require(registry.ActionOutput(action, "target"))
    )
    with pytest.raises(
        ValueError,
        match=exact_match(
            "Cannot add target 'target' as an input to action"
            " null_action(result=None)."
            " The parent action of target 'target' is"
            " null_action(result=None)."
        ),
    ):
        testing_registry.require(registry.ActionInput(action, "target"))


def test_add_twice(registry):
    """Test that adding to the registry is idempotent."""
    action1 = object()
    action2 = object()
    action3 = object()
    requirements = [
        registry.Action(action1),
        registry.ActionOutput(action1, "target"),
        registry.Action(action2),
        registry.ActionInput(action2, "target"),
        registry.Action(action3),
    ]
    testing_registry = registry.Registry()
    for requirement in requirements:
        testing_registry = testing_registry.require(requirement)
    for requirement in requirements:
        testing_registry = testing_registry.require(requirement)
