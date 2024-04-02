import time
import urllib.request
from datetime import datetime

from rembg import remove

from funkcje import *


class LootTab(QWidget):
    def __init__(self):
        super().__init__()

        self.set_gold_bp = QPushButton("Set Loot Backpack", self)
        self.set_gold_bp.setGeometry(301, 370, 120, 25)
        self.set_gold_bp.clicked.connect(self.set_gold_backpack)

        loot_status = QCheckBox(self)
        loot_status.move(0, 260)
        loot_status_text = QLabel("Open Monsters", self)
        loot_status_text.setGeometry(17, 251, 100, 30)

        blackList_label = QLabel("BlackList", self)
        blackList_label.setGeometry(0, 0, 100, 20)
        self.black_list = QListWidget(self)
        self.black_list.setGeometry(0, 20, 150, 235)

        collect_label = QLabel("Collect List", self)
        collect_label.setGeometry(200, 0, 100, 20)
        self.collect_list = QListWidget(self)
        self.collect_list.setGeometry(190, 20, 150, 100)
        add_to_collect = QPushButton("Collect", self)
        add_to_collect.setGeometry(150, 50, 40, 25)
        add_to_collect.clicked.connect(self.add_collect)

        use_label = QLabel("Use List", self)
        use_label.setGeometry(200, 120, 100, 20)
        self.use_list = QListWidget(self)
        self.use_list.setGeometry(190, 145, 150, 115)
        add_to_use = QPushButton("Use", self)
        add_to_use.setGeometry(150, 190, 40, 25)
        add_to_use.clicked.connect(self.add_use)

        self.mouse_status = QLabel(self)
        self.mouse_status.setGeometry(301, 410, 150, 30)
        self.mouse_status.setStyleSheet('color: red')

        self.gold_bp_x = 0
        self.gold_bp_y = 0

        def item_list():
            f = open('Loot.txt', 'r')
            tmp = 0
            for item in f:
                name = item.split('/')[-1]
                name = name.strip('\n')
                for files in os.listdir('Loot/'):
                    tmp = 0
                    if files == name:
                        tmp = 1
                        break
                if tmp:
                    continue
                urllib.request.urlretrieve(item, 'Loot/'+name)
                image1 = Image.open('Loot/'+name)
                image1 = remove(image1)
                image1.save('Loot/'+name)
                image1 = Image.open('Loot/'+name)
                image2 = Image.open('background.png')
                image2.paste(image1, (0, 0), image1)
                image2.save('Loot/'+name)
            for file in os.listdir("Loot"):
                self.black_list.addItem(f"{file.split('.')[0]}")

        item_list()

        def start_loot_thread():
            thread = Thread(target=open_monster)
            thread.daemon = True  # Daemonize the thread to terminate it when the main thread exits
            if loot_status.checkState() == 2:
                thread.start()

        loot_status.stateChanged.connect(start_loot_thread)

        def open_monster():
            win_cap = WindowCapture('Medivia', 190, 680, 1730, 350)
            savedX = 0
            savedY = 0
            monsterX = 0
            monsterY = 0
            loot = 0
            while loot_status.checkState() == 2:
                targetID = read_memory(attack, 0)
                targetID = c.c_ulonglong.from_buffer(targetID).value
                while targetID != 0:
                    if loot == 0:
                        loot = 1
                    targetID = read_memory(attack, 0)
                    targetID = c.c_ulonglong.from_buffer(targetID).value
                    savedX = monsterX
                    savedY = monsterY
                    monsterY = read_memory(targetID - base_adr, 0x3C)
                    monsterY = c.c_int.from_buffer(monsterY).value
                    monsterX = read_memory(targetID - base_adr, 0x38)
                    monsterX = c.c_int.from_buffer(monsterX).value
                    if monsterX > 60000:
                        break
                    time.sleep(0.1)
                if loot == 1:
                    loot = 0
                    time.sleep(0.1)
                    x = read_memory(myX, 0)
                    x = c.c_int.from_buffer(x).value
                    y = read_memory(myY, 0)
                    y = c.c_int.from_buffer(y).value
                    x = savedX - x
                    y = savedY - y
                    x = 855 + x * 70
                    y = 460 + y * 70
                    win32gui.PostMessage(game, win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(x, y))
                    win32gui.PostMessage(game, win32con.WM_RBUTTONDOWN, 2, win32api.MAKELONG(x, y))
                    win32gui.PostMessage(game, win32con.WM_RBUTTONUP, 0, win32api.MAKELONG(x, y))
                    time.sleep(0.2)
                    for _ in range(3):
                        for items in range(self.use_list.count()):
                            item = 'Loot/'f'{self.use_list.item(items).text()}' + '.png'
                            with lock:
                                screenshot = win_cap.get_screenshot()
                                screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
                                template = cv.imread(item, 0)
                                result = cv.matchTemplate(screenshot, template, cv.TM_CCOEFF_NORMED)
                                locations = list(zip(*(np.where(result >= 0.75))[::-1]))
                                locations = merge_close_points(locations, 10)
                                locations = sorted(locations, key=lambda point: (point[1], point[0]), reverse=True)
                                for x, y in locations:
                                    click_right(int(x) + 1740, int(y) + 336)
                                    time.sleep(0.1)
                        for items in range(self.collect_list.count()):
                            item = 'Loot/'f'{self.collect_list.item(items).text()}' + '.png'
                            with lock:
                                screenshot = win_cap.get_screenshot()
                                screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
                                template = cv.imread(item, 0)
                                result = cv.matchTemplate(screenshot, template, cv.TM_CCOEFF_NORMED)
                                locations = list(zip(*(np.where(result >= 0.75))[::-1]))
                                locations = merge_close_points(locations, 10)
                                locations = sorted(locations, key=lambda point: (point[1], point[0]), reverse=True)
                                for x, y in locations:
                                    collect_items(int(x) + 1740, int(y) + 336, self.gold_bp_x, self.gold_bp_y - 20)
                                    time.sleep(0.1)
                time.sleep(0.1)

    def mouse_cords(self):
        while True:
            x, y = win32api.GetCursorPos()
            self.mouse_status.setText('x ='f"{x}"'           y = 'f'{y}')
            if win32api.GetAsyncKeyState(VK_LBUTTON) & 0x8000:
                self.mouse_status.setText("")
                x, y = win32gui.ScreenToClient(game, (x, y))
                gold_bp_x = x
                gold_bp_y = y
                self.set_gold_bp.setText("GOOD Job")
                self.set_gold_bp.setStyleSheet("color: green")
                return

    def set_gold_backpack(self):
        self.set_gold_bp.setText("Left-Click on spot")
        self.set_gold_bp.setStyleSheet("color: red")
        thread = Thread(target=self.mouse_cords)
        thread.daemon = True
        thread.start()
        return

    def add_collect(self, item):
        selected_item = self.black_list.currentItem()
        if selected_item:
            self.collect_list.addItem(self.black_list.item(self.black_list.row(selected_item)).text())

    def add_use(self):
        selected_item = self.black_list.currentItem()
        if selected_item:
            self.use_list.addItem(self.black_list.item(self.black_list.row(selected_item)).text())

