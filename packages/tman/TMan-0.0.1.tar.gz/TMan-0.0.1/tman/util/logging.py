#  Copyright (c) 2021, Daniel Mouritzen.

"""Various logging functionality."""

import inspect
import logging
import sys
from pathlib import Path
from typing import Any, Dict, Mapping, Optional, Union

from loguru import logger


class InterceptHandler(logging.Handler):
    """
    Handler to force stdlib logging to go through loguru.

    Based on https://github.com/Delgan/loguru/issues/78
    """

    def __init__(
        self,
        level: int = logging.NOTSET,
        module_levels: Optional[Mapping[str, str]] = None,
    ):
        super().__init__(level)
        self._module_levels = {} if module_levels is None else module_levels
        for mod, lev in self._module_levels.items():
            logging.getLogger(mod).setLevel(lev)

    def emit(self, record: logging.LogRecord) -> None:
        """Process log record and log with loguru."""
        depth = self._get_depth()
        logger_opt = logger.opt(depth=depth, exception=record.exc_info)
        for line in record.getMessage().split("\n"):
            level = record.levelname
            level_: Union[str, int] = int(level[6:]) if level.startswith("Level ") else level
            logger_opt.log(level_, line.rstrip())

    @staticmethod
    def _get_depth() -> int:
        """Find out how far back to go in the stack trace to find the original source file."""
        try:
            frame = inspect.currentframe().f_back.f_back  # type: ignore[union-attr]
        except AttributeError:
            frame = None
        depth = 1
        while frame is not None and depth < 20:
            file = inspect.getsourcefile(frame) or inspect.getfile(frame)
            if file != logging.__file__:
                break
            frame = frame.f_back
            depth += 1
        return depth


def init_logging(verbosity: str, logdir: Union[str, Path]) -> None:
    """
    Configure loggers according to specified verbosity level and log directory.

    Should be called at the program's main entrypoint.
    """
    # Remove default loguru logger
    logger.remove()

    # Intercept all third-party logging
    logging.basicConfig(handlers=[InterceptHandler()], level=0)

    # Log to stdout and logfiles
    trace_logfile = Path(logdir) / "trace.log"
    info_logfile = Path(logdir) / "info.log"
    kwargs: Dict[str, Any] = dict(backtrace=True, diagnose=True, enqueue=True)
    logger.add(trace_logfile, level="TRACE", **kwargs)
    kwargs["format"] = "<level>[{level.name[0]}] {time:HH:mm:ss}</level> {message}"
    logger.add(info_logfile, level="INFO", **kwargs)
    logger.add(sys.stdout, level=verbosity, **kwargs)

    logger.debug("Logging initialized.")
    logger.debug(f"Logging to {info_logfile} and {trace_logfile}.")
