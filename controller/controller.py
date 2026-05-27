#  SPDX-License-Identifier: MIT
#  Copyright (c) 2026 Joshua C. Whitman

from utils.logger import get_logger

logger = get_logger(__name__)


class AppController:
    def __init__(self, model, window):
        self.model = model
        self.window = window
        self.canvas = self.window.canvas
        self.axes = self.canvas.axes
        self.measurement_tool = None
        self.connect_signals()

    def connect_signals(self):
        self.window.ui.actionLoad_Sample_Data.triggered.connect(
            self.on_load_sample_data_triggered
        )

        self.model.spectrum_loaded.connect(self.on_spectrum_loaded)
        self.window.new_measurement_signal.connect(self.on_place_measurement_tool)

    def on_load_sample_data_triggered(self):
        logger.info("Loading sample data...")

        self.model.load_sample_data()

    def on_spectrum_loaded(self):
        x_step = self.model.step_x
        y_step = self.model.step_y
        target_name = self.model.object_name
        x_label = f"Wavelength ({self.model.wavelength_unit})"
        y_label = f"Flux ({self.model.flux_unit})"

        self.canvas.plot_spectrum(x_step, y_step, target_name, x_label, y_label)

    def on_place_measurement_tool(self):
        if self.model.spectrum is None:
            logger.debug("No spectrum loaded")
            return
        if self.measurement_tool is not None:
            self.measurement_tool.remove()
            self.measurement_tool = None
            return

        from view.measurement_tool import MeasurementTool

        self.measurement_tool = MeasurementTool(self.axes)

        logger.info("Placing measurement tool...")
