#  SPDX-License-Identifier: MIT
#  Copyright (c) 2026 Joshua C. Whitman

from PySide6.QtCore import Qt
from matplotlib.backend_bases import MouseEvent, Event, KeyEvent
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from utils.logger import get_logger

logger = get_logger(__name__)


class PlotCanvas(FigureCanvasQTAgg):
    """
    The canvas where the plotted figures are drawn
    """

    def __init__(self, parent=None):
        # A blank matplotlib figure
        self.fig = Figure(tight_layout=True)

        # Add a single subplot to the figure
        self.axes = self.fig.add_subplot(111)

        # Initialize the axes with default styles
        self._initialize_blank_axes()

        # Initialize the canvas with the figure
        super().__init__(self.fig)
        self.setParent(parent)
        self.setFocusPolicy(Qt.StrongFocus)

        self.connect_signals()

        # State variables
        self._is_panning = False
        self._rmb_event_location = None
        self.tool_placement_step = 0
        self._initial_xlim = None
        self._initial_ylim = None

    def _initialize_blank_axes(self):
        self.axes.grid(linestyle=":", linewidth=1, alpha=0.5)
        self.draw_idle()

    def connect_signals(self):
        self.mpl_connect("key_press_event", self.on_key_press)
        self.mpl_connect("key_release_event", self.on_key_release)
        self.mpl_connect("scroll_event", self.on_scroll)
        self.mpl_connect("motion_notify_event", self.on_mouse_move)
        self.mpl_connect("button_press_event", self.on_mouse_press)
        self.mpl_connect("button_release_event", self.on_mouse_release)

    def plot_spectrum(
        self, x, y, title: str = None, x_label: str = None, y_label: str = None
    ):
        self.axes.clear()
        self.axes.grid(linestyle=":", linewidth=1, alpha=0.5)
        self.axes.plot(x, y)

        if title:
            self.axes.set_title(title)
        else:
            self.axes.set_title("Spectrum")

        if x_label:
            self.axes.set_xlabel(x_label)
        else:
            self.axes.set_xlabel("Wavelength")

        if y_label:
            self.axes.set_ylabel(y_label)
        else:
            self.axes.set_ylabel("Flux")

        logger.info("Plotting spectrum...")
        self.draw_idle()

    def on_key_press(self, event: Event):
        if not isinstance(event, KeyEvent):
            return
        logger.debug(f"Key pressed: {event.key}")

    def on_key_release(self, event: Event):
        if not isinstance(event, KeyEvent):
            return
        logger.debug(f"Key released: {event.key}")

    def on_scroll(self, event: Event):
        if not isinstance(event, MouseEvent):
            return

        if event.inaxes is not self.axes:
            logger.debug("Scroll event outside axes")
            return

        base_scale = 1.1
        scale_factor = 1 / base_scale if event.button == "up" else base_scale

        xdata = event.xdata
        ydata = event.ydata

        x0, x1 = self.axes.get_xlim()
        y0, y1 = self.axes.get_ylim()

        is_shift = event.key == "shift"
        is_ctrl = event.key == "control"

        zoom_x = is_shift or (not is_shift and not is_ctrl)
        zoom_y = is_ctrl or (not is_shift and not is_ctrl)

        if zoom_x:
            new_dx = (x1 - x0) * scale_factor
            rel_x = (xdata - x0) / (x1 - x0)
            self.axes.set_xlim([xdata - new_dx * rel_x, xdata + new_dx * (1 - rel_x)])

        if zoom_y:
            new_dy = (y1 - y0) * scale_factor
            rel_y = (ydata - y0) / (y1 - y0)
            self.axes.set_ylim([ydata - new_dy * rel_y, ydata + new_dy * (1 - rel_y)])

        self.draw_idle()

    def on_mouse_move(self, event: Event):
        if not isinstance(event, MouseEvent):
            return
        if event.button == 3 and self._rmb_event_location is not None:
            dx_px = event.x - self._rmb_event_location[0]
            dy_px = event.y - self._rmb_event_location[1]
            dist = (dx_px**2 + dy_px**2) ** 0.5

            if dist > 5:
                self._is_panning = True

                inv = self.axes.transData.inverted()
                p_start = inv.transform(self._rmb_event_location)
                p_curr = inv.transform((event.x, event.y))

                dx = p_start[0] - p_curr[0]
                dy = p_start[1] - p_curr[1]

                self.axes.set_xlim(
                    self._initial_xlim[0] + dx, self._initial_xlim[1] + dx
                )
                self.axes.set_ylim(
                    self._initial_ylim[0] + dy, self._initial_ylim[1] + dy
                )
                self.draw_idle()

    def on_mouse_press(self, event: Event):
        if not isinstance(event, MouseEvent):
            return
        if event.inaxes is not self.axes:
            return
        logger.debug(f"Mouse press event: {event.button}")

        if event.button == 3:
            self._is_panning = False
            self._rmb_event_location = (event.x, event.y)

            self._initial_xlim = self.axes.get_xlim()
            self._initial_ylim = self.axes.get_ylim()

    def on_mouse_release(self, event: Event):
        if not isinstance(event, MouseEvent):
            return
        self._is_panning = False
        self._rmb_event_location = None
        self._initial_xlim = self.axes.get_xlim()
        self._initial_ylim = self.axes.get_ylim()
        logger.debug(f"Mouse release event: {event.button}")
