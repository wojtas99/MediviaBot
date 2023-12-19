from funkcje import *


class HealingTab(QWidget):
    def __init__(self):
        super().__init__()
        # Variables
        self.healthPointsRune_line = None
        self.setRune_button = None
        self.healthPointsHotkey_line = None
        self.manaPoints_line = None
        self.hotkeyList_comboBox = None
        self.healing_listWidget = None
        self.startHealing_checkBox = None
        self.runeX = 0
        self.runeY = 0

        self.layout = QGridLayout()
        self.setLayout(self.layout)
        # Functions
        self.groupbox1()
        self.groupbox2()
        self.groupbox3()
        self.groupbox4()

    def groupbox1(self) -> None:
        groupbox = QGroupBox("Healing List")
        groupbox_layout = QVBoxLayout()
        groupbox.setLayout(groupbox_layout)

        # List Widgets
        self.healing_listWidget = QListWidget(self)

        # Add Layouts
        groupbox_layout.addWidget(self.healing_listWidget)
        self.layout.addWidget(groupbox, 0, 0, alignment=Qt.AlignTop | Qt.AlignLeft)
        groupbox.setFixedSize(150, 150)

    def groupbox2(self) -> None:
        groupbox = QGroupBox("Set Heal Hotkey")
        groupbox_layout = QVBoxLayout()
        groupbox.setLayout(groupbox_layout)

        # Buttons
        addHotkey_button = QPushButton("Add", self)
        addHotkey_button.clicked.connect(self.addHotkey)

        # Combo Boxes
        self.hotkeyList_comboBox = QComboBox(self)
        for i in range(1, 13):
            self.hotkeyList_comboBox.addItem("F" + f'{i}')

        # Labels
        manaList_label = QLabel("MP:", self)
        manaList_label.setFixedWidth(200)
        healthList_label = QLabel("HP %", self)
        healthList_label.setFixedWidth(40)

        # Edit Lines
        self.manaPoints_line = QLineEdit()
        self.healthPointsHotkey_line = QLineEdit()
        self.healthPointsHotkey_line.setFixedWidth(30)
        self.healthPointsHotkey_line.setMaxLength(3)

        # QHBox
        layout1 = QHBoxLayout()
        layout1.addWidget(healthList_label)
        layout1.addWidget(manaList_label)
        layout2 = QHBoxLayout()
        layout2.addWidget(self.healthPointsHotkey_line)
        layout2.addWidget(self.manaPoints_line)
        layout2.addWidget(self.hotkeyList_comboBox)
        layout2.addWidget(addHotkey_button)

        # Add Layouts
        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        groupbox.setFixedSize(200, 80)
        self.layout.addWidget(groupbox, 0, 1, alignment=Qt.AlignTop | Qt.AlignLeft)

    def groupbox3(self) -> None:
        groupbox = QGroupBox("Set Heal Rune")
        groupbox_layout = QVBoxLayout()
        groupbox.setLayout(groupbox_layout)

        # Buttons
        addRune_button = QPushButton("Add", self)
        addRune_button.clicked.connect(self.addRune)
        self.setRune_button = QPushButton("Select Rune", self)
        self.setRune_button.clicked.connect(self.setRune_thread)

        # Labels
        healthList_label = QLabel("HP %", self)
        healthList_label.setFixedWidth(300)

        # Edit Lines
        self.healthPointsRune_line = QLineEdit()
        self.healthPointsRune_line.setFixedWidth(30)
        self.healthPointsRune_line.setMaxLength(3)

        # QHBox
        layout1 = QHBoxLayout()
        layout1.addWidget(healthList_label)
        layout2 = QHBoxLayout()
        layout2.addWidget(self.healthPointsRune_line)
        layout2.addWidget(self.setRune_button)
        layout2.addWidget(addRune_button)

        # Add Layouts
        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        groupbox.setFixedSize(200, 80)
        self.layout.addWidget(groupbox, 1, 1, alignment=Qt.AlignTop)

    def groupbox4(self) -> None:
        groupbox = QGroupBox("Start Healing")
        groupbox_layout = QVBoxLayout()
        groupbox.setLayout(groupbox_layout)

        # Check Boxes
        self.startHealing_checkBox = QCheckBox(self)
        self.startHealing_checkBox.stateChanged.connect(self.startHealing_thread)

        # Labels
        startHealing_label = QLabel("Start Healer", self)
        startHealing_label.setFixedWidth(200)

        # QHBox
        layout1 = QHBoxLayout()
        layout1.addWidget(self.startHealing_checkBox)
        layout1.addWidget(startHealing_label)

        # Add Layouts
        groupbox_layout.addLayout(layout1)
        groupbox.setFixedSize(200, 80)
        self.layout.addWidget(groupbox, 2, 1, alignment=Qt.AlignTop)

    def addHotkey(self) -> None:
        hotkey = self.hotkeyList_comboBox.currentText()
        if hotkey and self.healthPointsHotkey_line.text() and self.manaPoints_line.text():
            self.healing_listWidget.addItem('HP=' + f'{self.healthPointsHotkey_line.text()}' + '% MP=' + f'{self.manaPoints_line.text()}' + ' hotkey:' + hotkey)

    def setRune_thread(self) -> None:
        thread = Thread(target=self.setRune)
        thread.daemon = True
        thread.start()
        return

    def setRune(self) -> None:
        while True:
            x, y = win32api.GetCursorPos()
            self.setRune_button.setText(str(x) + "| " + str(y))
            if win32api.GetAsyncKeyState(VK_LBUTTON) & 0x8000:
                x, y = win32gui.ScreenToClient(game, (x, y))
                self.runeX = x
                self.runeY = y
                self.setRune_button.setText("Select Rune")
                return

    def addRune(self):
        if self.runeX != 0 and self.healthPointsRune_line.text():
            self.healing_listWidget.addItem('HP=' + f'{self.healthPointsRune_line.text()}' + '% runePos:x=' + f'{self.runeX}' + '|y=' + f'{self.runeY}')

    def startHealing_thread(self) -> None:
        thread = Thread(target=self.startHealing)
        thread.daemon = True
        if self.startHealing_checkBox.checkState() == 2:
            thread.start()

    def startHealing(self) -> None:
        maxHP = read_pointer(maxHp, maxHpOffsets)
        maxHP = c.c_double.from_buffer(maxHP).value
        while self.startHealing_checkBox.checkState():
            for index in range(self.healing_listWidget.count()):
                item = self.healing_listWidget.item(index)
                item = item.text()
                hpHeal = item.split('%')[0]
                hpHeal = hpHeal[3:]
                hpHeal = float(hpHeal)
                hotkey = item.split(':')[1]
                myHp = read_pointer(maxHp, myHpOffsets)
                myHp = c.c_double.from_buffer(myHp).value
                myMana = read_pointer(maxHp, myManaOffsets)
                myMana = c.c_double.from_buffer(myMana).value
                if len(hotkey) <= 3:
                    hotkey = hotkey[1:]
                    hotkey = int(hotkey)
                    mana_heal = item.split('MP=')[1]
                    mana_heal = mana_heal.split('h')[0]
                    mana_heal = float(mana_heal)
                    if (myHp <= (maxHP * 0.01 * hpHeal)) and myMana >= mana_heal:
                        press_hotkey(hotkey)
                        time.sleep(0.3)
                else:
                    x = hotkey.split('x=')[1]
                    x = x.split('|')[0]
                    x = int(x)
                    y = hotkey.split('y=')[1]
                    y = int(y)
                    if myHp <= (maxHP * 0.01 * hpHeal):
                        use_on_myself(x, y)
                        time.sleep(0.3)
                time.sleep(0.2)

