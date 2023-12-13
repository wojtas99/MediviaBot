from funkcje import *


class HealingTab(QWidget):
    def __init__(self):
        super().__init__()

        self.my_maxHP = read_pointer(maxHp, maxHpOffsets)
        self.my_maxHP = c.c_double.from_buffer(self.my_maxHP).value

        label_text = QLabel("Healing List", self)
        label_text.setGeometry(0, 0, 100, 20)

        self.save_healing_list = QListWidget(self)
        self.save_healing_list.setGeometry(0, 20, 180, 130)

        self.add_spell_button = QPushButton("Add", self)
        self.add_spell_button.setGeometry(362, 19, 40, 22)
        self.add_spell_button.clicked.connect(self.add_healing_spell)

        healingHotkey_label = QLabel("Healing Hotkey", self)
        healingHotkey_label.setGeometry(250, 0, 100, 20)

        healingMana_label = QLabel("Mana", self)
        healingMana_label.setGeometry(322, 0, 50, 20)
        self.mana_hotkey_line = QLineEdit(self)
        self.mana_hotkey_line.setGeometry(322, 20, 40, 20)
        self.mana_hotkey_line.setMaxLength(6)

        self.hotkey_list = QComboBox(self)
        self.hotkey_list.setGeometry(250, 20, 70, 20)
        for i in range(1, 13):
            self.hotkey_list.addItem("F" + f'{i}')

        hp_hotkey_label = QLabel("HP %", self)
        hp_hotkey_label.setGeometry(215, 0, 30, 20)
        self.hp_hotkey_line = QLineEdit(self)
        self.hp_hotkey_line.setGeometry(215, 20, 30, 20)
        self.hp_hotkey_line.setMaxLength(3)

        healingRune_label = QLabel("Healing Rune", self)
        healingRune_label.setGeometry(250, 40, 100, 20)
        hp_rune_label = QLabel("HP %", self)
        hp_rune_label.setGeometry(215, 40, 30, 20)
        self.hp_rune_line = QLineEdit(self)
        self.hp_rune_line.setGeometry(215, 60, 30, 20)
        self.hp_rune_line.setMaxLength(3)

        self.add_rune_button = QPushButton("Add", self)
        self.add_rune_button.setGeometry(352, 59, 40, 22)
        self.add_rune_button.clicked.connect(self.add_healing_rune)

        self.chose_rune_button = QPushButton("Select Rune", self)
        self.chose_rune_button.setStyleSheet('color: red')
        self.chose_rune_button.setGeometry(250, 59, 100, 22)
        self.chose_rune_button.clicked.connect(self.chose_rune)

        healing_status = QCheckBox(self)
        healing_status.move(0, 290)
        healing_status_label = QLabel("Healing On", self)
        healing_status_label.setGeometry(17, 281, 100, 30)

        def list_monsters_thread():
            thread = Thread(target=start_healing)
            thread.daemon = True  # Daemonize the thread to terminate it when the main thread exits
            if healing_status.checkState() == 2:
                thread.start()

        healing_status.stateChanged.connect(list_monsters_thread)

        def start_healing():
            while healing_status.checkState():
                for index in range(self.save_healing_list.count()):
                    item = self.save_healing_list.item(index)
                    item = item.text()
                    hp_heal = item.split('%')[0]
                    hp_heal = hp_heal[3:]
                    hp_heal = float(hp_heal)
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
                        if (myHp <= (self.my_maxHP * 0.01 * hp_heal)) and myMana >= mana_heal:
                            press_hotkey(hotkey)
                            time.sleep(0.3)
                    else:
                        x = hotkey.split('x=')[1]
                        x = x.split('|')[0]
                        x = int(x)
                        y = hotkey.split('y=')[1]
                        y = int(y)
                        if myHp <= (self.my_maxHP * 0.01 * hp_heal):
                            use_on_myself(x, y)
                            time.sleep(0.3)
                    time.sleep(0.2)

        self.x = 0
        self.y = 0

    def add_healing_spell(self):
        hotkey = self.hotkey_list.currentText()
        self.save_healing_list.addItem('HP=' + f'{self.hp_hotkey_line.text()}' + '% MP=' + f'{self.mana_hotkey_line.text()}' + ' hotkey:' + hotkey)

    def add_healing_rune(self):
        hotkey = self.hotkey_list.currentText()
        self.save_healing_list.addItem('HP=' + f'{self.hp_rune_line.text()}' + '% runePos:x=' + f'{self.x}' + '|y=' + f'{self.y}')
        self.chose_rune_button.setStyleSheet('color: red')
        self.chose_rune_button.setText('Select Rune')

    def set_healing_rune(self):
        while True:
            x, y = win32api.GetCursorPos()
            self.chose_rune_button.setText('x='f"{x}"' y='f'{y}')
            if win32api.GetAsyncKeyState(VK_LBUTTON) & 0x8000:
                x, y = win32gui.ScreenToClient(game, (x, y))
                self.x = x
                self.y = y
                self.chose_rune_button.setText("Selected")
                self.chose_rune_button.setStyleSheet("color: green")
                return

    def chose_rune(self):
        self.chose_rune_button.setText("LeftClick")
        self.chose_rune_button.setStyleSheet("color: green")
        thread = Thread(target=self.set_healing_rune)
        thread.daemon = True
        thread.start()

