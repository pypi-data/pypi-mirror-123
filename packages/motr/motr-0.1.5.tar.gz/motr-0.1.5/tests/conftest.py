"""Common fixtures for testing MOTR."""

import enum
import pathlib
import tempfile

import pytest


@pytest.fixture(autouse=True)
def _restore_cwd(monkeypatch, base):
    monkeypatch.setattr(base, "chdir", monkeypatch.chdir)


class ToParent(enum.Enum):
    """Helper class for representing values for the to_parent fixture."""

    SELF = False
    PARENT = True


@pytest.fixture
def to_tmpdir(monkeypatch):
    """Run the test from a temporary directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        monkeypatch.chdir(tmpdir)
        yield tmpdir


@pytest.fixture(params=list(ToParent))
def to_parent(request):
    """Return whether the motrfile should be in a parent directory."""
    return request.param.value


@pytest.fixture
def implicit_expected(to_tmpdir, to_parent, monkeypatch):
    """Return the path that MOTR will look for the motrfile at."""
    target = pathlib.Path(".")
    if to_parent:
        target /= "child"
        target.mkdir()
        monkeypatch.chdir(target)
    return pathlib.Path("motrfile.py").resolve()


@pytest.fixture
def implicit_actual(implicit_expected, to_tmpdir):
    """Return the path that MOTR will find the motrfile at."""
    return to_tmpdir / pathlib.Path("motrfile.py")


@pytest.fixture(scope="session", name="test_helpers")
def _test_helpers():
    import motr.test_helpers

    return motr.test_helpers


@pytest.fixture(scope="session")
def main():
    """Return the motr.main module."""
    import motr.main

    return motr.main


@pytest.fixture(scope="session")
def exc():
    """Return the motr.core.exc module."""
    import motr.core.exc

    return motr.core.exc


@pytest.fixture(scope="session")
def registry():
    """Return the motr.core.registry module."""
    import motr.core.registry

    return motr.core.registry


@pytest.fixture(scope="session")
def result():
    """Return the motr.core.result module."""
    import motr.core.result

    return motr.core.result


@pytest.fixture(scope="session")
def runner():
    """Return the motr.core.runner module."""
    import motr.core.runner

    return motr.core.runner


@pytest.fixture(scope="session")
def target():
    """Return the motr.core.target module."""
    import motr.core.target

    return motr.core.target


@pytest.fixture(scope="session")
def base():
    """Return the motr.controllers.base module."""
    import motr.controllers.base

    return motr.controllers.base


@pytest.fixture(scope="session")
def api():
    """Return the motr.api module."""
    import motr.api

    return motr.api


@pytest.fixture(scope="session")
def io():
    """Return the motr._api.actions.io module."""
    import motr._api.actions.io

    return motr._api.actions.io


@pytest.fixture(scope="session")
def cmd():
    """Return the motr._api.actions.cmd module."""
    import motr._api.actions.cmd

    return motr._api.actions.cmd


@pytest.fixture(scope="session")
def mkdir():
    """Return the motr._api.actions.mkdir module."""
    import motr._api.actions.mkdir

    return motr._api.actions.mkdir


@pytest.fixture(scope="session")
def write_bytes():
    """Return the motr._api.actions.write_bytes module."""
    import motr._api.actions.write_bytes

    return motr._api.actions.write_bytes


@pytest.fixture(scope="session")
def requirements():
    """Return the motr._api.requirements.requirements module."""
    import motr._api.requirements.requirements

    return motr._api.requirements.requirements
