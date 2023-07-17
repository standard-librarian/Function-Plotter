import re
import sympy
from PySide6.QtWidgets import QMessageBox


def validate_range(plotter, xmin, xmax):
    """Creates a x_range after validating the range of input"""
    try:
        x_range = float(xmin), float(xmax)

    except ValueError:
        QMessageBox.warning(plotter, "Invalid input", "Enter a valid range of x.")
        return
    return x_range


def validate_2d_function(plotter, function_string):
    """Creates a pop up if the input function is not valid"""
    if not re.match(r"^[0-9x+\-*/^(). ]+$", function_string):
        QMessageBox.warning(plotter, "Invalid input", "Enter a valid function of x.")


def parse_2d_function(function_string, x_range, x_samples):
    """Parse the function string and get the data ready for plotting"""
    function_string = function_string.replace("^", "**")
    x = sympy.Symbol('x')
    function = sympy.parse_expr(function_string)
    x_data = [x_range[0] + (x_range[1] - x_range[0]) * i / x_samples for i in range(x_samples + 1)]
    y_data = [function.subs(x, xi) for xi in x_data]

    return x_data, y_data
