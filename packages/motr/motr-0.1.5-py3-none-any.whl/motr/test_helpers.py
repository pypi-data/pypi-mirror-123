"""Helpers for writing tests against MOTR.

May also be useful for plugins or extensions.
"""

from cement import TestApp

import motr.motr_app


class MOTRTest(TestApp, motr.motr_app.MOTR):
    """A sub-class of MOTR that is better suited for testing."""

    class Meta:
        """The metadata for the test-helping class."""

        label = "motr"
