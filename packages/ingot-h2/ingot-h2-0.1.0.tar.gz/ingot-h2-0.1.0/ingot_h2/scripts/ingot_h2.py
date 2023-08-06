import typing as t
from logging import getLogger
from logging import INFO

from ingots.scripts.base import BaseDispatcher
from ingots.utils.logging import configure_startup_logging

if t.TYPE_CHECKING:
    from ingots.operations import BaseCliOperation  # noqa


__all__ = (
    "IngotH2Dispatcher",
    "main",
)


configure_startup_logging(
    default_level=INFO,
    format="%(levelname)s: %(message)s",
)
logger = getLogger(__name__)


class IngotH2Dispatcher(BaseDispatcher):

    name = "ingot_h2"
    description = "The Ingot H2 management CLI."
    cli_entities_classes: t.List[t.Type["BaseCliOperation"]] = []


def main():
    dispatcher = IngotH2Dispatcher.build()
    dispatcher.run()


if __name__ == "__main__":
    main()
