from __future__ import annotations

import re
from typing import Tuple, List

import sympy
from PySide6.QtWidgets import QMessageBox


def validate_range(plotter, xmin: str, xmax: str) -> None | Tuple[float, float]:
    """
    Validate the range of x and create a valid x_range.

    This function takes the minimum and maximum values of x as input and validates them.
    If the values are valid, it returns the x_range as a tuple (xmin, xmax).
    If the values are not valid, it displays a warning message using a QMessageBox.

    Args:
        plotter: The Plotter instance.
        xmin (str): The minimum value of x.
        xmax (str): The maximum value of x.

    Returns:
        tuple: The x_range as a tuple (xmin, xmax) if the input is valid, None otherwise.

    """
    try:
        x_range = float(xmin), float(xmax)

    except ValueError:
        QMessageBox.warning(plotter, "Invalid input", "Enter a valid range of x.")
        return None
    return x_range


def validate_2d_function(plotter, function_string: str) -> None:
    """
    Validate the input function string for 2D plotting.

    This function checks if the input function string is valid for 2D plotting.
    It uses regular expressions to match the allowed characters and format.
    If the function string is not valid, it displays a warning message using a QMessageBox.

    Args:
        plotter: The Plotter instance.
        function_string (str): The input function string.

    """
    if not re.match(r"^[0-9x+\-*/^(). ]+$", function_string):
        QMessageBox.warning(plotter, "Invalid input", "Enter a valid function of x.")


def parse_2d_function(function_string: str, x_range: Tuple[float, float], x_samples: int) \
        -> Tuple[List[float], List[float]]:
    """
    Parse the function string and prepare data for 2D plotting.

    This function parses the input function string using sympy.
    It replaces '^' with '**' to represent exponentiation.
    It creates a sympy expression for the function and evaluates it at various x values.
    The x data is generated based on the x_range and x_samples.
    The corresponding y data is computed by substituting the x values into the function.
    The x data and y data are returned as lists.

    Args:
        function_string (str): The input function string.
        x_range (tuple): The range of x as a tuple (xmin, xmax).
        x_samples (int): The number of x samples.

    Returns:
        tuple: The x data and y data as lists.

    """
    function_string = function_string.replace("^", "**")
    x = sympy.Symbol('x')
    function = sympy.parse_expr(function_string)
    x_data = [x_range[0] + (x_range[1] - x_range[0]) * i / x_samples for i in range(x_samples + 1)]
    y_data = [function.subs(x, xi) for xi in x_data]

    return x_data, y_data
