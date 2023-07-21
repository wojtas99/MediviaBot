import time

from PyQt5.QtWidgets import *
from window_capture import WindowCapture
import numpy as np
import cv2 as cv
from funkcje import *
from threading import Thread
from PyQt5.QtGui import *


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.resize(500, 500)
        #  Title and Size
        self.setWindowTitle("EasyBot")
        tab = QTabWidget()
        tab.addTab(TargetTab(), "Target")
        tab.addTab(RuneTab(), "Rune")
        vbox = QVBoxLayout(self)
        vbox.addWidget(tab)
        self.setLayout(vbox)


class TargetTab(QWidget):
    def __init__(self):
        super().__init__()
        win_cap = WindowCapture('Medivia')
        game = win32gui.FindWindow(None, 'Medivia')

        self.monster_list = QListWidget(self)
        self.monster_list.setGeometry(0, 0, 150, 200)

        monster_name = QLabel("Monster :", self)
        monster_name.setGeometry(160, 0, 50, 20)
        self.textfield = QLineEdit(self)
        self.textfield.setGeometry(210, 0, 100, 20)

        add_monster = QPushButton("Add", self)
        add_monster.setGeometry(209, 20, 40, 25)
        add_monster.clicked.connect(self.create_monster)

        left = QPushButton("<", self)
        left.setGeometry(0, 200, 30, 25)
        left.clicked.connect(self.go_left)
        right = QPushButton(">", self)
        right.setGeometry(31, 200, 30, 25)
        right.clicked.connect(self.go_right)

        del_monster = QPushButton("Del", self)
        del_monster.setGeometry(111, 200, 40, 25)
        del_monster.clicked.connect(self.delete_monster)

        self.target_status = QCheckBox(self)
        self.target_status.move(0, 400)
        target_status_text = QLabel("Start Targeting", self)
        target_status_text.setGeometry(17, 390, 100, 30)

        def list_monsters():
            while True:
                value = ReadMemory(game)
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
                            for monster in combined_list:
                                for i in range(self.monster_list.count()):
                                    if monster[2] == self.monster_list.item(i).text():
                                        print(monster[0])
                                        print(monster[1])
                                        click_right(monster[0], monster[1], game)
                                        return

                time.sleep(0.05)

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
