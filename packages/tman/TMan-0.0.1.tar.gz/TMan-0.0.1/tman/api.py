#  Copyright (c) 2021, Daniel Mouritzen.

"""Defines the public API."""

from pathlib import Path

import attr
from loguru import logger


@attr.s
class TManAPI:
    """Main API handle."""

    data_dir: Path = attr.ib(converter=Path)
    config_file: Path = attr.ib(converter=Path)

    def __attrs_post_init__(self) -> None:
        logger.info(f"Data: {self.data_dir}")
        logger.info(f"Config: {self.config_file}")
