import pytest
from app.plotter import Plotter
from app.utils.plot_option import PlotOption


@pytest.fixture
def plotter(qtbot):
    plt = Plotter()
    qtbot.addWidget(plt)
    return plt


@pytest.fixture(params=[PlotOption.PLOT, PlotOption.SCATTER, PlotOption.BAR, PlotOption.STEM, PlotOption.STEP])
def draw_option(request):
    """Fixture to provide different draw_option values for testing."""
    return request.param
