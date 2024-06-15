import time

import win32api
import win32con
import win32gui

from Functions import *


class SmartHotkeysTab(QWidget):
    def __init__(self):
        super().__init__()
        # Load Icon
        self.setWindowIcon(QIcon('Icon.jpg'))

        # Set Title and Size
        self.setWindowTitle("Smart Hotkeys")
        self.setFixedSize(300, 80)

        self.X = 0
        self.Y = 0

        # Layout
        self.layout = QGridLayout(self)
        self.setLayout(self.layout)

        # List Widgets
        self.smartHotkeys_listWidget = QListWidget(self)
        self.smartHotkeys_listWidget.setFixedHeight(60)

        # Combo Boxes
        self.runeOption_comboBox = QComboBox(self)
        self.runeOption_comboBox.addItem("With Crosshair")
        self.runeOption_comboBox.addItem("On Target")
        self.runeOption_comboBox.addItem("On Yourself")

        self.hotkeyOption_comboBox = QComboBox(self)
        for i in range(1, 13):
            self.hotkeyOption_comboBox.addItem(f"F{i}")

        # Buttons
        self.coordinates_button = QPushButton("Coordinates", self)
        addSmartHotkey_button = QPushButton("Add", self)

        # Buttons Functions
        addSmartHotkey_button.clicked.connect(self.addSmartHotkey)
        self.coordinates_button.clicked.connect(self.setCoordinates)

        self.layout.addWidget(self.smartHotkeys_listWidget, 0, 0)
        self.layout.addWidget(self.runeOption_comboBox, 0, 1)
        self.layout.addWidget(self.hotkeyOption_comboBox, 0, 2)
        self.layout.addWidget(self.coordinates_button, 1, 1)
        self.layout.addWidget(addSmartHotkey_button, 1, 2)

    def addSmartHotkey(self):
        smartHotkeyData = {"Hotkey": self.hotkeyOption_comboBox.currentText(),
                           "Option": self.runeOption_comboBox.currentText(),
                           "X": self.X, "Y": self.Y}
        hotkey = QListWidgetItem(self.hotkeyOption_comboBox.currentText())
        hotkey.setData(Qt.UserRole, smartHotkeyData)
        self.smartHotkeys_listWidget.addItem(hotkey)
        thread = Thread(target=self.smartHotkeys_Thread)
        thread.daemon = True
        thread.start()

    def setCoordinates(self):
        self.coordinates_button.setStyleSheet("color: red")
        thread = Thread(target=self.setCoordinates_Thread)
        thread.daemon = True
        thread.start()

    def setCoordinates_Thread(self):
        while True:
            self.X, self.Y = win32gui.ScreenToClient(game, win32api.GetCursorPos())
            self.coordinates_button.setText(f'{self.X} {self.Y}')
            if win32api.GetAsyncKeyState(VK_LBUTTON) & 0x8000:
                self.coordinates_button.setStyleSheet("color: black")
                self.coordinates_button.setText('Coordinates')
                return

    def smartHotkeys_Thread(self):
        while True:
            for index in range(self.smartHotkeys_listWidget.count()):
                hotkey = self.smartHotkeys_listWidget.item(index).data(Qt.UserRole)
                if win32api.GetAsyncKeyState(111+int(hotkey['Hotkey'][1:])) & 1:
                    if hotkey['Option'] == 'With Crosshair':
                        rightClick(hotkey['X'], hotkey['Y'])
                    elif hotkey['Option'] == 'On Target':
                        rightClick(hotkey['X'], hotkey['Y'])
                        targetID = c.c_ulonglong.from_buffer(readMemory(attack, 0)).value
                        if targetID:
                            targetY = c.c_int.from_buffer(readMemory(targetID - baseAddress, 0x3C)).value
                            targetX = c.c_int.from_buffer(readMemory(targetID - baseAddress, 0x38)).value
                            x = targetX - c.c_int.from_buffer(readMemory(myX, 0)).value
                            y = targetY - c.c_int.from_buffer(readMemory(myY, 0)).value
                            x = x * 75
                            y = y * 75
                            leftClick(x, y)
                    else:
                        rightClick(hotkey['X'], hotkey['Y'])
            time.sleep(0.05)








