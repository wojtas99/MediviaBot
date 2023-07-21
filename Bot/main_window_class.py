from PyQt5.QtWidgets import *


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.stacked_widget = QStackedWidget(self)
        #  Title and Size
        self.setWindowTitle("KrawczorBot")
        self.resize(500, 500)
        self.textfield = QLineEdit(self)
        self.textfield.setGeometry(300, 300, 100, 30)
        self.textfield.show()
