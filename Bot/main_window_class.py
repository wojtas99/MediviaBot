import os
import time
from PyQt5.QtWidgets import *
from window_capture import WindowCapture
import numpy as np
import cv2 as cv
from funkcje import *
from threading import Thread


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(500, 500)
        #  Title and Size
        self.setWindowTitle("EasyBot")
        tab = QTabWidget(self)
        tab.addTab(TargetTab(), "Monster Targeting")
        tab.addTab(CaveTab(), "CaveBot")
        tab.addTab(RuneTab(), "RuneMaker")
        vbox = QVBoxLayout(self)
        vbox.addWidget(tab)
        self.setLayout(vbox)


class TargetTab(QWidget):
    def __init__(self):
        super().__init__()

        self.monster_list = QListWidget(self)
        self.monster_list.setGeometry(0, 20, 150, 200)

        self.save_targeting_list = QListWidget(self)
        self.save_targeting_list.setGeometry(300, 320, 120, 80)
        for file in os.listdir("Targeting"):
            self.save_targeting_list.addItem(f"{file.split('.')[0]}")

        self.save_targeting_text = QLabel("Name", self)
        self.save_targeting_text.setGeometry(301, 400, 100, 20)

        self.save_targeting_textfield = QLineEdit(self)
        self.save_targeting_textfield.setGeometry(335, 401, 85, 20)

        self.save_targeting_button = QPushButton("Save", self)
        self.save_targeting_button.setGeometry(334, 421, 41, 20)
        self.save_targeting_button.clicked.connect(self.save_monster_list)

        self.load_targeting_button = QPushButton("Load", self)
        self.load_targeting_button.setGeometry(380, 421, 41, 20)
        self.load_targeting_button.clicked.connect(self.load_monster_list)

        text_label = QLabel("Targeting", self)
        text_label.setGeometry(0, 0, 100, 20)

        monster_name = QLabel("Monster ", self)
        monster_name.setGeometry(160, 20, 50, 20)

        self.textfield = QLineEdit(self)
        self.textfield.setGeometry(210, 20, 100, 20)

        add_monster = QPushButton("Add", self)
        add_monster.setGeometry(209, 40, 40, 25)
        add_monster.clicked.connect(self.create_monster)

        left = QPushButton("<", self)
        left.setGeometry(0, 220, 30, 25)
        left.clicked.connect(self.go_left)

        right = QPushButton(">", self)
        right.setGeometry(31, 220, 30, 25)
        right.clicked.connect(self.go_right)

        del_monster = QPushButton("Del", self)
        del_monster.setGeometry(111, 220, 40, 25)
        del_monster.clicked.connect(self.delete_monster)

        clear_monsters = QPushButton("Clear", self)
        clear_monsters.setGeometry(66, 220, 40, 25)
        clear_monsters.clicked.connect(self.clear_monster_list)

        self.target_status = QCheckBox(self)
        self.target_status.move(0, 400)
        target_status_text = QLabel("Start Targeting", self)
        target_status_text.setGeometry(17, 390, 100, 30)

        self.loot_status = QCheckBox(self)
        self.loot_status.move(0, 370)
        loot_status_text = QLabel("Open Monsters", self)
        loot_status_text.setGeometry(17, 360, 100, 30)

    def clear_monster_list(self):
        self.monster_list.clear()

    def save_monster_list(self):
        if self.save_targeting_textfield.text() != '':
            f = open("Targeting/"f"{self.save_targeting_textfield.text()}.txt", "w")
            self.save_targeting_list.addItem(f'{self.save_targeting_textfield.text()}')
            self.save_targeting_textfield.clear()
            for i in range(self.monster_list.count()):
                f.write(f'{self.monster_list.item(i).text()}\n')
            f.close()

    def load_monster_list(self):
        self.monster_list.clear()
        selected_item = self.save_targeting_list.currentItem()
        if selected_item:
            f = open("Targeting/"f"{self.save_targeting_list.item(self.save_targeting_list.row(selected_item)).text()}.txt")
            for monster in f:
                if monster != '\n':
                    self.monster_list.addItem(monster.split("\n")[0])
            f.close()

        def list_monsters():
            game = win32gui.FindWindow(None, 'Medivia')
            win_cap = WindowCapture('Medivia')
            procID = win32process.GetWindowThreadProcessId(game)
            procID = procID[1]
            process_handle = c.windll.kernel32.OpenProcess(0x1F0FFF, False, procID)
            modules = win32process.EnumProcessModules(process_handle)
            base_adr = modules[0]
            while True:
                value = read_memory(0xDBEEA8, base_adr, game)
                value = c.c_ulonglong.from_buffer(value).value
                if self.target_status.checkState() == 2:
                    if value == 0:
                        img = win_cap.get_screenshot()
                        lower = np.array([9, 180, 150])
                        upper = np.array([14, 190, 255])
                        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
                        mask = cv.inRange(hsv, lower, upper)
                        output = cv.bitwise_and(img, img, mask=mask)
                        coordinates, monsters = get_text(output)
                        combined_list = [(coordinates[i * 2], coordinates[i * 2 + 1], monster) for i, monster in
                                         enumerate(monsters)]
                        combined_list = sorted(combined_list, key=distance)
                        if monsters:
                            continue_while = True
                            for monster in combined_list:
                                for i in range(self.monster_list.count()):
                                    if monster[2] == self.monster_list.item(i).text():
                                        click_right(monster[0], monster[1], game)
                                        continue_while = False
                                        time.sleep(1)
                                        break
                                if not continue_while:
                                    break

                time.sleep(0.1)

        def loot_monster():
            game = win32gui.FindWindow(None, 'Medivia')
            loot = 0
            monsterX = 0
            savedX = 0
            savedY = 0
            monsterY = 0
            procID = win32process.GetWindowThreadProcessId(game)
            procID = procID[1]
            process_handle = c.windll.kernel32.OpenProcess(0x1F0FFF, False, procID)
            modules = win32process.EnumProcessModules(process_handle)
            base_adr = modules[0]
            while True:
                while self.loot_status.checkState() == 2:
                    targetID = read_memory(0xDBEEA8, base_adr, game)
                    targetID = c.c_ulonglong.from_buffer(targetID).value
                    while targetID != 0:
                        if loot == 0:
                            loot = 1
                        targetID = read_memory(0xDBEEA8, base_adr, game)
                        targetID = c.c_ulonglong.from_buffer(targetID).value
                        savedX = monsterX
                        savedY = monsterY
                        monsterY = read_memory(targetID + 0x3C, 0, game)
                        monsterY = c.c_int.from_buffer(monsterY).value
                        monsterX = read_memory(targetID + 0x38, 0, game)
                        monsterX = c.c_int.from_buffer(monsterX).value
                        time.sleep(0.01)
                        if monsterX > 60000:
                            monsterX = savedX
                            monsterY = savedY
                            break
                    if loot == 1:
                        x = read_memory(0xDBFC48, base_adr, game)
                        x = c.c_int.from_buffer(x).value
                        y = read_memory(0xDBFC4C, base_adr, game)
                        y = c.c_int.from_buffer(y).value
                        x = savedX - x
                        y = savedY - y
                        x = 875 + x * 70
                        y = 475 + y * 70
                        click_right(x, y, game)
                        time.sleep(2)
                    loot = 0

                time.sleep(1)

        loot_thread = Thread(target=loot_monster)
        loot_thread.daemon = True  # Daemonize the thread to terminate it when the main thread exits
        loot_thread.start()

        monster_thread = Thread(target=list_monsters)
        monster_thread.daemon = True  # Daemonize the thread to terminate it when the main thread exits
        monster_thread.start()

    def delete_monster(self):
        selected_item = self.monster_list.currentItem()
        if selected_item:
            self.monster_list.takeItem(self.monster_list.row(selected_item))

    def create_monster(self):
        if self.textfield.text() != '':
            self.monster_list.addItem(self.textfield.text())
            self.textfield.clear()

    def go_right(self):
        self.monster_list.setCurrentRow(self.monster_list.currentRow() + 1)

    def go_left(self):
        self.monster_list.setCurrentRow(self.monster_list.currentRow() - 1)


class RuneTab(QWidget):
    def __init__(self):
        super().__init__()


class CaveTab(QWidget):
    def __init__(self):
        super().__init__()
        self.waypoints_list = QListWidget(self)
        self.waypoints_list.setGeometry(0, 20, 150, 200)

        label_text = QLabel("Waypoints", self)
        label_text.setGeometry(0, 0, 100, 20)

        left = QPushButton("<", self)
        left.setGeometry(0, 220, 30, 25)
        right = QPushButton(">", self)
        right.setGeometry(31, 220, 30, 25)

        del_waypoint = QPushButton("Del", self)
        del_waypoint.setGeometry(111, 220, 40, 25)

        self.cave_status = QCheckBox(self)
        self.cave_status.move(0, 400)
        cave_status_text = QLabel("Follow Waypoints", self)
        cave_status_text.setGeometry(17, 390, 100, 30)

        stand = QPushButton("Stand", self)
        stand.setGeometry(200, 10, 40, 25)
        north = QPushButton("North", self)
        north.setGeometry(241, 10, 40, 25)
        south = QPushButton("South", self)
        south.setGeometry(241, 36, 40, 25)
        west = QPushButton("West", self)
        west.setGeometry(200, 36, 40, 25)
        east = QPushButton("East", self)
        east.setGeometry(282, 36, 40, 25)
        action = QPushButton("Action", self)
        action.setGeometry(282, 10, 40, 25)


