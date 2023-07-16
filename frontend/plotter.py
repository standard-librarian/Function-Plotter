from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QWidget, QLineEdit, QHBoxLayout, QPushButton, QSlider
)
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from backend.function_processor import FunctionProcessor

from utils.plot_option import PlotOption


class Plotter(QMainWindow):
    def __init__(self):
        self.function_processor = None
        super().__init__()
        self.create_variables()
        self.create_widgets()
        self.create_layouts()
        self.create_ui()
        self.connect_signals()
        self.setup()

    def create_variables(self):
        self.is_3d_checkbox = False
        self.draw_option = None
        self.last_plot_option = None

    def create_widgets(self):
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
        self.samples_slider.setMinimum(1)
        self.samples_slider.setMaximum(500)
        self.samples_slider.setSingleStep(1)
        self.samples_slider.setValue(100)

        self.scatter_button = QPushButton("Scatter")
        self.bar_button = QPushButton("Bar")
        self.stem_button = QPushButton("Stem")
        self.step_button = QPushButton("Step")

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

    def create_layouts(self):
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
        self.layout.addLayout(self.function_layout)
        self.layout.addLayout(self.range_x_layout)
        self.layout.addLayout(self.buttons_layout)
        self.layout.addLayout(self.samples_layout)
        self.layout.addLayout(self.plotting_options_layout)
        self.layout.addWidget(self.canvas)

        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)
        self.setGeometry(500, 50, 800, 700)

    def connect_signals(self):
        self.plot_button.clicked.connect(self.select_plot_and_draw)
        self.scatter_button.clicked.connect(self.select_scatter_and_draw)
        self.bar_button.clicked.connect(self.select_bar_and_draw)
        self.stem_button.clicked.connect(self.select_stem_and_draw)
        self.step_button.clicked.connect(self.select_step_and_draw)
        self.zoom_in_button.clicked.connect(self.zoom_in)
        self.zoom_out_button.clicked.connect(self.zoom_out)
        self.samples_slider.sliderReleased.connect(self.draw)

    def select_plot_and_draw(self):
        self.draw_option = PlotOption.PLOT
        self.draw()

    def select_scatter_and_draw(self):
        self.draw_option = PlotOption.SCATTER
        self.draw()

    def select_bar_and_draw(self):
        self.draw_option = PlotOption.BAR
        self.draw()

    def select_stem_and_draw(self):
        self.draw_option = PlotOption.STEM
        self.draw()

    def select_step_and_draw(self):
        self.draw_option = PlotOption.STEP
        self.draw()

    def draw(self):
        x_data, y_data = self.prepare_to_draw()
        if self.draw_option == PlotOption.PLOT:
            self.plot(x_data, y_data)
        elif self.draw_option == PlotOption.SCATTER:
            self.scatter(x_data, y_data)
        elif self.draw_option == PlotOption.BAR:
            self.bar(x_data, y_data)
        elif self.draw_option == PlotOption.STEM:
            self.stem(x_data, y_data)
        elif self.draw_option == PlotOption.STEP:
            self.step(x_data, y_data)

    def prepare_to_draw(self):
        self.function_processor = FunctionProcessor(self,
                                                    self.function_input.text(),
                                                    self.xmin_input.text(),
                                                    self.xmax_input.text(),
                                                    x_samples=self.samples_slider.value())
        self.function_processor.validate_2d_function()
        x_data, y_data = self.function_processor.parse_2d_function()
        self.figure.clear()
        self.ax = self.figure.add_subplot(111)
        return x_data, y_data

    def plot(self, x_data, y_data):
        self.ax.plot(x_data, y_data)
        self.canvas.draw()

    def scatter(self, x_data, y_data):
        self.ax.scatter(x_data, y_data)
        self.canvas.draw()

    def bar(self, x_data, y_data):
        self.ax.bar(x_data, y_data)
        self.canvas.draw()

    def stem(self, x_data, y_data):
        self.ax.stem(x_data, y_data)
        self.canvas.draw()
    def step(self, x_data, y_data):
        self.ax.step(x_data, y_data)
        self.canvas.draw()

    def setup(self):
        self.show()

    def zoom_in(self):
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        self.ax.set_xlim(xlim[0] * 0.9, xlim[1] * 0.9)
        self.ax.set_ylim(ylim[0] * 0.9, ylim[1] * 0.9)
        self.canvas.draw()

    def zoom_out(self):
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        self.ax.set_xlim(xlim[0] * 1.1, xlim[1] * 1.1)
        self.ax.set_ylim(ylim[0] * 1.1, ylim[1] * 1.1)
        self.canvas.draw()

    def redraw_with_samples(self):
        self.function_processor.samples = self.samples_slider.value()
        if self.last_plot_option == PlotOption.PLOT:
            self.plot()
        elif self.last_plot_option == PlotOption.SCATTER:
            pass
        elif self.last_plot_option == PlotOption.BAR:
            pass
        elif self.last_plot_option == PlotOption.STEM:
            pass
        elif self.last_plot_option == PlotOption.STEP:
            pass
