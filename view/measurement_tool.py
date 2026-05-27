#  SPDX-License-Identifier: MIT
#  Copyright (c) 2026 Joshua C. Whitman

from enum import Enum, auto

from utils.logger import get_logger

logger = get_logger(__name__)


class SetupState(Enum):
    IDLE = auto()
    PLACING_X1 = auto()
    PLACING_X2 = auto()
    DRAGGING_X1 = auto()
    DRAGGING_X2 = auto()
    PLACING_Y1 = auto()
    PLACING_Y2 = auto()
    PLACING_Y3 = auto()
    DRAGGING_Y1 = auto()
    DRAGGING_Y2 = auto()
    DRAGGING_Y3 = auto()
    PLACING_F1 = auto()
    PLACING_F2 = auto()
    READY = auto()


class MeasurementTool:
    """
    Represents a visual tool for integrating the flux of an emission line
    """

    def __init__(self, axes):
        """
        The MeasurementTool attaches to the axes of a PlotCanvas
        and listens for events to update the visuals
        """

        self.continuum_bounds = None
        self.flux_bounds = None
        self.axes = axes
        self.canvas = axes.figure.canvas
        self.flux_bound_color = "#308cc9"
        self.cont_bound_color = "#308cc9"

        self.state = SetupState.IDLE

        self._active_line = None
        self._lmb_held = False

        self.initialize_lines()
        self.connect_events()

    def initialize_lines(self):
        self.flux_bounds = [
            self.axes.axvline(0, color=self.flux_bound_color, ls="--", visible=False),
            self.axes.axvline(0, color=self.flux_bound_color, ls="--", visible=False),
        ]
        self.continuum_bounds = [
            self.axes.axvline(0, color=self.cont_bound_color, ls="--", visible=False),
            self.axes.axvline(0, color=self.cont_bound_color, ls="--", visible=False),
        ]
        logger.debug("Setup state: IDLE")

    def remove(self):
        for line in self.flux_bounds:
            line.remove()
        for line in self.continuum_bounds:
            line.remove()

        self.canvas.draw_idle()

    def connect_events(self):
        canvas = self.axes.figure.canvas
        canvas.mpl_connect("button_press_event", self.on_mouse_press)
        canvas.mpl_connect("button_release_event", self.on_mouse_release)
        canvas.mpl_connect("motion_notify_event", self.on_mouse_move)

    def on_mouse_press(self, event):
        if event.inaxes is not self.axes or event.button != 1:
            return
        logger.debug("LMB pressed")

        xdata, _ = self.axes.transData.inverted().transform((event.x, event.y))

        if self.state == SetupState.IDLE:
            self.set_flux_bounds(left=xdata)
            logger.debug(f"event.x: {xdata}")

            self.state = SetupState.PLACING_X2
            logger.debug("Setup state: PLACING_X2")

    def set_flux_bounds(self, left=None, right=None):
        logger.debug(f"Setting flux bounds: {left}, {right}")
        if left is not None:
            logger.debug(f"Setting left bound to {left}")
            self.flux_bounds[0].set_xdata([left, left])
            self.flux_bounds[0].set_visible(True)
            self.canvas.draw_idle()
            logger.debug(f"Left bound visible: {self.flux_bounds[0].get_visible()}")
        if right is not None:
            self.flux_bounds[1].set_xdata([right, right])
            self.flux_bounds[1].set_visible(True)

    def on_mouse_release(self, event):
        pass

    def on_mouse_move(self, event):
        pass
