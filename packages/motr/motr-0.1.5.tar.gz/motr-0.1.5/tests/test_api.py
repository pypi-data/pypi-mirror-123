"""Tests for the public api module."""

import pathlib
import types
from unittest import mock

import pytest
import trio.testing


def make_run_process(returncode):
    """Return a suitable run_process stub for mocking behavior."""

    async def run_process(command, capture_stdout, capture_stderr, check, env):
        return types.SimpleNamespace(
            returncode=returncode, stdout=b"", stderr=b""
        )

    return run_process


def test_import(api):
    """Test that the module is importable."""
    assert api


def test_cmd(api, io):
    """Test the cmd function."""
    string = pathlib.Path("string")
    env = pathlib.Path("env")
    for requirement in api.cmd(
        ["str", io.Input(string / "in"), io.Input(string / "out").as_output()],
        "test_cmd",
        env={
            "IN": io.Input(env / "in"),
            "OUT": io.Input(env / "out").as_output(),
        },
    ):
        assert requirement


def test_mkdir(api, io):
    """Test the mkdir function."""
    for requirement in api.mkdir(
        io.Input(pathlib.Path("test-path")),
    ):
        assert requirement


def test_write_bytes(api, io):
    """Test the write_bytes function."""
    for requirement in api.write_bytes(
        io.Input(pathlib.Path("test-path")), b"test-data"
    ):
        assert requirement


@pytest.mark.parametrize(
    "returncode,expected", [(0, "PASSED"), (1, "FAILED"), (2, "ABORTED")]
)
@trio.testing.trio_test
async def test_inner_cmd(cmd, result, returncode, expected):
    """Test that the Cmd class properly handles different return codes."""
    test_cmd = cmd.Cmd((), allowed_codes=frozenset([1]))
    with mock.patch("trio.run_process", new=make_run_process(returncode)):
        my_result, mapping = await test_cmd()
    assert result.Result[expected] is my_result


@trio.testing.trio_test
async def test_inner_mkdir_success(mkdir, result, tmp_path):
    """Test that the Mkdir class can create a directory that doesn't exist."""
    test_path = tmp_path / "test-path"
    my_result, mapping = await mkdir.Mkdir(test_path)()
    assert result.Result.PASSED is my_result


@trio.testing.trio_test
async def test_inner_mkdir_failure(mkdir, result, tmp_path):
    """Test that the Mkdir class can't create a directory over a file."""
    test_path = tmp_path / "test-path"
    test_path.touch()
    my_result, mapping = await mkdir.Mkdir(test_path)()
    assert result.Result.ABORTED is my_result


@trio.testing.trio_test
async def test_inner_write_bytes_success(write_bytes, result, tmp_path):
    """Test that the WriteBytes class can write a file that doesn't exist."""
    test_path = tmp_path / "test-path"
    my_result, mapping = await write_bytes.WriteBytes(test_path, b"")()
    assert result.Result.PASSED is my_result


@trio.testing.trio_test
async def test_inner_write_bytes_failure(write_bytes, result, tmp_path):
    """Test that the WriteBytes class can't write a file over a directory."""
    test_path = tmp_path / "test-path"
    test_path.mkdir()
    my_result, mapping = await write_bytes.WriteBytes(test_path, b"")()
    assert result.Result.ABORTED is my_result
