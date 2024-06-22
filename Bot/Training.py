import random
import time

from Functions import *


class TrainingTab(QWidget):
    def __init__(self):
        super().__init__()
        # Load Icon
        self.setWindowIcon(QIcon('Icon.jpg'))

        # Set Title and Size
        self.setWindowTitle("Training")
        self.setFixedSize(300, 200)
        # Variables
        # Check Boxes
        self.burnMana_checkBox = QCheckBox("Burn Mana", self)
        self.startFishing_checkBox = QCheckBox("Start Fishing", self)
        self.startEat_checkBox = QCheckBox("Eat Food", self)

        # Combo Boxes
        self.hotkeyList_comboBox = QComboBox(self)

        # Line Edits
        self.mp_lineEdit = QLineEdit(self)

        # List Widgets
        self.burnMana_listWidget = QListWidget(self)

        # Buttons
        self.fishingRod_button = QPushButton("FishingRod", self)
        self.water_button = QPushButton("Water", self)
        self.addFood_button = QPushButton("Food", self)

        # Other Variables
        self.foodX = 0
        self.foodY = 0
        self.waterX = 0
        self.waterY = 0
        self.fishingRodX = 0
        self.fishingRodY = 0

        # Layouts
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        # Initialize
        self.burnManaList()
        self.addHotkeys()
        self.fishing()
        self.eatFood()

    def burnManaList(self) -> None:
        groupbox = QGroupBox("Burn Mana")
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Add Layouts
        groupbox_layout.addWidget(self.burnMana_listWidget)
        self.layout.addWidget(groupbox, 0, 0, 1, 1)

    def addHotkeys(self) -> None:
        groupbox = QGroupBox("Hotkeys")
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Buttons
        addHotkey_button = QPushButton("Add", self)

        # Buttons Functions
        addHotkey_button.clicked.connect(self.addHotkey)

        # Check Boxes
        self.burnMana_checkBox.stateChanged.connect(self.startSkill)

        # Combo Boxes
        for i in range(1, 11):
            self.hotkeyList_comboBox.addItem("F" + f'{i}')

        # QHBox
        layout1 = QHBoxLayout(self)
        layout2 = QHBoxLayout(self)

        # Add Widgets
        layout1.addWidget(self.mp_lineEdit)
        layout1.addWidget(self.hotkeyList_comboBox)
        layout1.addWidget(addHotkey_button)
        layout2.addWidget(self.burnMana_checkBox)

        # Add Layouts
        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        self.layout.addWidget(groupbox, 0, 1)

    def fishing(self) -> None:
        groupbox = QGroupBox("Fishing")
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Buttons Functions
        self.fishingRod_button.clicked.connect(lambda: self.setCoordinates(0))
        self.water_button.clicked.connect(lambda: self.setCoordinates(1))
        # Check Boxes

        # QHBox
        layout1 = QHBoxLayout(self)
        layout2 = QHBoxLayout(self)

        # Add Widgets
        layout1.addWidget(self.fishingRod_button)
        layout1.addWidget(self.water_button)
        layout2.addWidget(self.startFishing_checkBox)

        # Add Layouts
        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        self.layout.addWidget(groupbox, 1, 1)

    def eatFood(self) -> None:
        groupbox = QGroupBox("Food")
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Buttons Functions
        self.addFood_button.clicked.connect(lambda: self.setCoordinates(2))

        # QHBox
        layout1 = QHBoxLayout(self)
        layout2 = QHBoxLayout(self)

        # Add Widgets
        layout1.addWidget(self.addFood_button)
        layout2.addWidget(self.startEat_checkBox)

        # Add Layouts
        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        self.layout.addWidget(groupbox, 1, 0)

    def addHotkey(self) -> None:
        hotkeyName = self.hotkeyList_comboBox.currentText()
        hotkeyData = {"Mana": int(self.mp_lineEdit.text())}
        hotkey = QListWidgetItem(hotkeyName)
        hotkey.setData(Qt.UserRole, hotkeyData)
        self.burnMana_listWidget.addItem(hotkey)
        self.mp_lineEdit.clear()

    def setCoordinates(self, index):
        thread = Thread(target=self.setCoordinates_Thread, args=(index,))
        thread.daemon = True
        thread.start()

    def setCoordinates_Thread(self, index) -> None:
        while True:
            x, y = win32api.GetCursorPos()
            if index == 0:
                self.fishingRod_button.setText(f"{x, y}")
            elif index == 1:
                self.water_button.setText(f"{x, y}")
            else:
                self.addFood_button.setText(f"{x, y}")
            time.sleep(0.05)
            if win32api.GetAsyncKeyState(VK_LBUTTON) & 0x8000:
                x, y = win32gui.ScreenToClient(game, (x, y))
                if index == 0:
                    self.fishingRod_button.setText("FishingRod")
                    self.fishingRodX = x
                    self.fishingRodY = y
                elif index == 1:
                    self.water_button.setText("Water")
                    self.waterX = x
                    self.waterY = y
                else:
                    self.addFood_button.setText("Food")
                    self.foodX = x
                    self.foodY = y
                return

    def startSkill(self) -> None:
        thread = Thread(target=self.startSkill_Thread)
        thread.daemon = True
        if self.burnMana_checkBox.checkState() == 2:
            thread.start()

    def startSkill_Thread(self) -> None:
        timer = 0.0
        while self.burnMana_checkBox.checkState():
            for index in range(self.burnMana_listWidget.count()):
                myMana = c.c_double.from_buffer(readPointer(myStatsPtr, myMPOffset)).value
                hotkeyData = self.burnMana_listWidget.item(index).data(Qt.UserRole)
                hotkeyMana = hotkeyData['Mana']
                if myMana >= hotkeyMana:
                    pressHotkey(int(self.burnMana_listWidget.item(index).text()[1:]))
                    time.sleep(0.5)
                    timer += 0.5
            time.sleep(1)
            timer += 1
            if timer > 60:
                timer = 0
                antyIdle()


