import pytest
import unittest.mock as mock

from PySide6.QtWidgets import QHBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from app.plotter import Plotter
from app.utils.constants import ZOOM_IN, ZOOM_OUT
from app.utils.plot_option import PlotOption


@pytest.mark.plotter
def test_create_widgets(plotter: Plotter):
    """
    Test function to verify the creation of widgets in the `create_widgets` method of the `Plotter` class.

    Args:
        plotter (Plotter): An instance of the Plotter class.

    Raises:
        AssertionError: If any of the required widgets are not created.
    """
    assert plotter.function_label is not None, "Function label is not created"
    assert plotter.function_input is not None, "Function input is not created"
    assert plotter.xmin_label is not None, "xmin label is not created"
    assert plotter.xmin_input is not None, "xmin input is not created"
    assert plotter.xmax_label is not None, "xmax label is not created"
    assert plotter.xmax_input is not None, "xmax input is not created"
    assert plotter.plot_button is not None, "Plot button is not created"
    assert plotter.zoom_in_button is not None, "Zoom in button is not created"
    assert plotter.zoom_out_button is not None, "Zoom out button is not created"
    assert plotter.samples_label is not None, "Samples label is not created"
    assert plotter.samples_slider is not None, "Samples slider is not created"
    assert plotter.scatter_button is not None, "Scatter button is not created"
    assert plotter.bar_button is not None, "Bar button is not created"
    assert plotter.stem_button is not None, "Stem button is not created"
    assert plotter.step_button is not None, "Step button is not created"
    assert plotter.figure is not None, "Figure is not created"
    assert plotter.canvas is not None, "Canvas is not created"


@pytest.mark.plotter
def test_create_layouts(plotter: Plotter):
    """
    Test the creation of the layout.

    This function tests the creation of the layouts in the Plotter class.
    It checks if the main layout and its sub-layouts are created properly.

    Args:
        plotter (Plotter): The Plotter instance.

    """
    assert plotter.layout is not None, "Main layout is None"
    assert len(plotter.layout.findChildren(QHBoxLayout)) == 5, "Expected 5 QHBoxLayouts"


@pytest.mark.plotter
def test_connect_signals(plotter: Plotter):
    """
    Test the connection of the signals.

    This function tests if the signals emitted by the widgets in the Plotter class
    are connected as expected.

    Args:
        plotter (Plotter): The Plotter instance.

    """
    assert plotter.plot_button.clicked is not None, "plot_button signal is not connected"
    assert plotter.scatter_button.clicked is not None, "scatter_button signal is not connected"
    assert plotter.bar_button.clicked is not None, "bar_button signal is not connected"
    assert plotter.stem_button.clicked is not None, "stem_button signal is not connected"
    assert plotter.step_button.clicked is not None, "step_button signal is not connected"
    assert plotter.samples_slider.sliderReleased is not None, "samples_slider signal is not connected"
    assert plotter.zoom_in_button.clicked is not None, "zoom_in_button signal is not connected"
    assert plotter.zoom_out_button.clicked is not None, "zoom_out_button signal is not connected"


@pytest.mark.plotter
def test_prepare_to_draw(plotter: Plotter):
    """
    Test the prepare_to_draw() method.

    This function tests if the prepare_to_draw() method in the Plotter class correctly extracts the necessary
    variables from the UI widgets, performs validation checks, and returns the expected x_data and y_data.

    Args:
        plotter (Plotter): The Plotter instance.

    """
    # Set up test inputs
    plotter.xmin_input.setText("0")
    plotter.xmax_input.setText("10")
    plotter.function_input.setText("x**2")
    plotter.samples_slider.setValue(100)

    # Call the prepare_to_draw() method
    x_data, y_data = plotter.prepare_to_draw()

    # Perform assertions
    assert isinstance(x_data, list), "x_data is not a list"
    assert isinstance(y_data, list), "y_data is not a list"
    assert len(x_data) == 101, "Unexpected length of x_data"
    assert len(y_data) == 101, "Unexpected length of y_data"
    assert x_data[0] == 0, "Unexpected start value of x_data"
    assert x_data[-1] == 10, "Unexpected end value of x_data"
    assert y_data[0] == 0, "Unexpected start value of y_data"
    assert y_data[-1] == 100, "Unexpected end value of y_data"


@pytest.mark.plotter
def test_draw(plotter: Plotter):
    """
    Test the draw() method.

    This function tests if the draw() method in the Plotter class correctly chooses the drawing option and
    plots the data on the canvas.

    Args:
        plotter (Plotter): The Plotter instance.
        mocker: The mocker fixture from pytest.

    """
    test_draw_option(plotter, PlotOption.PLOT)
    test_draw_option(plotter, PlotOption.SCATTER)
    test_draw_option(plotter, PlotOption.BAR)
    test_draw_option(plotter, PlotOption.STEM)
    test_draw_option(plotter, PlotOption.STEP)


@pytest.mark.plotter
def test_draw_option(plotter: Plotter, draw_option: PlotOption):
    """
    Test the draw() method with a specific draw_option.

    This function calls the draw() method with the specified draw_option and asserts that the draw_option
    value is updated correctly.

    Args:
        plotter (Plotter): The Plotter instance.
        draw_option (PlotOption): The draw_option value to test.

    """
    with mock.patch.object(Plotter, 'prepare_to_draw', return_value=([1, 2, 3], [4, 5, 6])):
        plotter.draw(draw_option)
        assert plotter.draw_option == draw_option, f"Unexpected draw_option value after {draw_option}"


@pytest.mark.plotter
def test_zoom(plotter: Plotter, mocker):
    """
    Test the zoom() method.

    This function tests if the zoom() method in the Plotter class correctly adjusts the plot's x and y limits
    based on the given zoom factor and redraws the canvas.

    Args:
        plotter (Plotter): The Plotter instance.
        mocker: The mocker fixture from pytest.

    """
    # Mock the FigureCanvas and Figure objects
    mocker.patch.object(FigureCanvas, '__init__', return_value=None)
    mocker.patch.object(FigureCanvas, 'draw')

    # Mock the AxesSubplot object
    ax_mock = mocker.MagicMock()
    ax_mock.get_xlim.return_value = (0, 10)
    ax_mock.get_ylim.return_value = (0, 10)
    plotter.figure.add_subplot = mocker.MagicMock(return_value=ax_mock)

    # Test zoom in
    plotter.zoom(ZOOM_IN)
    ax_mock.set_xlim.assert_called_with(0, 8)
    ax_mock.set_ylim.assert_called_with(0, 8)
    plotter.canvas.draw.assert_called_once()

    # Test zoom out
    ax_mock.get_xlim.return_value = (0, 10)
    ax_mock.get_ylim.return_value = (0, 10)
    plotter.zoom(ZOOM_OUT)
    ax_mock.set_xlim.assert_called_with(0, 12.5)
    ax_mock.set_ylim.assert_called_with(0, 12.5)
    assert plotter.canvas.draw.call_count == 2


@pytest.mark.plotter
def test_zoom_in(plotter: Plotter, mocker):
    """
    Test the zoom_in() slot.

    This function tests if the zoom_in() slot in the Plotter class correctly calls the zoom() method with the
    ZOOM_IN factor.

    Args:
        plotter (Plotter): The Plotter instance.
        mocker: The mocker fixture from pytest.

    """
    mocker.patch.object(plotter, 'zoom')

    # Call the slot
    plotter.zoom_in()

    # Verify that the zoom method was called with ZOOM_IN factor
    plotter.zoom.assert_called_with(ZOOM_IN)


@pytest.mark.plotter
def test_zoom_out(plotter: Plotter, mocker):
    """
    Test the zoom_out() slot.

    This function tests if the zoom_out() slot in the Plotter class correctly calls the zoom() method with the
    ZOOM_OUT factor.

    Args:
        plotter (Plotter): The Plotter instance.
        mocker: The mocker fixture from pytest.

    """
    mocker.patch.object(plotter, 'zoom')

    # Call the slot
    plotter.zoom_out()

    # Verify that the zoom method was called with ZOOM_OUT factor
    plotter.zoom.assert_called_with(ZOOM_OUT)
