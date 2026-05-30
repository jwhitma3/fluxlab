#  SPDX-License-Identifier: MIT
#  Copyright (c) 2026 Joshua C. Whitman
import numpy as np
import pytest

# fmt: off
@pytest.fixture(scope="class")
def spectrum_model_instance():
    from model.spectrum import SpectrumModel
    spectrum_model = SpectrumModel()
    spectrum_model._boundaries = [1.0, 2.0, 3.0, 4.0, 5.0]
    return spectrum_model

class TestGetNearestWavelength:
    def test_set_first_index_when_x_is_left_of_first_index(
        self, spectrum_model_instance
    ):
        assert spectrum_model_instance.get_nearest_wavelength(0.9) == 1.0

    def test_set_first_index_when_x_is_right_of_first_index(
        self, spectrum_model_instance
    ):
        assert spectrum_model_instance.get_nearest_wavelength(1.1) == 1.0

    def test_set_first_index_when_x_equals_first_index(
        self,
        spectrum_model_instance
    ):
        assert spectrum_model_instance.get_nearest_wavelength(1.0) == 1.0

    def test_set_last_index_when_x_is_left_of_last_index(
        self,
        spectrum_model_instance
    ):
        assert spectrum_model_instance.get_nearest_wavelength(4.9) == 5.0

    def test_set_last_index_when_x_is_right_of_last_index(
        self,
        spectrum_model_instance
    ):
        assert spectrum_model_instance.get_nearest_wavelength(5.1) == 5.0

    def test_set_last_index_when_x_equals_last_index(
        self,
        spectrum_model_instance
    ):
        assert spectrum_model_instance.get_nearest_wavelength(5.0) == 5.0

    def test_set_index_when_x_is_between_internal_indices(
        self,
        spectrum_model_instance
    ):
        assert spectrum_model_instance.get_nearest_wavelength(2.1) == 2.0

    def test_raises_runtime_error_when_boundaries_are_not_set(
        self
    ):
        from model.spectrum import SpectrumModel
        uninitialized_model = SpectrumModel()
        with pytest.raises(
                RuntimeError,
                match =
                "Spectrum boundaries not set."
        ):
            uninitialized_model.get_nearest_wavelength(2.1)

    @pytest.mark.parametrize("invalid_value, expected_error, expected_message",[
        (None, ValueError, "x cannot be None"),
        (float("nan"), ValueError, "x cannot be NaN"),
        (np.nan, ValueError, "x cannot be NaN"),
        ("invalid", TypeError, "x must be a number")
    ])
    def test_raises_error_when_x_is_invalid_value(
        self,
        spectrum_model_instance,
            invalid_value,
            expected_error,
            expected_message
    ):
        with pytest.raises(expected_error, match=expected_message):
            spectrum_model_instance.get_nearest_wavelength(invalid_value)

# fmt: on
