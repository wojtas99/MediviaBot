import random

from funkcje import *


class SkillTab(QWidget):
    def __init__(self):
        super().__init__()
        # Variables
        self.setBait_button = None
        self.setFood_button = None
        self.setWater_button = None
        self.setFishingRod_button = None
        self.startFishing_checkBox = None
        self.antyIdle_checkBox = None
        self.foodX = 0
        self.foodY = 0
        self.waterX = 0
        self.waterY = 0
        self.fishingRodX = 0
        self.fishingRodY = 0
        self.baitX = 0
        self.baitY = 0
        self.bait = 0
        self.hotkeyList_comboBox = None
        self.manaPoints_line = None
        self.startEat_checkBox = None
        self.startSkill_checkBox = None
        self.burnMana_listWidget = None

        self.layout = QGridLayout()
        self.setLayout(self.layout)
        # Functions
        self.groupbox1()
        self.groupbox2()
        self.groupbox3()

    def groupbox1(self) -> None:
        groupbox = QGroupBox("Burn Mana List")
        groupbox_layout = QVBoxLayout()
        groupbox.setLayout(groupbox_layout)

        # List Widgets
        self.burnMana_listWidget = QListWidget(self)

        # Add Layouts
        groupbox_layout.addWidget(self.burnMana_listWidget)
        self.layout.addWidget(groupbox, 0, 0, alignment=Qt.AlignTop | Qt.AlignLeft)
        groupbox.setFixedSize(150, 150)

    def groupbox2(self) -> None:
        groupbox = QGroupBox("Set Hotkey")
        groupbox_layout = QVBoxLayout()
        groupbox.setLayout(groupbox_layout)

        # Buttons
        addHotkey_button = QPushButton("Add", self)
        addHotkey_button.clicked.connect(self.addHotkey)

        self.setFood_button = QPushButton("Select Food", self)
        self.setFood_button.clicked.connect(self.setFood_thread)

        # Check Boxes
        self.startSkill_checkBox = QCheckBox(self)
        self.startSkill_checkBox.setFixedWidth(15)
        self.startSkill_checkBox.stateChanged.connect(self.startSkill_thread)
        self.antyIdle_checkBox = QCheckBox(self)
        self.antyIdle_checkBox.setFixedWidth(15)

        # Combo Boxes
        self.hotkeyList_comboBox = QComboBox(self)
        for i in range(1, 13):
            self.hotkeyList_comboBox.addItem("F" + f'{i}')

        # Labels
        manaList_label = QLabel("MP:", self)
        startSkill_label = QLabel("Start Skill", self)
        antyIdle_label = QLabel("Anty Idle", self)

        # Edit Lines
        self.manaPoints_line = QLineEdit()

        # QHBox
        layout1 = QHBoxLayout()
        layout1.addWidget(manaList_label)
        layout1.addWidget(self.manaPoints_line)
        layout1.addWidget(self.hotkeyList_comboBox)
        layout1.addWidget(addHotkey_button)
        layout2 = QHBoxLayout()
        layout2.addWidget(self.startSkill_checkBox)
        layout2.addWidget(startSkill_label)
        layout2.addWidget(self.setFood_button)
        layout3 = QHBoxLayout()
        layout3.addWidget(self.antyIdle_checkBox)
        layout3.addWidget(antyIdle_label)

        # Add Layouts
        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        groupbox_layout.addLayout(layout3)
        groupbox.setFixedSize(240, 180)
        self.layout.addWidget(groupbox, 0, 1, alignment=Qt.AlignTop | Qt.AlignLeft)

    def groupbox3(self) -> None:
        groupbox = QGroupBox("Fishing")
        groupbox_layout = QVBoxLayout()
        groupbox.setLayout(groupbox_layout)

        # Buttons
        self.setFishingRod_button = QPushButton("Select FishingRod", self)
        self.setFishingRod_button.clicked.connect(self.setFishingRod_thread)

        self.setWater_button = QPushButton("Select Water", self)
        self.setWater_button.clicked.connect(self.setWater_thread)

        self.setBait_button = QPushButton("Select Bait", self)
        self.setBait_button.clicked.connect(self.setBait_thread)

        # Check Boxes
        self.startFishing_checkBox = QCheckBox(self)
        self.startFishing_checkBox.setFixedWidth(15)
        self.startFishing_checkBox.stateChanged.connect(self.startFishing_thread)

        # Labels
        startFishing_label = QLabel("Start Fishing", self)

        # QHBox
        layout1 = QHBoxLayout()
        layout1.addWidget(self.setFishingRod_button)
        layout2 = QHBoxLayout()
        layout2.addWidget(self.setWater_button)
        layout3 = QHBoxLayout()
        layout3.addWidget(self.setBait_button)
        layout4 = QHBoxLayout()
        layout4.addWidget(self.startFishing_checkBox)
        layout4.addWidget(startFishing_label)

        # Add Layouts
        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        groupbox_layout.addLayout(layout3)
        groupbox_layout.addLayout(layout4)
        groupbox.setFixedSize(150, 120)
        self.layout.addWidget(groupbox, 1, 0, alignment=Qt.AlignTop | Qt.AlignLeft)

    def addHotkey(self) -> None:
        hotkey = self.hotkeyList_comboBox.currentText()
        self.burnMana_listWidget.addItem('Mana=' + f'{self.manaPoints_line.text()}' + ' hotkey:' + hotkey)

    def setFood_thread(self) -> None:
        thread = Thread(target=self.setFood)
        thread.daemon = True
        thread.start()
        return

    def setFood(self) -> None:
        while True:
            x, y = win32api.GetCursorPos()
            self.setFood_button.setText(str(x)+"| "+str(y))
            if win32api.GetAsyncKeyState(VK_LBUTTON) & 0x8000:
                x, y = win32gui.ScreenToClient(game, (x, y))
                self.foodX = x
                self.foodY = y
                self.setFood_button.setStyleSheet("color: green")
                return

    def startSkill_thread(self) -> None:
        thread = Thread(target=self.startSkill)
        thread.daemon = True
        if self.startSkill_checkBox.checkState() == 2:
            thread.start()

    def startSkill(self) -> None:
        timer = 0
        while self.startFishing_checkBox.checkState() == 2 and self.startSkill_checkBox.checkState() == 0 and self.waterX != 0 and self.fishingRodX != 0 and self.baitX != 0:
            if self.bait == 0:
                click_right(self.baitX, self.baitY)
                click_left(self.waterX, self.waterY)
                time.sleep(random.uniform(1.0, 1.1))
            click_right(self.fishingRodX, self.fishingRodY)
            click_left(self.waterX, self.waterY)
            self.bait += 1
            time.sleep(random.uniform(1.0, 1.1))
            if self.bait >= 1010:
                self.bait = 0
        while self.startSkill_checkBox.checkState() == 2:
            for index in range(self.burnMana_listWidget.count()):
                item = self.burnMana_listWidget.item(index)
                item = item.text()
                mana = item.split('h')[0]
                mana = mana[5:]
                mana = float(mana)
                hotkey = item.split(':')[1]
                myMana = read_pointer(maxHp, myManaOffsets)
                myMana = c.c_double.from_buffer(myMana).value
                if len(hotkey) <= 3:
                    hotkey = hotkey[1:]
                    hotkey = int(hotkey)
                    if myMana >= mana:
                        press_hotkey(hotkey)
                        time.sleep(0.3)
                time.sleep(0.5)
                timer += 0.5
                if timer >= 60:
                    timer = 0
                    if self.foodX != 0:
                        for _ in range(5):
                            click_right(self.foodX, self.foodY)
                            time.sleep(0.1)
                    if self.antyIdle_checkBox.checkState() == 2:
                        antyIdle()
                    time.sleep(0.2)

    def setFishingRod_thread(self) -> None:
        thread = Thread(target=self.setFishingRod)
        thread.daemon = True
        thread.start()
        return

    def setFishingRod(self) -> None:
        while True:
            x, y = win32api.GetCursorPos()
            self.setFishingRod_button.setText("Fishing Rod: " + str(x) + " | " + str(y))
            time.sleep(0.05)
            if win32api.GetAsyncKeyState(VK_LBUTTON) & 0x8000:
                x, y = win32gui.ScreenToClient(game, (x, y))
                self.fishingRodX = x
                self.fishingRodY = y
                return

    def setWater_thread(self) -> None:
        thread = Thread(target=self.setWater)
        thread.daemon = True
        thread.start()
        return

    def setWater(self) -> None:
        while True:
            x, y = win32api.GetCursorPos()
            self.setWater_button.setText(str(x)+"| "+str(y))
            time.sleep(0.05)
            if win32api.GetAsyncKeyState(VK_LBUTTON) & 0x8000:
                x, y = win32gui.ScreenToClient(game, (x, y))
                self.waterX = x
                self.waterY = y
                return

    def setBait_thread(self) -> None:
        thread = Thread(target=self.setBait)
        thread.daemon = True
        thread.start()
        return

    def setBait(self) -> None:
        while True:
            x, y = win32api.GetCursorPos()
            self.setBait_button.setText(str(x)+"| "+str(y))
            time.sleep(0.05)
            if win32api.GetAsyncKeyState(VK_LBUTTON) & 0x8000:
                x, y = win32gui.ScreenToClient(game, (x, y))
                self.baitX = x
                self.baitY = y
                return

    def startFishing_thread(self) -> None:
        thread = Thread(target=self.startSkill)
        thread.daemon = True
        thread.start()
        return

