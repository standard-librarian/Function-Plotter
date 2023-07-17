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
    PLOT = 1
    SCATTER = 2
    BAR = 3
    STEM = 4
    STEP = 5
