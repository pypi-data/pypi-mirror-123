from logging import getLogger

from ingots.bootstrap.base import BaseBuilder

import ingot_h2 as package

__all__ = ("IngotH2BaseBuilder",)


logger = getLogger(__name__)


class IngotH2BaseBuilder(BaseBuilder):

    package = package
