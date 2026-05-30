#  SPDX-License-Identifier: MIT
#  Copyright (c) 2026 Joshua C. Whitman

import sys

from PySide6.QtWidgets import QApplication

from controller.controller import AppController
from model.spectrum import SpectrumModel
from view.window import AppWindow


def main():
    app = QApplication(sys.argv)
    model = SpectrumModel()
    window = AppWindow()
    controller = AppController(model=model, window=window)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
