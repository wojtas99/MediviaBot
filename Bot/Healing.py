import time

from Functions import *


class HealingTab(QWidget):
    def __init__(self):
        super().__init__()
        # Load Icon
        self.setWindowIcon(QIcon('Icon.jpg'))

        # Set Title and Size
        self.setWindowTitle("Healing")
        self.setFixedSize(300, 180)
        # Variables
        # Check Boxes
        self.startHealing_checkBox = QCheckBox("Start Healing", self)

        # Combo Boxes
        self.hpMana_comboBox = QComboBox(self)
        self.hotkeyRuneList_comboBox = QComboBox(self)

        # Line Edits
        self.hpBelow_lineEdit = QLineEdit(self)
        self.hpAbove_lineEdit = QLineEdit(self)
        self.minMp_lineEdit = QLineEdit(self)
        self.minMp_lineEdit.hide()

        # Labels
        self.mp_label = QLabel("Min MP:", self)
        self.mp_label.hide()

        # List Widgets
        self.healList_listWidget = QListWidget(self)

        # Layouts
        self.layout = QGridLayout(self)
        self.setLayout(self.layout)

        # Initialize
        self.healList()
        self.healHotkeyRune()
        self.startHealing()

    def healList(self) -> None:
        groupbox = QGroupBox("Heal List")
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Add Layouts
        groupbox_layout.addWidget(self.healList_listWidget)
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
        for i in range(1, 11):
            self.hotkeyRuneList_comboBox.addItem("F" + f'{i}')

        # Combo Boxes Functions
        self.hotkeyRuneList_comboBox.currentIndexChanged.connect(self.runeHotkeyListChange)
        self.hpMana_comboBox.currentIndexChanged.connect(self.runeHotkeyListChange)

        # QHBox
        layout1 = QHBoxLayout(self)
        layout2 = QHBoxLayout(self)
        layout3 = QHBoxLayout(self)

        # Add Widgets
        layout1.addWidget(self.hpMana_comboBox)
        layout1.addWidget(self.hotkeyRuneList_comboBox)
        layout2.addWidget(QLabel("Below:", self))
        layout2.addWidget(self.hpBelow_lineEdit)
        layout2.addWidget(QLabel("Above:", self))
        layout2.addWidget(self.hpAbove_lineEdit)
        layout3.addWidget(self.mp_label)
        layout3.addWidget(self.minMp_lineEdit)
        layout3.addWidget(addHotkey_button)

        # Add Layouts
        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        groupbox_layout.addLayout(layout3)
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
            self.minMp_lineEdit.show()
            self.minMp_lineEdit.setEnabled(True)
        else:
            self.mp_label.hide()
            self.minMp_lineEdit.hide()
            self.minMp_lineEdit.setEnabled(False)

    def addHealing(self) -> None:
        healName = self.hotkeyRuneList_comboBox.currentText()
        healName += " " + self.hpMana_comboBox.currentText()
        if self.minMp_lineEdit.text() == "":
            self.minMp_lineEdit.setText("0")
        if healName:
            healData = {"Type": self.hpMana_comboBox.currentText(),
                        "Option": self.hotkeyRuneList_comboBox.currentText(),
                        "Below": int(self.hpBelow_lineEdit.text()),
                        "Above": int(self.hpAbove_lineEdit.text()),
                        "MinMp": int(self.minMp_lineEdit.text())}
            heal = QListWidgetItem(healName)
            heal.setData(Qt.UserRole, healData)
            self.healList_listWidget.addItem(heal)
            self.hpAbove_lineEdit.clear()
            self.hpBelow_lineEdit.clear()
            self.minMp_lineEdit.clear()

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
                time.sleep(0.5)
                if healType[0:2] == "HP":
                    if healOption == "UH":
                        if '%' in healType:
                            while healAbove <= (myHp * 100 / myMaxHp) < healBelow:
                                useOnMe(coordinatesX[5], coordinatesY[5])
                                time.sleep(1)
                                myHp = c.c_double.from_buffer(readPointer(myStatsPtr, myHPOffset)).value
                        else:
                            while healAbove <= myHp < healBelow:
                                useOnMe(coordinatesX[5], coordinatesY[5])
                                time.sleep(1)
                                myHp = c.c_double.from_buffer(readPointer(myStatsPtr, myHPOffset)).value
                    else:
                        if '%' in healType:
                            while healAbove <= (myHp * 100 / myMaxHp) < healBelow and myMp >= healMinMP:
                                pressHotkey(int(healOption[1:]))
                                time.sleep(1)
                                myHp = c.c_double.from_buffer(readPointer(myStatsPtr, myHPOffset)).value
                                myMp = c.c_double.from_buffer(readPointer(myStatsPtr, myMPOffset)).value
                        else:
                            while healAbove <= myHp < healBelow and myMp >= healMinMP:
                                pressHotkey(int(healOption[1:]))
                                time.sleep(1)
                                myHp = c.c_double.from_buffer(readPointer(myStatsPtr, myHPOffset)).value
                                myMp = c.c_double.from_buffer(readPointer(myStatsPtr, myMPOffset)).value
                else:
                    if '%' in healType:
                        while healAbove <= (myMp * 100 / myMaxMp) < healBelow:
                            useOnMe(coordinatesX[5], coordinatesY[5])
                            time.sleep(1)
                            myMp = c.c_double.from_buffer(readPointer(myStatsPtr, myMPOffset)).value



