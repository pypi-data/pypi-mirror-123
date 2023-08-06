import typing as t

from ingots.tests.units.bootstrap import test_base

from ingot_h2.bootstrap import IngotH2BaseBuilder

__all__ = ("IngotH2BaseBuilderTestCase",)


class IngotH2BaseBuilderTestCase(test_base.BaseBuilderTestCase):
    """Contains tests for the IngotH2Builder class."""

    tst_cls: t.Type = IngotH2BaseBuilder
    tst_entity_name: str = "ingot_h2"
    tst_entity_name_upper: str = "INGOT_H2"
    tst_entity_name_class_name: str = "IngotH2"
    tst_entity_description = (
        "Provides supporting HTTP/2 protocol via integration with the hyper h2 package."
    )
