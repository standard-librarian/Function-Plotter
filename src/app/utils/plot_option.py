import enum
from enum import Enum


class PlotOption(Enum):
    """
        Enum representing different plot options.

        This enumeration defines the available plot options for the Plotter class.
        Each option is associated with a unique integer value.

        Attributes:
            PLOT (int): Option for plotting a line plot.
            SCATTER (int): Option for plotting a scatter plot.
            BAR (int): Option for plotting a bar plot.
            STEM (int): Option for plotting a stem plot.
            STEP (int): Option for plotting a step plot.

        """
    PLOT = enum.auto()
    SCATTER = enum.auto()
    BAR = enum.auto()
    STEM = enum.auto()
    STEP = enum.auto()
