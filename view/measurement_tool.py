#  SPDX-License-Identifier: MIT
#  Copyright (c) 2026 Joshua C. Whitman

from enum import Enum, auto

import numpy as np
from PySide6.QtCore import Signal, QObject
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg

from utils.logger import get_logger
from view.theme_manager import AppTheme

logger = get_logger(__name__)


class ToolState(Enum):
    IDLE = auto()
    PLACING_LEFT_FLUX = auto()
    PLACING_RIGHT_FLUX = auto()


class MeasurementTool(QObject):
    """
    Represents a visual tool for integrating the flux of an emission line
    """

    flux_bounds_changed = Signal()
    continuum_bounds_changed = Signal()

    def __init__(self, axes, theme: AppTheme):
        """
        The MeasurementTool attaches to the axes of a PlotCanvas
        and listens for events to update the visuals
        """
        super().__init__()
        self.cid_release = None
        self.cid_press = None
        self.cid_pick = None
        self.cid_motion = None
        self.theme = theme
        self.axes = axes
        self.canvas: FigureCanvasQTAgg = self.axes.figure.canvas
        self.center = np.average(axes.get_xlim())

        self.flux_bounds = (None, None)
        self.continuum_bounds = (None, None)

        self.left_flux_line = self.VLine(self)
        self.right_flux_line = self.VLine(self)
        self.left_continuum_line = self.VLine(self)
        self.right_continuum_line = self.VLine(self)
        self.tool_state = ToolState.PLACING_LEFT_FLUX
        self._connect_signals()
        self.canvas.draw_idle()

    def _connect_signals(self):
        self.cid_motion = self.canvas.mpl_connect(
            "motion_notify_event", self.on_mouse_move
        )
        self.cid_pick = self.canvas.mpl_connect("pick_event", self.on_click)
        self.cid_press = self.canvas.mpl_connect(
            "button_press_event", self.on_mouse_press
        )
        self.cid_release = self.canvas.mpl_connect(
            "button_release_event", self.on_mouse_release
        )

    def lines(self):
        return [
            self.left_flux_line,
            self.right_flux_line,
            self.left_continuum_line,
            self.right_continuum_line,
        ]

    def _disconnect_signals(self):
        if self.cid_motion is not None:
            self.canvas.mpl_disconnect(self.cid_motion)
        if self.cid_pick is not None:
            self.canvas.mpl_disconnect(self.cid_pick)
        if self.cid_press is not None:
            self.canvas.mpl_disconnect(self.cid_press)
        if self.cid_release is not None:
            self.canvas.mpl_disconnect(self.cid_release)

    def remove(self):
        self._disconnect_signals()
        for line in self.lines():
            line.remove()
        self.canvas.draw_idle()

    def on_mouse_press(self, event):
        if event.inaxes is not self.axes:
            return
        if event.button == 1:

            # User is placing the left flux line
            if self.tool_state == ToolState.PLACING_LEFT_FLUX:
                # Place the left flux line
                self.left_flux_line.place(event.xdata)
                self.canvas.draw_idle()

                self.flux_bounds = (event.xdata, self.flux_bounds[1])
                # User is now placing the right flux line
                self.tool_state = ToolState.PLACING_RIGHT_FLUX

                return

            # User is placing the right flux line
            if self.tool_state == ToolState.PLACING_RIGHT_FLUX:
                # Place the right flux line
                self.right_flux_line.place(event.xdata)
                self.canvas.draw_idle()

                self.flux_bounds = (self.flux_bounds[0], event.xdata)

                # Both flux lines placed, emit signal
                self.flux_bounds_changed.emit()
                self.tool_state = ToolState.IDLE
                return

    def on_mouse_release(self, event):
        pass

    def on_mouse_move(self, event):
        if event.inaxes is not self.axes:
            if self.tool_state == ToolState.PLACING_LEFT_FLUX:
                self.left_flux_line.set_visible(False)
                self.canvas.draw_idle()
            return
        if self.tool_state == ToolState.PLACING_LEFT_FLUX:
            self.left_flux_line.set_visible(True)
            self.left_flux_line.set_x(event.xdata)
            self.canvas.draw_idle()

        if self.tool_state == ToolState.PLACING_RIGHT_FLUX:
            self.right_flux_line.set_visible(True)
            self.right_flux_line.set_x(event.xdata)
            self.canvas.draw_idle()

    def on_click(self, event):
        pass

    class VLine:
        def __init__(self, parent, x=None):
            self.theme: AppTheme = parent.theme
            self._axes = parent.axes
            self.center = parent.center
            self._line = self._make_line()

        def _make_line(self):
            return self._axes.axvline(
                x=self.center,
                color=self.theme.tool_base,
                linestyle="--",
                picker=5,
                alpha=0.5,
                linewidth=1.5,
                visible=False,
            )

        def place(self, x):
            self._line.set_xdata([x, x])
            self._line.set_visible(True)
            self._line.set_alpha(1.0)

        def set_x(self, x):
            self._line.set_xdata([x, x])

        def set_visible(self, visible):
            self._line.set_visible(visible)

        def remove(self):
            if self._line in self._axes.lines:
                try:
                    self._line.remove()
                except Exception as e:
                    logger.error(f"Failed to remove line: {e}")
