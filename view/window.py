#  SPDX-License-Identifier: MIT
#  Copyright (c) 2026 Joshua C. Whitman

import sys
from pathlib import Path

import qtawesome
from PySide6.QtCore import QFile, Signal, QObject
from PySide6.QtGui import QAction
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QToolBar, QVBoxLayout

from utils.logger import get_logger
from view.canvas import PlotCanvas
from view.theme_manager import ThemeManager

logger = get_logger(__name__)


def get_resource_path(relative_path: str) -> Path:
    base_path = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent.parent))
    return base_path / relative_path


class AppWindow(QObject):
    new_measurement_signal = Signal()

    def __init__(self):
        super().__init__()

        self.new_measurement_action = None
        self.ui = None
        self.main_toolbar = None
        self.theme_file = get_resource_path("themes/dark.theme.json")

        self.reset_view_action = None
        self.box_zoom_action = None

        self.load_ui()

        self.theme_manager = ThemeManager(self.ui, self.theme_file)

        self.setup_toolbars()

        self.canvas = PlotCanvas()
        self.attach_canvas_to_ui()

    def load_ui(self):

        ui_file_path = Path(__file__).parent / "main_window.ui"
        ui_file = QFile(str(ui_file_path))

        # Ensure the file exists
        if not ui_file.open(QFile.ReadOnly):
            logger.critical(f"Cannot open {ui_file_path}: {ui_file.errorString()}")
            sys.exit(-1)

        # Load the UI file
        self.ui = QUiLoader().load(ui_file)
        ui_file.close()

    def show(self, width=1200, height=800):
        self.ui.show()
        self.ui.resize(width, height)

    def setup_toolbars(self):
        self.main_toolbar = QToolBar("Tools")
        self.main_toolbar.setMovable(False)
        self.main_toolbar.setIconSize(self.ui.iconSize())
        self.ui.addToolBar(self.main_toolbar)

        # Box Zoom
        box_zoom_icon = qtawesome.icon("mdi6.magnify-scan")
        self.box_zoom_action = QAction(box_zoom_icon, "Box Zoom", self.ui)
        self.box_zoom_action.setToolTip("Box Zoom")
        self.box_zoom_action.triggered.connect(self.on_box_zoom)

        # Reset View
        reset_view_icon = qtawesome.icon("ph.arrows-out")
        self.reset_view_action = QAction(reset_view_icon, "Reset View", self.ui)
        self.reset_view_action.setToolTip("Reset View")
        self.reset_view_action.triggered.connect(self.on_reset_view)

        # New Measurement
        new_measurement_icon = qtawesome.icon("mdi6.math-compass")
        self.new_measurement_action = QAction(
            new_measurement_icon, "New Measurement", self.ui
        )
        self.new_measurement_action.setToolTip("New Measurement")
        self.new_measurement_action.triggered.connect(self.new_measurement_signal.emit)

        # Attach actions to the toolbar
        self.main_toolbar.addAction(self.box_zoom_action)
        self.main_toolbar.addAction(self.reset_view_action)
        self.main_toolbar.addAction(self.new_measurement_action)

    def attach_canvas_to_ui(self):
        layout = self.ui.plot_container.layout()
        if layout is None:
            layout = QVBoxLayout(self.ui.plot_container)
        layout.addWidget(self.canvas)

    def on_box_zoom(self):
        pass

    def on_reset_view(self):
        pass
