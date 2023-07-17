from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QWidget, QLineEdit, QHBoxLayout, QPushButton, QSlider
)
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from app.utils.plot_option import PlotOption
from app.utils.validation import *
from app.utils.constants import *


class Plotter(QMainWindow):
    def __init__(self):
        self.draw_option = None
        self.function_processor = None
        super().__init__()
        self.create_widgets()
        self.create_layouts()
        self.create_ui()
        self.connect_signals()
        self.show()

    def create_widgets(self):
        """Make objects of the widgets that's needed for the app"""
        self.function_label = QLabel("\tEnter a f(x):")
        self.function_input = QLineEdit()

        self.xmin_label = QLabel("Range of x between:")
        self.xmin_input = QLineEdit()
        self.xmax_label = QLabel("&")
        self.xmax_input = QLineEdit()

        self.plot_button = QPushButton("Plot")
        self.zoom_in_button = QPushButton("Zoom +")
        self.zoom_out_button = QPushButton("Zoom -")

        self.samples_label = QLabel("Number of X samples:")
        self.samples_slider = QSlider(Qt.Orientation.Horizontal)
        self.samples_slider.setMinimum(MIN_SLIDER_VALUE)
        self.samples_slider.setMaximum(MAX_SLIDER_VALUE)
        self.samples_slider.setSingleStep(SLIDER_STEP)
        self.samples_slider.setValue(SLIDER_STARTING_VALUE)

        self.scatter_button = QPushButton("Scatter")
        self.bar_button = QPushButton("Bar")
        self.stem_button = QPushButton("Stem")
        self.step_button = QPushButton("Step")

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

    def create_layouts(self):
        """Organize the main layout into sub layouts each has its widgets"""
        self.layout = QVBoxLayout()

        self.function_layout = QHBoxLayout()
        self.function_layout.addWidget(self.function_label)
        self.function_layout.addWidget(self.function_input)

        self.range_x_layout = QHBoxLayout()
        self.range_x_layout.addWidget(self.xmin_label)
        self.range_x_layout.addWidget(self.xmin_input)
        self.range_x_layout.addWidget(self.xmax_label)
        self.range_x_layout.addWidget(self.xmax_input)

        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.addWidget(self.plot_button)
        self.buttons_layout.addWidget(self.zoom_in_button)
        self.buttons_layout.addWidget(self.zoom_out_button)

        self.samples_layout = QHBoxLayout()
        self.samples_layout.addWidget(self.samples_label)
        self.samples_layout.addWidget(self.samples_slider)

        self.plotting_options_layout = QHBoxLayout()
        self.plotting_options_layout.addWidget(self.scatter_button)
        self.plotting_options_layout.addWidget(self.bar_button)
        self.plotting_options_layout.addWidget(self.stem_button)
        self.plotting_options_layout.addWidget(self.step_button)

    def create_ui(self):
        """Construct the actual ui from the layouts"""
        widget = QWidget()
        self.layout.addLayout(self.function_layout)
        self.layout.addLayout(self.range_x_layout)
        self.layout.addLayout(self.buttons_layout)
        self.layout.addLayout(self.samples_layout)
        self.layout.addLayout(self.plotting_options_layout)
        self.layout.addWidget(self.canvas)
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)
        self.setGeometry(WINDOW_X_START, WINDOW_Y_START, WINDOW_WIDTH, WINDOW_HEIGHT)

    def connect_signals(self):
        """Connect signals to their slots"""
        self.plot_button.clicked.connect(lambda: self.draw(PlotOption.PLOT))
        self.scatter_button.clicked.connect(lambda: self.draw(PlotOption.SCATTER))
        self.bar_button.clicked.connect(lambda: self.draw(PlotOption.BAR))
        self.stem_button.clicked.connect(lambda: self.draw(PlotOption.STEM))
        self.step_button.clicked.connect(lambda: self.draw(PlotOption.STEP))
        self.samples_slider.sliderReleased.connect(lambda: self.draw(self.draw_option))
        self.zoom_in_button.clicked.connect(self.zoom_in)
        self.zoom_out_button.clicked.connect(self.zoom_out)

    def prepare_to_draw(self):
        """When the draw() called from the UI, perpare_to_draw creates the needed vars"""
        xmin = self.xmin_input.text()
        xmax = self.xmax_input.text()
        function_string = self.function_input.text()
        samples = self.samples_slider.value()

        x_range = validate_range(self, xmin, xmax)
        validate_2d_function(self, function_string)
        x_data, y_data = parse_2d_function(function_string, x_range, samples)
        self.figure.clear()
        self.ax = self.figure.add_subplot(PLOT_PLACE_FROM_CANVAS)
        return x_data, y_data

    def draw(self, draw_option):
        """Choose the Option of drawing and draws on the canvas"""
        x_data, y_data = self.prepare_to_draw()
        if draw_option == PlotOption.PLOT:
            self.ax.plot(x_data, y_data)
        elif draw_option == PlotOption.SCATTER:
            self.ax.scatter(x_data, y_data)
        elif draw_option == PlotOption.BAR:
            self.ax.bar(x_data, y_data)
        elif draw_option == PlotOption.STEM:
            self.ax.stem(x_data, y_data)
        elif draw_option == PlotOption.STEP:
            self.ax.step(x_data, y_data)
        self.draw_option = draw_option
        self.canvas.draw()

    def zoom(self, percent):
        """General Zoom function to be used by both zoom in and zoom out"""
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        self.ax.set_xlim(xlim[0] * percent, xlim[1] * percent)
        self.ax.set_ylim(ylim[0] * percent, ylim[1] * percent)
        self.canvas.draw()

    def zoom_in(self):
        """When the zoom in button pressed, this slot activates"""
        self.zoom(ZOOM_IN)

    def zoom_out(self):
        """When the zoom out button pressed, this slot activates"""
        self.zoom(ZOOM_OUT)
