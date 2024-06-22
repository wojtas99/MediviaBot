import json
from Functions import *


class SettingsTab(QWidget):
    def __init__(self, parent=None):
        super(SettingsTab, self).__init__(parent)
        # Load Icon
        self.setWindowIcon(QIcon('Icon.jpg'))

        # Set Title and Size
        self.setWindowTitle("Settings")
        self.setFixedSize(350, 300)

        # Variables
        # Labels
        self.tools_label = QLabel("Set", self)
        self.screen_label = QLabel("Set", self)

        self.tools_label.setFixedHeight(20)
        self.screen_label.setFixedHeight(20)

        # List Widgets
        self.settingsProfile_listWidget = QListWidget(self)

        # Line Edits
        self.settings_lineEdit = QLineEdit(self)

        # Layouts
        self.layout = QGridLayout(self)
        self.setLayout(self.layout)

        # Initialize
        self.setTools()
        self.setEnvironment()
        self.saveLoadSettings()

    def setTools(self) -> None:
        groupbox = QGroupBox("Tools", self)
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Buttons
        goldBP_button = QPushButton("1 Backpack", self)
        itemBP1_button = QPushButton("2 Backpack", self)
        itemBP2_button = QPushButton("3 Backpack", self)
        itemBP3_button = QPushButton("4 Backpack", self)
        hmmBP_button = QPushButton("HMM", self)
        uhBP_button = QPushButton("UH", self)
        sdBP_button = QPushButton("SD", self)
        gfbBP_button = QPushButton("GFB", self)
        rope_button = QPushButton("Rope", self)
        shovel_button = QPushButton("Shovel", self)

        # Buttons Functions
        goldBP_button.clicked.connect(lambda: self.setCoordinates(1))
        itemBP1_button.clicked.connect(lambda: self.setCoordinates(2))
        itemBP2_button.clicked.connect(lambda: self.setCoordinates(3))
        itemBP3_button.clicked.connect(lambda: self.setCoordinates(4))
        uhBP_button.clicked.connect(lambda: self.setCoordinates(5))
        hmmBP_button.clicked.connect(lambda: self.setCoordinates(6))
        sdBP_button.clicked.connect(lambda: self.setCoordinates(7))
        gfbBP_button.clicked.connect(lambda: self.setCoordinates(8))
        shovel_button.clicked.connect(lambda: self.setCoordinates(9))
        rope_button.clicked.connect(lambda: self.setCoordinates(10))

        # QHBox
        layout = QHBoxLayout(self)
        layout1 = QHBoxLayout(self)
        layout2 = QHBoxLayout(self)
        layout3 = QHBoxLayout(self)
        layout4 = QHBoxLayout(self)
        layout5 = QHBoxLayout(self)

        # Add Widgets
        layout.addWidget(self.tools_label)
        layout1.addWidget(goldBP_button)
        layout1.addWidget(itemBP1_button)
        layout2.addWidget(itemBP2_button)
        layout2.addWidget(itemBP3_button)
        layout3.addWidget(uhBP_button)
        layout3.addWidget(hmmBP_button)
        layout4.addWidget(sdBP_button)
        layout4.addWidget(gfbBP_button)
        layout5.addWidget(rope_button)
        layout5.addWidget(shovel_button)

        # Add Layouts
        groupbox_layout.addLayout(layout)
        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        groupbox_layout.addLayout(layout3)
        groupbox_layout.addLayout(layout4)
        groupbox_layout.addLayout(layout5)
        self.layout.addWidget(groupbox, 0, 1, 2, 1)

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
        self.layout.addWidget(groupbox, 1, 0)

    def setEnvironment(self) -> None:
        groupbox = QGroupBox("Environment", self)
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Buttons
        setCharacterPos_button = QPushButton("Set Character", self)
        setLootScreen_button = QPushButton("Set Loot", self)

        # Buttons Functions
        setCharacterPos_button.clicked.connect(lambda: self.setCoordinates(0))
        setLootScreen_button.clicked.connect(lambda: self.setScreen(0))

        # QHBox
        layout = QHBoxLayout(self)
        layout1 = QHBoxLayout(self)
        layout2 = QHBoxLayout(self)

        # Add Widgets
        layout.addWidget(self.screen_label)
        layout1.addWidget(setCharacterPos_button)
        layout2.addWidget(setLootScreen_button)

        # Add Layouts
        groupbox_layout.addLayout(layout)
        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        self.layout.addWidget(groupbox, 0, 0)

    # Functions
    def setScreen(self, index):
        thread = Thread(target=self.setScreen_Thread, args=(index,))
        thread.daemon = True
        thread.start()

    def setCoordinates(self, index):
        thread = Thread(target=self.setCoordinates_Thread, args=(index,))
        thread.daemon = True
        thread.start()

    # Threads
    def setScreen_Thread(self, index):
        self.screen_label.setStyleSheet("color: red")
        while True:
            screenX[index], screenY[index] = win32api.GetCursorPos()
            self.screen_label.setText(f"X = {screenX[index]} | Y = {screenY[index]}")
            time.sleep(0.05)
            if win32api.GetAsyncKeyState(VK_LBUTTON) & 0x8000:
                self.screen_label.setStyleSheet("color: blue")
                break
        time.sleep(0.1)
        while True:
            screenWidth[index], screenHeight[index] = win32api.GetCursorPos()
            self.screen_label.setText(f"X = {screenWidth[index]} | Y = {screenHeight[index]}")
            time.sleep(0.05)
            if win32api.GetAsyncKeyState(VK_LBUTTON) & 0x8000:
                self.screen_label.setStyleSheet("color: black")
                self.screen_label.setText("Set")
                screenX[index], screenY[index] = win32gui.ScreenToClient(game, (screenX[index], screenY[index]))
                screenWidth[index], screenHeight[index] = win32gui.ScreenToClient(game, (screenWidth[index], screenHeight[index]))
                return

    def setCoordinates_Thread(self, index):
        if index == 0:
            self.screen_label.setStyleSheet("color: red")
        else:
            self.tools_label.setStyleSheet("color: red")
        while True:
            coordinatesX[index], coordinatesY[index] = win32api.GetCursorPos()
            if index == 0:
                self.screen_label.setText(f"X = {coordinatesX[index]} | Y = {coordinatesY[index]}")
            else:
                self.tools_label.setText(f"X = {coordinatesX[index]} | Y = {coordinatesY[index]}")
            time.sleep(0.05)
            if win32api.GetAsyncKeyState(VK_LBUTTON) & 0x8000:
                coordinatesX[index], coordinatesY[index] = win32gui.ScreenToClient(game, (coordinatesX[index], coordinatesY[index]))
                if index == 0:
                    self.screen_label.setText("Set")
                    self.screen_label.setStyleSheet("color: black")
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
                "screenX": screenX[0],
                "screenY": screenY[0],
                "screenWidth": screenWidth[0],
                "screenHeight": screenHeight[0],
                "bpX": coordinatesX,
                "bpY": coordinatesY
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
            screenX[0] = settingsData.get("screenX")
            screenY[0] = settingsData.get("screenY")
            screenWidth[0] = settingsData.get("screenWidth")
            screenHeight[0] = settingsData.get("screenHeight")
            bpDataX = settingsData.get("bpX", [0] * 11)
            bpDataY = settingsData.get("bpY", [0] * 11)
            for i in range(len(coordinatesX)):
                coordinatesX[i] = bpDataX[i]
                coordinatesY[i] = bpDataY[i]
        self.tools_label.setStyleSheet("color: green")
        self.screen_label.setStyleSheet("color: green")
        self.screen_label.setText("Loaded")
        self.tools_label.setText("Loaded")

