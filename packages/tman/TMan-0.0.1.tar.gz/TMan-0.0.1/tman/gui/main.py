#  Copyright (c) 2021, Daniel Mouritzen.

"""Main GUI entry point."""

import PySimpleGUI as sg
from appdirs import user_config_dir, user_data_dir, user_log_dir
from loguru import logger

from tman.api import TManAPI
from tman.util.logging import init_logging


def main() -> None:
    """Start GUI."""
    app_name = "TMan"
    init_logging(verbosity="DEBUG", logdir=user_log_dir(app_name))

    logger.debug("Initializing backend")
    api = TManAPI(  # noqa: F841
        data_dir=user_data_dir(app_name), config_file=user_config_dir(app_name) + "/config.json"
    )

    logger.debug("Starting UI")
    sg.theme("DarkBlue")
    layout = [
        [sg.Text("Some text on Row 1")],
        [sg.Text("Enter something on Row 2"), sg.InputText()],
        [sg.Button("Ok"), sg.Button("Cancel")],
    ]
    window = sg.Window("Window Title", layout)
    while True:
        event, values = window.read()
        if event in (None, "Cancel"):
            break
        logger.info(f"You entered {values[0]}")
    window.close()

    logger.info("Finished successfully.")
