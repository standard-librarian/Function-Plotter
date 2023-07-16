from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QWidget, QLineEdit, QHBoxLayout, QPushButton, QSlider, QCheckBox
)
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class Plotter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.create_variables()
        self.create_widgets()
        self.create_layouts()
        self.create_ui()
        self.connect_signals()
        self.setup()

    def create_variables(self):
        self.is_3d_checkbox = False

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
        self.zoom_in_button.clicked.connect(self.zoom_in)
        self.zoom_out_button.clicked.connect(self.zoom_out)

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