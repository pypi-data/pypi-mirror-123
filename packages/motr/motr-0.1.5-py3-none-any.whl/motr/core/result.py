"""Module for representing action outcomes."""

import enum


class Result(enum.Enum):
    """Enumeration of all three action outcomes."""

    PASSED = False, False
    FAILED = True, False
    ABORTED = True, True

    @property
    def failed(self) -> bool:
        """Return whether this outcome represents a failure."""
        return self.value[0]

    @property
    def aborted(self) -> bool:
        """Return whether this outcome should halt execution."""
        return self.value[1]
