import json

import win32gui

from Functions import *


class LootTab(QWidget):
    def __init__(self, parent=None):
        super(LootTab, self).__init__(parent)
        # Variables
        # Labels
        self.bp_label = QLabel("Set", self)
        self.screen_label = QLabel("Set", self)
        self.tools_label = QLabel("Set", self)

        self.bp_label.setFixedHeight(20)
        self.screen_label.setFixedHeight(20)
        self.tools_label.setFixedHeight(20)

        # List Widgets
        self.settingsProfile_listWidget = QListWidget(self)

        # Line Edits
        self.settings_lineEdit = QLineEdit(self)

        # Layout
        self.layout = QGridLayout(self)
        self.setLayout(self.layout)

        # Init View
        self.setBackpacks()
        self.setEnvironment()
        self.setTools()
        self.saveLoadSettings()

    def setBackpacks(self) -> None:
        groupbox = QGroupBox("Backpacks&&Runes", self)
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Buttons
        goldBP_button = QPushButton("0 Backpack", self)
        itemBP1_button = QPushButton("1 Backpack", self)
        itemBP2_button = QPushButton("2 Backpack", self)
        itemBP3_button = QPushButton("3 Backpack", self)
        hmmBP_button = QPushButton("HMM Backpack", self)
        uhBP_button = QPushButton("UH Backpack", self)
        sdBP_button = QPushButton("SD Backpack", self)
        gfbBP_button = QPushButton("GFB Backpack", self)

        # Buttons Functions
        goldBP_button.clicked.connect(lambda: self.setBP(0))
        itemBP1_button.clicked.connect(lambda: self.setBP(1))
        itemBP2_button.clicked.connect(lambda: self.setBP(2))
        itemBP3_button.clicked.connect(lambda: self.setBP(3))
        uhBP_button.clicked.connect(lambda: self.setBP(4))
        hmmBP_button.clicked.connect(lambda: self.setBP(5))
        sdBP_button.clicked.connect(lambda: self.setBP(6))
        gfbBP_button.clicked.connect(lambda: self.setBP(7))

        # QHBox
        layout = QHBoxLayout(self)
        layout1 = QHBoxLayout(self)
        layout2 = QHBoxLayout(self)
        layout3 = QHBoxLayout(self)
        layout4 = QHBoxLayout(self)
        layout5 = QHBoxLayout(self)
        layout6 = QHBoxLayout(self)
        layout7 = QHBoxLayout(self)
        layout8 = QHBoxLayout(self)

        # Add Widgets
        layout.addWidget(self.bp_label)
        layout1.addWidget(goldBP_button)
        layout2.addWidget(itemBP1_button)
        layout3.addWidget(itemBP2_button)
        layout4.addWidget(itemBP3_button)
        layout5.addWidget(uhBP_button)
        layout6.addWidget(hmmBP_button)
        layout7.addWidget(sdBP_button)
        layout8.addWidget(gfbBP_button)

        # Add Layouts
        groupbox_layout.addLayout(layout)
        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        groupbox_layout.addLayout(layout3)
        groupbox_layout.addLayout(layout4)
        groupbox_layout.addLayout(layout5)
        groupbox_layout.addLayout(layout6)
        groupbox_layout.addLayout(layout7)
        groupbox_layout.addLayout(layout8)
        self.layout.addWidget(groupbox, 0, 1, 3, 1)

    def setTools(self) -> None:
        groupbox = QGroupBox("Tools", self)
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Buttons
        rope_button = QPushButton("Rope", self)
        shovel_button = QPushButton("Shovel", self)
        pick_button = QPushButton("Pick", self)

        # Buttons Functions
        shovel_button.clicked.connect(lambda: self.setBP(8))
        rope_button.clicked.connect(lambda: self.setBP(9))
        pick_button.clicked.connect(lambda: self.setBP(10))

        # QHBox
        layout = QHBoxLayout(self)
        layout1 = QHBoxLayout(self)
        layout2 = QHBoxLayout(self)
        layout3 = QHBoxLayout(self)
        layout4 = QHBoxLayout(self)

        # Add Widgets
        layout.addWidget(self.tools_label)
        layout1.addWidget(shovel_button)
        layout2.addWidget(rope_button)
        layout3.addWidget(pick_button)

        # Add Layouts
        groupbox_layout.addLayout(layout)
        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        groupbox_layout.addLayout(layout3)
        groupbox_layout.addLayout(layout4)
        groupbox.setFixedWidth(150)
        self.layout.addWidget(groupbox, 0, 0)

    def saveLoadSettings(self) -> None:
        groupbox = QGroupBox("Save&&Load", self)
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Buttons
        saveSettings_button = QPushButton("Save", self)
        loadSettings_button = QPushButton("Load", self)

        # Buttons Functions
        saveSettings_button.clicked.connect(self.saveSettings)
        loadSettings_button.clicked.connect(self.loadSettings)

        # List Widgets
        for file in os.listdir("Settings"):
            self.settingsProfile_listWidget.addItem(f"{file.split('.')[0]}")

        # QHBox
        layout1 = QHBoxLayout(self)
        layout2 = QHBoxLayout(self)

        # Add Widgets
        layout1.addWidget(QLabel("Name:", self))
        layout1.addWidget(self.settings_lineEdit)
        layout2.addWidget(saveSettings_button)
        layout2.addWidget(loadSettings_button)

        # Add Layouts
        groupbox_layout.addWidget(self.settingsProfile_listWidget)
        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        groupbox.setFixedWidth(150)
        self.layout.addWidget(groupbox, 2, 0)

    def setEnvironment(self) -> None:
        groupbox = QGroupBox("Environment", self)
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Buttons
        setMainScreen_button = QPushButton("Set Screen", self)
        setLootScreen_button = QPushButton("Set Loot", self)

        # Buttons Functions
        setMainScreen_button.clicked.connect(lambda: self.setScreen(0))
        setLootScreen_button.clicked.connect(lambda: self.setScreen(1))

        # QHBox
        layout = QHBoxLayout(self)
        layout1 = QHBoxLayout(self)
        layout2 = QHBoxLayout(self)

        # Add Widgets
        layout.addWidget(self.screen_label)
        layout1.addWidget(setMainScreen_button)
        layout2.addWidget(setLootScreen_button)

        # Add Layouts
        groupbox_layout.addLayout(layout)
        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        groupbox.setFixedWidth(150)
        self.layout.addWidget(groupbox, 1, 0)

    # Functions
    def setScreen(self, id):
        thread = Thread(target=self.setScreen_Thread, args=(id,))
        thread.daemon = True
        thread.start()

    def setBP(self, id):
        thread = Thread(target=self.setBP_Thread, args=(id,))
        thread.daemon = True
        thread.start()

    # Threads
    def setScreen_Thread(self, id):
        self.screen_label.setStyleSheet("color: red")
        while True:
            screenX[id], screenY[id] = win32api.GetCursorPos()
            self.screen_label.setText(f"X = {screenX[id]} | Y = {screenY[id]}")
            time.sleep(0.05)
            if win32api.GetAsyncKeyState(VK_LBUTTON) & 0x8000:
                self.screen_label.setStyleSheet("color: blue")
                break
        time.sleep(0.1)
        while True:
            screenWidth[id], screenHeight[id] = win32api.GetCursorPos()
            self.screen_label.setText(f"X = {screenWidth[id]} | Y = {screenHeight[id]}")
            time.sleep(0.05)
            if win32api.GetAsyncKeyState(VK_LBUTTON) & 0x8000:
                self.screen_label.setStyleSheet("color: black")
                self.screen_label.setText("Set")
                screenX[id], screenY[id] = win32gui.ScreenToClient(game, (screenX[id], screenY[id]))
                screenWidth[id], screenHeight[id] = win32gui.ScreenToClient(game, (screenWidth[id], screenHeight[id]))
                return

    def setBP_Thread(self, id):
        if id < 8:
            self.bp_label.setStyleSheet("color: red")
        else:
            self.tools_label.setStyleSheet("color: red")
        while True:
            bpX[id], bpY[id] = win32api.GetCursorPos()
            if id < 8:
                self.bp_label.setText(f"X = {bpX[id]} | Y = {bpY[id]}")
            else:
                self.tools_label.setText(f"X = {bpX[id]} | Y = {bpY[id]}")
            time.sleep(0.05)
            if win32api.GetAsyncKeyState(VK_LBUTTON) & 0x8000:
                bpX[id], bpY[id] = win32gui.ScreenToClient(game, (bpX[id], bpY[id]))
                if id < 8:
                    self.bp_label.setText("Set")
                    self.bp_label.setStyleSheet("color: black")
                else:
                    self.tools_label.setText("Set")
                    self.tools_label.setStyleSheet("color: black")
                return

    def saveSettings(self) -> None:
        settingsName = self.settings_lineEdit.text()
        for index in range(self.settingsProfile_listWidget.count()):
            if settingsName.upper() == self.settingsProfile_listWidget.item(index).text().upper():
                return
        if settingsName:
            screen_data = {
                "screenX": screenX,
                "screenY": screenY,
                "screenWidth": screenWidth,
                "screenHeight": screenHeight,
                "bpX": bpX,
                "bpY": bpY
            }
            settingsData = {
                "screen_data": screen_data
            }
            with open(f"Settings/{settingsName}.json", "w") as f:
                json.dump(settingsData, f, indent=4)
            self.settingsProfile_listWidget.addItem(settingsName)
            self.settings_lineEdit.clear()

    def loadSettings(self) -> None:
        settingsName = self.settingsProfile_listWidget.currentItem().text()
        if settingsName:
            with open(f"Settings/{settingsName}.json", "r") as f:
                settingsList = json.load(f)
            settingsData = settingsList.get("screen_data", {})
            screenX[0], screenX[1] = settingsData.get("screenX", [0] * 2)
            screenY[0], screenY[1] = settingsData.get("screenY", [0] * 2)
            screenWidth[0], screenWidth[1] = settingsData.get("screenWidth", [0] * 2)
            screenHeight[0], screenHeight[1] = settingsData.get("screenHeight", [0] * 2)
            bpDataX = settingsData.get("bpX", [0] * 12)
            bpDataY = settingsData.get("bpY", [0] * 12)
            for i in range(len(bpX)):
                bpX[i] = bpDataX[i]
                bpY[i] = bpDataY[i]
        self.bp_label.setStyleSheet("color: green")
        self.screen_label.setStyleSheet("color: green")
        self.tools_label.setStyleSheet("color: green")
        self.screen_label.setText("Loaded")
        self.bp_label.setText("Loaded")
        self.tools_label.setText("Loaded")

