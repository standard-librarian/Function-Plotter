import pytest
from app.plotter import Plotter


@pytest.fixture
def plotter(qtbot):
    plt = Plotter()
    qtbot.addWidget(plt)
    return plt
