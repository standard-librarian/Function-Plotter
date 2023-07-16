from PySide6.QtWidgets import QApplication

from frontend.plotter import Plotter


def main() -> None:
    app = QApplication([])
    plt = Plotter()
    app.exec()


if __name__ == "__main__":
    main()
