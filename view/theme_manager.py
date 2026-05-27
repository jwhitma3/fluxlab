#  SPDX-License-Identifier: MIT
#  Copyright (c) 2026 Joshua C. Whitman

import json
from pathlib import Path

from PySide6.QtGui import QPalette, QColor
from cycler import cycler
from matplotlib import pyplot as plt

from utils.logger import get_logger

logger = get_logger(__name__)


class ThemeManager:
    def __init__(self, ui, theme_file):
        self.ui = ui
        self.theme_file = Path(theme_file)

        self.theme = self.load_theme()

        if self.theme:
            self.apply_theme_to_matplotlib()
            self.apply_theme_to_ui()

    def load_theme(self):
        try:
            with open(self.theme_file, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.error(f"Failed to load theme {self.theme_file.name}: {e}")
            return {}

    def get_color(self, key, namespace="app_tools"):
        if namespace in self.theme and key in self.theme[namespace]:
            return self.theme[namespace][key]

        logger.warning(f"Theme lookup failed: '{key}' not found in '{namespace}'.")
        return "#55FF33"  # Fallback to lime green fo debugging

    def apply_theme_to_matplotlib(self):
        if "matplotlib" not in self.theme:
            return

        for key, value in self.theme["matplotlib"].items():
            if key == "axes.prop_cycle":
                try:
                    plt.rcParams[key] = cycler(color=value)
                except Exception as e:
                    logger.error(f"Failed to set axes.prop_cycle: {e}")
                continue

            if key in plt.rcParams:
                plt.rcParams[key] = value
            else:
                logger.warning(f"'{key}' is not a valid Matplotlib parameter.")

    def apply_theme_to_ui(self):
        palette = self.ui.palette()
        logger.debug(f"Applying theme to UI: {self.theme_file.name}")

        # Base layer
        if "qt" in self.theme:
            logger.debug("Applying base theme to UI")
            for key, value in self.theme["qt"].items():
                logger.debug(f"Setting {key} to {value}")
                try:
                    role = getattr(QPalette.ColorRole, key)
                    palette.setColor(role, QColor(value))
                except AttributeError:
                    logger.warning(f"'{key}' is not a valid QPalette role.")

        # Inactive state
        if "qt_inactive" in self.theme:
            logger.debug("Applying inactive theme to UI")
            for key, value in self.theme["qt_inactive"].items():
                logger.debug(f"Setting {key} to {value}")
                try:
                    role = getattr(QPalette.ColorRole, key)
                    palette.setColor(QPalette.ColorGroup.Inactive, role, QColor(value))
                except AttributeError:
                    logger.warning(f"'{key}' in qt_inactive is invalid.")

        # Disabled state
        if "qt_disabled" in self.theme:
            logger.debug("Applying disabled theme to UI")
            for key, value in self.theme["qt_disabled"].items():
                logger.debug(f"Setting {key} to {value}")
                try:
                    role = getattr(QPalette.ColorRole, key)
                    palette.setColor(QPalette.ColorGroup.Disabled, role, QColor(value))
                except AttributeError:
                    logger.warning(f"'{key}' in qt_disabled is invalid.")

        self.ui.setPalette(palette)
