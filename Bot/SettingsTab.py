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
        self.generalProfile_listWidget = QListWidget(self)

        # Line Edits
        self.generalProfile_line = QLineEdit(self)

        # Layout
        self.layout = QGridLayout(self)
        self.setLayout(self.layout)

        # Init View
        self.setBP()
        self.setEnvironment()
        self.setTools()
        self.saveSettings()

    def setBP(self) -> None:
        groupbox = QGroupBox("Backpacks&&Runes", self)
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Buttons
        goldBP_button = QPushButton("Gold Backpack", self)
        itemBP1_button = QPushButton("1 Item Backpack", self)
        itemBP2_button = QPushButton("2 Item Backpack", self)
        itemBP3_button = QPushButton("3 Item Backpack", self)
        hmmBP_button = QPushButton("HMM Backpack", self)
        uhBP_button = QPushButton("UH Backpack", self)
        sdBP_button = QPushButton("SD Backpack", self)
        gfbBP_button = QPushButton("GFB Backpack", self)

        # Buttons Functions
        goldBP_button.clicked.connect(lambda: self.chooseItem(0))
        itemBP1_button.clicked.connect(lambda: self.chooseItem(1))
        itemBP2_button.clicked.connect(lambda: self.chooseItem(2))
        itemBP3_button.clicked.connect(lambda: self.chooseItem(3))
        uhBP_button.clicked.connect(lambda: self.chooseItem(4))
        hmmBP_button.clicked.connect(lambda: self.chooseItem(5))
        sdBP_button.clicked.connect(lambda: self.chooseItem(6))
        gfbBP_button.clicked.connect(lambda: self.chooseItem(7))

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
        knife_button = QPushButton("Skin Knife", self)

        # Buttons Functions
        shovel_button.clicked.connect(lambda: self.chooseItem(8))
        rope_button.clicked.connect(lambda: self.chooseItem(9))
        pick_button.clicked.connect(lambda: self.chooseItem(10))
        knife_button.clicked.connect(lambda: self.chooseItem(11))

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
        layout4.addWidget(knife_button)

        # Add Layouts
        groupbox_layout.addLayout(layout)
        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        groupbox_layout.addLayout(layout3)
        groupbox_layout.addLayout(layout4)
        groupbox.setFixedWidth(150)
        self.layout.addWidget(groupbox, 0, 0)

    def saveSettings(self) -> None:
        groupbox = QGroupBox("Save&&Load Settings", self)
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Buttons
        saveProfile_button = QPushButton("Save", self)
        loadProfile_button = QPushButton("Load", self)

        # List Widgets
        for file in os.listdir("Settings"):
            self.generalProfile_listWidget.addItem(f"{file.split('.')[0]}")

        # QHBox
        layout1 = QHBoxLayout(self)
        layout2 = QHBoxLayout(self)

        # Add Widgets
        layout1.addWidget(QLabel("Name:", self))
        layout1.addWidget(self.generalProfile_line)
        layout2.addWidget(saveProfile_button)
        layout2.addWidget(loadProfile_button)

        # Add Layouts
        groupbox_layout.addWidget(self.generalProfile_listWidget)
        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        groupbox.setFixedWidth(150)
        self.layout.addWidget(groupbox, 2, 0)

    def setEnvironment(self) -> None:
        groupbox = QGroupBox("Environment", self)
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Buttons
        setScreen_button = QPushButton("Set Screen", self)
        setLoot_button = QPushButton("Set Loot", self)

        # Buttons Functions
        setScreen_button.clicked.connect(lambda: self.setScreen(0))
        setLoot_button.clicked.connect(lambda: self.setScreen(1))

        # QHBox
        layout = QHBoxLayout(self)
        layout1 = QHBoxLayout(self)
        layout2 = QHBoxLayout(self)

        # Add Widgets
        layout.addWidget(self.screen_label)
        layout1.addWidget(setScreen_button)
        layout2.addWidget(setLoot_button)

        # Add Layouts
        groupbox_layout.addLayout(layout)
        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        groupbox.setFixedWidth(150)
        self.layout.addWidget(groupbox, 1, 0)

    # Functions
    def setScreen(self, id):
        thread = Thread(target=self.setScreen_thread, args=(id,))
        thread.daemon = True
        thread.start()

    def chooseItem(self, id):
        thread = Thread(target=self.chooseBP_Thread, args=(id,))
        thread.daemon = True
        thread.start()

    # Threads
    def setScreen_thread(self, id):
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
                return

    def chooseBP_Thread(self, id):
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
