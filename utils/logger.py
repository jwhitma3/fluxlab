#  SPDX-License-Identifier: MIT
#  Copyright (c) 2026 Joshua C. Whitman

import logging
import os


def get_logger(name):
    logger = logging.getLogger(name)

    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.DEBUG)

    env = os.getenv("APP_ENV", "development")

    dev_formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)-8s %(name)s:%(lineno)d -> %(message)s",
        datefmt="%H:%M:%S",
    )

    prod_formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S%z",
    )

    if env == "development":
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(dev_formatter)
        logger.addHandler(console_handler)

    else:
        file_handler = logging.FileHandler("production_errors.log", encoding="utf-8")
        file_handler.setLevel(logging.WARNING)
        file_handler.setFormatter(prod_formatter)
        logger.addHandler(file_handler)

    return logger
