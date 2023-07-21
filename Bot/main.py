from PyQt5.QtWidgets import *
from main_window_class import MainWindow


def main():
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec()


if __name__ == '__main__':
    main()






