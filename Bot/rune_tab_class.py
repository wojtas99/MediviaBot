from funkcje import *

class RuneTab(QWidget):
    def __init__(self):
        super().__init__()

        label_text = QLabel("BurnMana List", self)
        label_text.setGeometry(0, 0, 100, 20)

        self.burn_mana_list = QListWidget(self)
        self.burn_mana_list.setGeometry(0, 20, 180, 130)
        self.add_spell_button = QPushButton("Add", self)
        self.add_spell_button.setGeometry(362, 19, 40, 22)
        self.add_spell_button.clicked.connect(self.add_burn_mana_spell)

        healingMana_label = QLabel("Mana", self)
        healingMana_label.setGeometry(322, 0, 50, 20)
        self.mana_hotkey_line = QLineEdit(self)
        self.mana_hotkey_line.setGeometry(322, 20, 40, 20)
        self.mana_hotkey_line.setMaxLength(6)

        self.hotkey_list = QComboBox(self)
        self.hotkey_list.setGeometry(250, 20, 70, 20)
        for i in range(1, 13):
            self.hotkey_list.addItem("F" + f'{i}')

        train_status = QCheckBox(self)
        train_status.move(0, 290)
        train_status_label = QLabel("MakeRunes", self)
        train_status_label.setGeometry(17, 281, 100, 30)

        def list_monsters_thread():
            thread = Thread(target=start_training)
            thread.daemon = True  # Daemonize the thread to terminate it when the main thread exits
            if train_status.checkState() == 2:
                thread.start()

        train_status.stateChanged.connect(list_monsters_thread)

        def start_training():
            while train_status.checkState():
                for index in range(self.burn_mana_list.count()):
                    item = self.burn_mana_list.item(index)
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

    def add_burn_mana_spell(self):
        hotkey = self.hotkey_list.currentText()
        self.burn_mana_list.addItem('Mana=' + f'{self.mana_hotkey_line.text()}' + ' hotkey:' + hotkey)