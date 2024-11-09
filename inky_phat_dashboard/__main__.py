"""The main module for the inky_phat_dashboard package."""

import asyncio
import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from inky_phat_dashboard.const import (
    DEFAULT_CONFIG_FILE_PATH,
    DEFAULT_LOG_PATH,
    ENV_CONFIG_FILE_PATH,
    ENV_LOG_FILE_PATH,
)
from inky_phat_dashboard.dashboard import Dashboard
from inky_phat_dashboard.models import Config


async def main():
    load_dotenv()

    config_file_path = Path(
        os.getenv(ENV_CONFIG_FILE_PATH, default=DEFAULT_CONFIG_FILE_PATH)
    )

    config = Config.load(config_file_path)

    if config is None:
        logging.error(f"Config could not be loaded from {config_file_path}")
        asyncio.get_event_loop().stop()
        return

    init_logger(config)

    logging.info("Starting inky-phat-dashboard service...")
    logging.info(f"Working directory: {os.getcwd()}")
    logging.info(f"Config file path: {config_file_path}")
    logging.info(f"Log file path: {config.logging_config.path}")

    dashboard = Dashboard(config)
    await dashboard.start()


def init_logger(config: Config):
    """Initialize the logger."""

    log_file_path = Path(
        config.logging_config.path or os.getenv(ENV_LOG_FILE_PATH) or DEFAULT_LOG_PATH
    )

    config.logging_config.path = log_file_path

    if not log_file_path.is_absolute():
        log_file_path = config.config_file_path.parent / log_file_path

    logging.basicConfig(
        level=config.logging_config.level.upper(),
        format=config.logging_config.fmt,
        datefmt=config.logging_config.datefmt,
        handlers=[
            logging.FileHandler(log_file_path, mode=config.logging_config.filemode),
            logging.StreamHandler(sys.stdout),
        ],
    )


if __name__ == "__main__":
    asyncio.run(main())
