import pytest
from PySide6.QtWidgets import QMessageBox
from app.plotter import Plotter
from app.utils.validation import validate_range, validate_2d_function, parse_2d_function


@pytest.mark.validation
def test_validate_range_valid_input(mocker):
    """Test validate_range with valid input."""
    plotter = mocker.Mock(spec=Plotter)
    mocker.patch.object(QMessageBox, 'warning')

    xmin = '0'
    xmax = '10'

    result = validate_range(plotter, xmin, xmax)

    assert result == (0.0, 10.0)
    QMessageBox.warning.assert_not_called()


@pytest.mark.validation
def test_validate_range_invalid_input(mocker):
    """Test validate_range with invalid input."""
    plotter = mocker.Mock(spec=Plotter)
    mocker.patch.object(QMessageBox, 'warning')

    xmin = 'a'
    xmax = '10'

    result = validate_range(plotter, xmin, xmax)

    assert result is None
    QMessageBox.warning.assert_called_once_with(
        plotter, "Invalid input", "Enter a valid range of x."
    )


@pytest.mark.validation
def test_validate_2d_function_valid_input(mocker):
    """Test validate_2d_function with valid input."""
    plotter = mocker.Mock(spec=Plotter)
    mocker.patch.object(QMessageBox, 'warning')

    function_string = "2*x + 3"

    validate_2d_function(plotter, function_string)

    QMessageBox.warning.assert_not_called()


@pytest.mark.validation
def test_validate_2d_function_invalid_input(mocker):
    """Test validate_2d_function with invalid input."""
    plotter = mocker.Mock(spec=Plotter)
    mocker.patch.object(QMessageBox, 'warning')

    function_string = "2*x + @"

    validate_2d_function(plotter, function_string)

    QMessageBox.warning.assert_called_once_with(
        plotter, "Invalid input", "Enter a valid function of x."
    )


@pytest.mark.auto
def test_parse_2d_function():
    """Test parse_2d_function."""
    function_string = "2*x + 3"
    x_range = (0, 10)
    x_samples = 5

    x_data, y_data = parse_2d_function(function_string, x_range, x_samples)

    expected_x_data = [0.0, 2.0, 4.0, 6.0, 8.0, 10.0]
    expected_y_data = [3.0, 7.0, 11.0, 15.0, 19.0, 23.0]

    assert x_data == expected_x_data
    assert y_data == expected_y_data
