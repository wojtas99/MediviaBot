from Functions import *


class SmartHotkeysTab(QWidget):
    def __init__(self):
        super().__init__()
        # Load Icon
        self.setWindowIcon(QIcon('Icon.jpg'))

        # Set Title and Size
        self.setWindowTitle("Smart Hotkeys")
        self.setFixedSize(300, 80)

        # Layout
        self.layout = QGridLayout(self)
        self.setLayout(self.layout)

        # List Widgets
        self.smartHotkeys_listWidget = QListWidget(self)
        self.smartHotkeys_listWidget.setFixedHeight(60)

        self.runeOption_comboBox = QComboBox(self)
        self.runeOption_comboBox.addItem("With Crosshair")
        self.runeOption_comboBox.addItem("On Target")
        self.runeOption_comboBox.addItem("On Yourself")

        self.hotkeyOption_comboBox = QComboBox()
        for i in range(1, 13):
            self.hotkeyOption_comboBox.addItem(f"F{i}")

        coordinates_button = QPushButton("Coordinates", self)

        addSmartHotkey_button = QPushButton("Add", self)
        addSmartHotkey_button.clicked.connect(self.addSmartHotkey)

        self.layout.addWidget(self.smartHotkeys_listWidget, 0, 0)
        self.layout.addWidget(self.runeOption_comboBox, 0, 1)
        self.layout.addWidget(self.hotkeyOption_comboBox, 0, 2)
        self.layout.addWidget(coordinates_button, 1, 1)
        self.layout.addWidget(addSmartHotkey_button, 1, 2)

    def addSmartHotkey(self):
        smartHotkeyData = {'Hotkey': self.hotkeyOption_comboBox.currentText(),
                           'Option': self.runeOption_comboBox.currentText(),
                           'X': 0, 'Y': 0}





