import os
import time
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QMovie
from window_capture import WindowCapture
import numpy as np
import cv2 as cv
from funkcje import *
from threading import Thread
import re


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
        '''
        parent_widget = QWidget(self)
        parent_widget.setStyleSheet(f"background-image: url(background.jpg);")
        parent_widget.resize(500, 500)
        '''

        label = QLabel(self)
        movie = QMovie("Demon.gif")
        label.setMovie(movie)
        label.move(200, 100)
        movie.start()

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

        self.delete_targeting_button = QPushButton("Del", self)
        self.delete_targeting_button.setGeometry(299, 421, 31, 20)
        self.delete_targeting_button.clicked.connect(self.delete_list)

        text_label = QLabel("Targeting", self)
        text_label.setGeometry(0, 0, 100, 20)
        #text_label.setStyleSheet("color: yellow")

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
        self.target_status.move(0, 290)
        target_status_text = QLabel("Start Targeting", self)
        target_status_text.setGeometry(17, 281, 100, 30)

        self.loot_status = QCheckBox(self)
        self.loot_status.move(0, 260)
        loot_status_text = QLabel("Open Monsters", self)
        loot_status_text.setGeometry(17, 251, 100, 30)

        def list_monsters():
            game = win32gui.FindWindow(None, 'Medivia')
            procID = win32process.GetWindowThreadProcessId(game)
            procID = procID[1]
            process_handle = c.windll.kernel32.OpenProcess(0x1F0FFF, False, procID)
            modules = win32process.EnumProcessModules(process_handle)
            base_adr = modules[0]
            win_cap = WindowCapture('Medivia')
            while True:
                value = read_memory(0xDBEEA8, base_adr, 0, procID)
                value = c.c_ulonglong.from_buffer(value).value
                if self.target_status.checkState() == 2:
                    if value == 0:
                        time.sleep(1)
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
                                        break
                                if not continue_while:
                                    break

                time.sleep(0.1)

        def loot_monster():
            game = win32gui.FindWindow(None, 'Medivia')
            procID = win32process.GetWindowThreadProcessId(game)
            procID = procID[1]
            process_handle = c.windll.kernel32.OpenProcess(0x1F0FFF, False, procID)
            modules = win32process.EnumProcessModules(process_handle)
            base_adr = modules[0]
            loot = 0
            monsterX = 0
            savedX = 0
            savedY = 0
            monsterY = 0
            while True:
                while self.loot_status.checkState() == 2:
                    targetID = read_memory(0xDBEEA8, base_adr, 0, procID)
                    targetID = c.c_ulonglong.from_buffer(targetID).value
                    while targetID != 0:
                        if loot == 0:
                            loot = 1
                        targetID = read_memory(0xDBEEA8, base_adr, 0, procID)
                        targetID = c.c_ulonglong.from_buffer(targetID).value
                        savedX = monsterX
                        savedY = monsterY
                        monsterY = read_memory(targetID, 0, 0x3C, procID)
                        monsterY = c.c_int.from_buffer(monsterY).value
                        monsterX = read_memory(targetID, 0, 0x38, procID)
                        monsterX = c.c_int.from_buffer(monsterX).value
                        time.sleep(0.01)
                        if monsterX > 60000:
                            monsterX = savedX
                            monsterY = savedY
                            break
                    if loot == 1:
                        x = read_memory(0xDBFC48, base_adr, 0, procID)
                        x = c.c_int.from_buffer(x).value
                        y = read_memory(0xDBFC4C, base_adr, 0, procID)
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

    def delete_list(self):
        selected_item = self.save_targeting_list.currentItem()
        if selected_item:
            os.remove('Targeting/'f'{self.save_targeting_list.item(self.save_targeting_list.row(selected_item)).text()}.txt')
            self.save_targeting_list.takeItem(self.save_targeting_list.row(selected_item))

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
        self.waypoints_list.setGeometry(0, 20, 170, 200)

        label_text = QLabel("Waypoints", self)
        label_text.setGeometry(0, 0, 100, 20)

        left = QPushButton("<", self)
        left.setGeometry(0, 220, 30, 25)
        right = QPushButton(">", self)
        right.setGeometry(31, 220, 30, 25)

        del_waypoint = QPushButton("Del", self)
        del_waypoint.setGeometry(111, 220, 40, 25)
        del_waypoint.clicked.connect(self.delete_wpt_item)

        clear_waypoint = QPushButton("Clear", self)
        clear_waypoint.setGeometry(66, 220, 40, 25)
        clear_waypoint.clicked.connect(self.clear_wpt_list)

        cave_status = QCheckBox(self)
        cave_status.move(0, 260)
        cave_status_text = QLabel("Follow Waypoints", self)
        cave_status_text.setGeometry(17, 251, 100, 30)

        stand = QPushButton("Stand", self)
        stand.setGeometry(200, 20, 40, 25)
        stand.clicked.connect(self.stand_add)

        north = QPushButton("North", self)
        north.setGeometry(241, 20, 40, 25)

        action = QPushButton("Action", self)
        action.setGeometry(282, 20, 40, 25)

        south = QPushButton("South", self)
        south.setGeometry(241, 46, 40, 25)

        west = QPushButton("West", self)
        west.setGeometry(200, 46, 40, 25)

        east = QPushButton("East", self)
        east.setGeometry(282, 46, 40, 25)

        auto_rec_label = QLabel("Auto Recording", self)
        auto_rec_label.setGeometry(17, 281, 100, 30)
        auto_rec_box = QCheckBox(self)
        auto_rec_box.move(0, 290)

        def start_auto_rec_thread():
            autorec_thread = Thread(target=auto_rec)
            autorec_thread.daemon = True  # Daemonize the thread to terminate it when the main thread exits
            if auto_rec_box.checkState() == 2:
                autorec_thread.start()

        auto_rec_box.stateChanged.connect(start_auto_rec_thread)

        def start_follow_thread():
            follow_wpt_thread = Thread(target=follow_wpt)
            follow_wpt_thread.daemon = True  # Daemonize the thread to terminate it when the main thread exits
            if cave_status.checkState() == 2:
                follow_wpt_thread.start()

        cave_status.stateChanged.connect(start_follow_thread)

        def auto_rec():
            game = win32gui.FindWindow(None, 'Medivia')
            procID = win32process.GetWindowThreadProcessId(game)
            procID = procID[1]
            process_handle = c.windll.kernel32.OpenProcess(0x1F0FFF, False, procID)
            modules = win32process.EnumProcessModules(process_handle)
            base_adr = modules[0]
            x = read_memory(0xDBFC48, base_adr, 0, procID)
            y = read_memory(0xDBFC4C, base_adr, 0, procID)
            z = read_memory(0xDBFC50, base_adr, 0, procID)
            x = c.c_int.from_buffer(x).value
            y = c.c_int.from_buffer(y).value
            z = c.c_int.from_buffer(z).value
            while True:
                if auto_rec_box.checkState() == 0:
                    return
                new_x = read_memory(0xDBFC48, base_adr, 0, procID)
                new_y = read_memory(0xDBFC4C, base_adr, 0, procID)
                new_z = read_memory(0xDBFC50, base_adr, 0, procID)
                new_x = c.c_int.from_buffer(new_x).value
                new_y = c.c_int.from_buffer(new_y).value
                new_z = c.c_int.from_buffer(new_z).value
                if x != new_x or y != new_y or z != new_z:
                    self.waypoints_list.addItem('X : 'f'{new_x}  Y : 'f'{new_y}  Z : 'f'{new_z}')
                    x = read_memory(0xDBFC48, base_adr, 0, procID)
                    y = read_memory(0xDBFC4C, base_adr, 0, procID)
                    z = read_memory(0xDBFC50, base_adr, 0, procID)
                    x = c.c_int.from_buffer(x).value
                    y = c.c_int.from_buffer(y).value
                    z = c.c_int.from_buffer(z).value
                time.sleep(0.2)

        def follow_wpt():
            game = win32gui.FindWindow(None, 'Medivia')
            procID = win32process.GetWindowThreadProcessId(game)
            procID = procID[1]
            process_handle = c.windll.kernel32.OpenProcess(0x1F0FFF, False, procID)
            modules = win32process.EnumProcessModules(process_handle)
            base_adr = modules[0]
            while True:
                if cave_status.checkState() == 0:
                    return
                for i in range(self.waypoints_list.count()):
                    numbers = re.sub(r'\D', ' ', self.waypoints_list.item(i).text())
                    wpt = [num for num in numbers.split(' ') if num]
                    self.waypoints_list.setCurrentRow(i)
                    while True:
                        if cave_status.checkState() == 0:
                            return
                        time.sleep(0.1)
                        x = read_memory(0xDBFC48, base_adr, 0, procID)
                        y = read_memory(0xDBFC4C, base_adr, 0, procID)
                        z = read_memory(0xDBFC50, base_adr, 0, procID)
                        x = c.c_int.from_buffer(x).value
                        y = c.c_int.from_buffer(y).value
                        z = c.c_int.from_buffer(z).value
                        if x == int(wpt[0]) and y == int(wpt[1]) and z == int(wpt[2]):
                            break
                        else:
                            myx = int(wpt[0]) - x
                            myy = int(wpt[1]) - y
                        if myy == -1 or myy == -2:
                            win32gui.SendMessage(game, win32con.WM_KEYDOWN, win32con.VK_UP, 0x01480001)
                            win32gui.SendMessage(game, win32con.WM_KEYUP, win32con.VK_UP, 0x01480001)
                            continue
                        if myy == 1 or myy == 2:
                            win32gui.SendMessage(game, win32con.WM_KEYDOWN, win32con.VK_DOWN, 0x01500001)
                            win32gui.SendMessage(game, win32con.WM_KEYUP, win32con.VK_DOWN, 0x01500001)
                            continue
                        if myx == -1 or myx == -2:
                            win32gui.SendMessage(game, win32con.WM_KEYDOWN, win32con.VK_LEFT, 0x014B0001)
                            win32gui.SendMessage(game, win32con.WM_KEYUP, win32con.VK_LEFT, 0x014B0001)
                            continue
                        if myx == 1 or myx == 2:
                            win32gui.SendMessage(game, win32con.WM_KEYDOWN, win32con.VK_RIGHT, 0x014D0001)
                            win32gui.SendMessage(game, win32con.WM_KEYUP, win32con.VK_RIGHT, 0x014D0001)
                            continue
                        x = 875 + myx * 70
                        y = 475 + myy * 70
                        click_left(x, y, game)
                        time.sleep(4)

    def delete_wpt_item(self):
        selected_item = self.waypoints_list.currentItem()
        if selected_item:
            self.waypoints_list.takeItem(self.waypoints_list.row(selected_item))

    def clear_wpt_list(self):
        self.waypoints_list.clear()

    def stand_add(self):
        game = win32gui.FindWindow(None, 'Medivia')
        procID = win32process.GetWindowThreadProcessId(game)
        procID = procID[1]
        process_handle = c.windll.kernel32.OpenProcess(0x1F0FFF, False, procID)
        modules = win32process.EnumProcessModules(process_handle)
        base_adr = modules[0]
        x = read_memory(0xDBFC48, base_adr, 0, procID)
        y = read_memory(0xDBFC4C, base_adr, 0, procID)
        z = read_memory(0xDBFC50, base_adr, 0, procID)

        x = c.c_int.from_buffer(x).value
        y = c.c_int.from_buffer(y).value
        z = c.c_int.from_buffer(z).value
        self.waypoints_list.addItem('X:'f'{x} Y:'f'{y} Z:'f'{z}')




