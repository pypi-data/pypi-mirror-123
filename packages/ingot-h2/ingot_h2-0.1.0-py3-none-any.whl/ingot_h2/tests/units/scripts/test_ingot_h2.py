import typing as t

from ingots.tests.units.scripts import test_base

from ingot_h2.scripts.ingot_h2 import IngotH2Dispatcher

__all__ = ("IngotH2DispatcherTestCase",)


class IngotH2DispatcherTestCase(test_base.BaseDispatcherTestCase):
    """Contains tests for the IngotH2Dispatcher class and checks it."""

    tst_cls: t.Type = IngotH2Dispatcher
    tst_builder_name = "test"
