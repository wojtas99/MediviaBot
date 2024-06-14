import time

from Functions import *


class HealingTab(QWidget):
    def __init__(self):
        super().__init__()
        # Variables
        # Check Boxes
        self.startHealing_checkBox = QCheckBox("Start Healing", self)

        # Combo Boxes
        self.hpMana_comboBox = QComboBox(self)
        self.hotkeyRuneList_comboBox = QComboBox(self)

        # Line Edits
        self.hpBelow_line = QLineEdit(self)
        self.hpAbove_line = QLineEdit(self)
        self.minMp_line = QLineEdit(self)
        self.minMp_line.hide()

        # Labels
        self.mp_label = QLabel("Min MP:", self)
        self.mp_label.hide()

        # List Widgets
        self.healList_listWidget = QListWidget(self)

        self.layout = QGridLayout(self)
        self.setLayout(self.layout)

        # Functions
        self.healList()
        self.healHotkeyRune()
        self.startHealing()

    def healList(self) -> None:
        groupbox = QGroupBox("Heal List")
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Add Layouts
        groupbox_layout.addWidget(self.healList_listWidget)
        groupbox.setFixedSize(150, 250)
        self.layout.addWidget(groupbox, 0, 0, 2, 1, alignment=Qt.AlignTop)

    def healHotkeyRune(self) -> None:
        groupbox = QGroupBox("Hotkeys&&Runes")
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Buttons
        addHotkey_button = QPushButton("Add", self)

        # Buttons Functions
        addHotkey_button.clicked.connect(self.addHealing)

        # Combo Boxes
        self.hpMana_comboBox.addItem("HP%")
        self.hpMana_comboBox.addItem("HP")
        self.hpMana_comboBox.addItem("MP%")
        self.hpMana_comboBox.addItem("MP")
        self.hotkeyRuneList_comboBox.addItem("UH")
        self.hotkeyRuneList_comboBox.addItem("Potion")
        for i in range(1, 13):
            self.hotkeyRuneList_comboBox.addItem("F" + f'{i}')

        # Combo Boxes Functions
        self.hotkeyRuneList_comboBox.currentIndexChanged.connect(self.runeHotkeyListChange)
        self.hpMana_comboBox.currentIndexChanged.connect(self.runeHotkeyListChange)

        # QHBox
        layout1 = QHBoxLayout(self)
        layout2 = QHBoxLayout(self)
        layout3 = QHBoxLayout(self)
        layout4 = QHBoxLayout(self)

        # Add Widgets
        layout1.addWidget(self.hpMana_comboBox)
        layout1.addWidget(self.hotkeyRuneList_comboBox)
        layout2.addWidget(QLabel("Below:", self))
        layout2.addWidget(self.hpBelow_line)
        layout2.addWidget(QLabel("Above:", self))
        layout2.addWidget(self.hpAbove_line)
        layout3.addWidget(self.mp_label)
        layout3.addWidget(self.minMp_line)
        layout4.addWidget(addHotkey_button)

        # Add Layouts
        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        groupbox_layout.addLayout(layout3)
        groupbox_layout.addLayout(layout4)
        self.layout.addWidget(groupbox, 0, 1)

    def startHealing(self):
        groupbox = QGroupBox("Start")
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Check Boxes Functions
        self.startHealing_checkBox.stateChanged.connect(self.checkStartState)

        # QHBox
        layout1 = QHBoxLayout(self)

        # Add Widgets
        layout1.addWidget(self.startHealing_checkBox)

        # Add Layouts
        groupbox_layout.addLayout(layout1)
        self.layout.addWidget(groupbox, 1, 1, 1, 1, alignment=Qt.AlignTop)

    def runeHotkeyListChange(self):
        if self.hotkeyRuneList_comboBox.currentIndex() != 0 and self.hpMana_comboBox.currentIndex() < 2:
            self.mp_label.show()
            self.minMp_line.show()
            self.minMp_line.setEnabled(True)
        else:
            self.mp_label.hide()
            self.minMp_line.hide()
            self.minMp_line.setEnabled(False)

    def addHealing(self) -> None:
        healName = self.hotkeyRuneList_comboBox.currentText()
        healName += " " + self.hpMana_comboBox.currentText()
        if self.minMp_line.text() == "":
            self.minMp_line.setText("0")
        if healName:
            healData = {"Type": self.hpMana_comboBox.currentText(),
                        "Option": self.hotkeyRuneList_comboBox.currentText(),
                        "Below": int(self.hpBelow_line.text()),
                        "Above": int(self.hpAbove_line.text()),
                        "MinMp": int(self.minMp_line.text())}
            heal = QListWidgetItem(healName)
            heal.setData(Qt.UserRole, healData)
            self.healList_listWidget.addItem(heal)
            self.hpAbove_line.clear()
            self.hpBelow_line.clear()
            self.minMp_line.clear()

    def checkStartState(self) -> None:
        thread = Thread(target=self.startHealing_Thread)
        thread.daemon = True
        if self.startHealing_checkBox.checkState() == 2:
            thread.start()

    def startHealing_Thread(self):
        while self.startHealing_checkBox.checkState() == 2:
            for healIndex in range(self.healList_listWidget.count()):
                healData = self.healList_listWidget.item(healIndex).data(Qt.UserRole)
                healType = healData['Type']
                healOption = healData['Option']
                healBelow = healData['Below']
                healAbove = healData['Above']
                healMinMP = healData['MinMp']
                myHp = c.c_double.from_buffer(readPointer(myStatsPtr, myHPOffset)).value
                myMaxHp = c.c_double.from_buffer(readPointer(myStatsPtr, myHPMAXOffset)).value
                myMp = c.c_double.from_buffer(readPointer(myStatsPtr, myMPOffset)).value
                myMaxMp = c.c_double.from_buffer(readPointer(myStatsPtr, myMPMAXOffset)).value
                if healType[0:2] == "HP":
                    if healOption == "UH":
                        if '%' in healType:
                            lock_acquired = False
                            try:
                                while healAbove <= (myHp * 100 / myMaxHp) < healBelow:
                                    if not lock_acquired:
                                        lock.acquire()
                                        lock_acquired = True
                                    myHp = c.c_double.from_buffer(readPointer(myStatsPtr, myHPOffset)).value
                                    useOnMe(bpX[4], bpY[4])
                                    time.sleep(0.5)
                            finally:
                                if lock_acquired:
                                    lock.release()
                        else:
                            lock_acquired = False
                            try:
                                while healAbove <= myHp < healBelow:
                                    if not lock_acquired:
                                        lock.acquire()
                                        lock_acquired = True
                                    myHp = c.c_double.from_buffer(readPointer(myStatsPtr, myHPOffset)).value
                                    useOnMe(bpX[4], bpY[4])
                                    time.sleep(0.5)
                            finally:
                                if lock_acquired:
                                    lock.release()
                    else:
                        if '%' in healType:
                            lock_acquired = False
                            try:
                                while healAbove <= (myHp * 100 / myMaxHp) < healBelow and myMp >= healMinMP:
                                    if not lock_acquired:
                                        lock.acquire()
                                        lock_acquired = True
                                    myHp = c.c_double.from_buffer(readPointer(myStatsPtr, myHPOffset)).value
                                    myMp = c.c_double.from_buffer(readPointer(myStatsPtr, myMPOffset)).value
                                    pressHotkey(int(healOption[1:]))
                                    time.sleep(0.5)
                            finally:
                                if lock_acquired:
                                    lock.release()
                        else:
                            lock_acquired = False
                            try:
                                while healAbove <= myHp < healBelow and myMp >= healMinMP:
                                    if not lock_acquired:
                                        lock.acquire()
                                        lock_acquired = True
                                    myHp = c.c_double.from_buffer(readPointer(myStatsPtr, myHPOffset)).value
                                    myMp = c.c_double.from_buffer(readPointer(myStatsPtr, myMPOffset)).value
                                    pressHotkey(int(healOption[1:]))
                                    time.sleep(0.5)
                            finally:
                                if lock_acquired:
                                    lock.release()
                else:
                    if '%' in healType:
                        lock_acquired = False
                        try:
                            while healAbove <= (myMp * 100 / myMaxMp) < healBelow:
                                if not lock_acquired:
                                    lock.acquire()
                                    lock_acquired = True
                                myMp = c.c_double.from_buffer(readPointer(myStatsPtr, myMPOffset)).value
                                useOnMe(bpX[4], bpY[4])
                                time.sleep(0.5)
                        finally:
                            if lock_acquired:
                                lock.release()



