"""Test the result module."""

import pytest


@pytest.mark.parametrize("name", ["PASSED", "FAILED", "ABORTED"])
def test_failed(result, name):
    """Test that the failed method works as expected.

    This is mainly for coverage of a function that exists for the sake of
    symmetry.
    """
    failed = name != "PASSED"
    assert result.Result[name].failed is failed
