import urllib.request
from funkcje import *


class LootTab(QWidget):
    def __init__(self):
        super().__init__()

        self.set_gold_bp = QPushButton("Set Gold Backpack", self)
        self.set_gold_bp.setGeometry(301, 220, 120, 25)
        self.set_gold_bp.clicked.connect(self.set_gold_backpack)

        self.loot_status = QCheckBox(self)
        self.loot_status.move(0, 260)
        loot_status_text = QLabel("Open Monsters", self)
        loot_status_text.setGeometry(17, 251, 100, 30)

        text_label = QLabel("BlackList", self)
        text_label.setGeometry(0, 0, 100, 20)

        self.black_list = QListWidget(self)
        self.black_list.setGeometry(0, 20, 150, 200)

        self.white_list = QListWidget(self)
        self.white_list.setGeometry(190, 20, 150, 200)

        add_to_loot = QPushButton("Add", self)
        add_to_loot.setGeometry(150, 100, 40, 25)
        add_to_loot.clicked.connect(self.add)

        self.mouse_status = QLabel(self)
        self.mouse_status.setGeometry(301, 180, 150, 30)
        self.mouse_status.setStyleSheet('color: red')

        self.gold_bp_x = 0
        self.gold_bp_y = 0

        def loot_items():
            lower = np.array([0, 0, 0])
            upper = np.array([255, 254, 255])
            f = open('Loot.txt', 'r')
            for item in f:
                name = item.split('/')[-1]
                name = name.strip('\n')
                '''
                if name.split('.')[-1] == 'gif':
                    gif = imageio.mimread(item)
                    img = [cv.cvtColor(img, cv.COLOR_RGB2BGR) for img in gif]
                    cv.imwrite('Loot/'+name.split('.')[0]+'.png', img[0])
                '''
                urllib.request.urlretrieve(item, 'Loot/'+name)
                img = cv.imread('Loot/'+name)
                hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
                mask = cv.inRange(hsv, lower, upper)
                output = cv.bitwise_and(img, img, mask=mask)
                cv.imwrite('Loot/' + name, output)
            for file in os.listdir("Loot"):
                self.black_list.addItem(f"{file.split('.')[0]}")

        def open_monster():
            game = win32gui.FindWindow(None, 'Medivia')
            procID = win32process.GetWindowThreadProcessId(game)
            procID = procID[1]
            process_handle = c.windll.kernel32.OpenProcess(0x1F0FFF, False, procID)
            modules = win32process.EnumProcessModules(process_handle)
            base_adr = modules[0]
            monsterX = 0
            savedX = 0
            savedY = 0
            monsterY = 0
            threshold = 0.6
            win_cap = WindowCapture('Medivia', 190, 680, 1730, 350)
            while True:
                while self.loot_status.checkState() == 2:
                    targetID = read_memory(0xDBEEA8, base_adr, 0, procID)
                    targetID = c.c_ulonglong.from_buffer(targetID).value
                    while targetID != 0:
                        targetID = read_memory(0xDBEEA8, base_adr, 0, procID)
                        targetID = c.c_ulonglong.from_buffer(targetID).value
                        savedX = monsterX
                        savedY = monsterY
                        monsterY = read_memory(targetID, 0, 0x3C, procID)
                        monsterY = c.c_int.from_buffer(monsterY).value
                        monsterX = read_memory(targetID, 0, 0x38, procID)
                        monsterX = c.c_int.from_buffer(monsterX).value
                        if monsterX == 0:
                            monsterX = savedX
                            monsterY = savedY
                            x = read_memory(0xDBFC48, base_adr, 0, procID)
                            x = c.c_int.from_buffer(x).value
                            y = read_memory(0xDBFC4C, base_adr, 0, procID)
                            y = c.c_int.from_buffer(y).value
                            x = monsterX - x
                            y = monsterY - y
                            x = 875 + x * 70
                            y = 475 + y * 70
                            click_right(x, y, game)
                            time.sleep(0.1)
                            for items in range(self.white_list.count()):
                                with lock:
                                    screenshot = win_cap.get_screenshot()
                                    item = 'Loot/'f'{self.white_list.item(items).text()}' + '.png'
                                    img = cv.imread(item)
                                    result = cv.matchTemplate(screenshot, img, cv.TM_CCOEFF_NORMED)
                                    rectangles = find_rectangle(result, img, threshold)
                                    points = find_points(rectangles)
                                    if points:
                                        points.sort()
                                        points.reverse()
                                        points = merge_close_points(points, 30)
                                        for x in points:
                                            collect_items(x[0] + 1725, x[1] + 325, self.gold_bp_x, self.gold_bp_y, game)
                                            time.sleep(0.1)
                                time.sleep(0.2)
                        time.sleep(0.01)
                    time.sleep(0.01)
                time.sleep(1)

        loot_thread = Thread(target=open_monster)
        loot_thread.daemon = True  # Daemonize the thread to terminate it when the main thread exits
        loot_thread.start()
        loot_items()

    def mouse_cords(self):
        game = win32gui.FindWindow(None, 'Medivia')
        while True:
            x, y = win32api.GetCursorPos()
            self.mouse_status.setText('x ='f"{x}"'           y = 'f'{y}')
            time.sleep(0.05)
            if win32api.GetAsyncKeyState(VK_LBUTTON) & 0x8000:
                self.set_gold_bp.setText("Success")
                self.set_gold_bp.setStyleSheet("color: green")
                self.mouse_status.setText("")
                x, y = win32gui.ScreenToClient(game, (x, y))
                self.gold_bp_x = x
                self.gold_bp_y = y
                time.sleep(5)
                self.set_gold_bp.setText("Set Gold Backpack")
                self.set_gold_bp.setStyleSheet("color: black")
                return

    def set_gold_backpack(self):
        self.set_gold_bp.setText("Left-Click on spot")
        self.set_gold_bp.setStyleSheet("color: red")
        mouse_cords_thread = Thread(target=self.mouse_cords)
        mouse_cords_thread.daemon = True  # Daemonize the thread to terminate it when the main thread exits
        mouse_cords_thread.start()
        return

    def add(self):
        selected_item = self.black_list.currentItem()
        if selected_item:
            self.white_list.addItem(self.black_list.item(self.black_list.row(selected_item)).text())

