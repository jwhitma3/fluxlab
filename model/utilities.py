#  SPDX-License-Identifier: MIT
#  Copyright (c) 2026 Joshua C. Whitman

import logging
import pathlib
from typing import Union

from specutils.spectra import Spectrum

logger = logging.getLogger(__name__)


def import_specturm(file_path: Union[str, pathlib.Path] = None):
    if not file_path:
        raise ValueError("No file path provided")

    file_path_obj = pathlib.Path(file_path)

    if not file_path_obj.is_file():
        raise FileNotFoundError(
            f"'{file_path}' is not a valid file or does not exist..."
        )

    spec = Spectrum.read(file_path_obj.as_posix())

    return spec
