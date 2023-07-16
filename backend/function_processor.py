import re
import sympy as sympy
from PySide6.QtWidgets import QMessageBox


class FunctionProcessor():
    def __init__(self, plotter, function_string, xmin, xmax, x_samples):
        self.plotter = plotter
        self.function_string = function_string
        self.x_samples = x_samples
        try:
            self.x_range = float(xmin), float(xmax)
        except ValueError:
            QMessageBox.warning(self.plotter, "Invalid input", "Enter a valid range of x.")
            return

    def validate_2d_function(self):
        if not re.match(r"^[0-9x+\-*/^(). ]+$", self.function_string):
            error_message = "Enter a valid function of x."
            QMessageBox.warning(self.plotter, "Invalid input", error_message)
            return

    def parse_2d_function(self):
        self.function_string = self.function_string.replace("^", "**")
        x = sympy.Symbol('x')
        function = sympy.parse_expr(self.function_string)
        x_data = [self.x_range[0] + (self.x_range[1] - self.x_range[0]) * i / self.x_samples for i in
                  range(self.x_samples + 1)]
        y_data = [function.subs(x, xi) for xi in x_data]

        return x_data, y_data
