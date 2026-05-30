#  SPDX-License-Identifier: MIT
#  Copyright (c) 2026 Joshua C. Whitman

import logging
from dataclasses import dataclass
from datetime import datetime as dt
from pathlib import Path

import numpy as np
from PySide6.QtCore import QObject, Signal

import model.utilities as utils


@dataclass
class Measurement:
    # Database & Audit Metadata
    id: int
    sequence: int
    created_dt: dt
    created_by: str
    status: str
    status_dt: dt
    status_by: str

    # Measurement Results
    peak_wavelength: float
    central_wavelength: float
    flux: tuple[float, float, float]
    flux_error: float

    # Integration
    integration_bounds: tuple[float, float]

    # Continuum Fitting
    fit_method: str
    continuum_bounds: tuple[float, float]
    upper_continuum_coefficients: tuple[float, ...]
    lower_continuum_coefficients: tuple[float, ...]
    central_continuum_coefficients: tuple[float, ...]


logger = logging.getLogger(__name__)


class SpectrumModel(QObject):
    spectrum_loaded = Signal()

    def __init__(self):
        super().__init__()
        self._spectrum = None
        self._step_x = None
        self._step_y = None
        self._boundaries = None

    def load_sample_data(self):
        file_path = Path.cwd() / "data" / "Sample_Flux.fits"

        try:
            self._spectrum = utils.import_specturm(file_path)

            self._boundaries = self.get_boundaries()
            self._step_x, self._step_y = self.create_step_profile()

            self.spectrum_loaded.emit()

        except Exception as e:
            logger.error(f"Failed to load spectrum: {e}")

    def get_boundaries(self):
        x = np.asarray(self.spectrum.wavelength)
        N = len(x)

        # Calculate the midpoints and boundaries
        midpoints = (x[1:] + x[:-1]) / 2

        left_edge = x[0] - (x[1] - x[0]) / 2
        right_edge = x[-1] + (x[-1] - x[-2]) / 2

        boundaries = np.empty(N + 1)
        boundaries[0] = left_edge
        boundaries[1:-1] = midpoints
        boundaries[-1] = right_edge

        return boundaries

    def get_nearest_wavelength(self, x):
        if self._boundaries is None:
            raise RuntimeError(
                "Spectrum boundaries not set. "
                "Call SpectrumModel.load_sample_data() first."
            )
        if x is None:
            raise ValueError("x cannot be None")

        if not isinstance(x, (int, float)):
            raise TypeError("x must be a number")

        if np.isnan(x):
            raise ValueError("x cannot be NaN")
        # The provided x value is beyond the boundaries of the spectrum
        if x < self._boundaries[0]:
            return self._boundaries[0]
        if x > self._boundaries[-1]:
            return self._boundaries[-1]

        # Nearest index to the left of x
        idx = np.searchsorted(self._boundaries, x, side="left")

        #
        left_val = self._boundaries[idx - 1]
        right_val = self._boundaries[idx]
        if abs(x - left_val) < abs(x - right_val):
            return left_val
        else:
            return right_val

    def create_step_profile(self):
        x = np.asarray(self.spectrum.wavelength)
        y = np.asarray(self.spectrum.flux)

        x_unit = self.spectrum.wavelength.unit
        y_unit = self.spectrum.flux.unit

        N = len(x)

        # Create the step profile
        step_x = np.empty(2 * N)
        step_y = np.empty(2 * N)

        step_x[0::2] = self._boundaries[:-1]  # Left Edges
        step_x[1::2] = self._boundaries[1:]  # Right Edges

        step_y[0::2] = y
        step_y[1::2] = y

        # Re-attach units to the step profile
        qty_step_x = step_x * x_unit
        qty_step_y = step_y * y_unit
        return qty_step_x, qty_step_y

    @property
    def spectrum(self):
        return self._spectrum

    @property
    def step_x(self):
        return self._step_x

    @property
    def step_y(self):
        return self._step_y

    @property
    def object_name(self):
        if self.spectrum.meta["header"]["OBJECT"] is None:
            return "Spectrum"
        else:
            return self.spectrum.meta["header"]["OBJECT"]

    @property
    def wavelength_unit(self):
        return self.spectrum.wavelength.unit

    @property
    def flux_unit(self):
        return self.spectrum.flux.unit
