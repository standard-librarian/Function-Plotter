from PySide6.QtWidgets import QApplication

from frontend.plotter import Plotter


def main() -> None:
    app = QApplication([])
    plt = Plotter()
    plt.setWindowTitle("Function Plotter by Medhat Mohammed")
    app.exec()


if __name__ == "__main__":
    main()
