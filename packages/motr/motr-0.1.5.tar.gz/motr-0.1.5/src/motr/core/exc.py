"""MOTR-specific exception classes."""


class MOTRError(Exception):
    """Generic errors."""


class MOTRTaskError(MOTRError):
    """Task-based errors."""
