import cv2

from funkcje import *


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

        text_label = QLabel("Targeting", self)
        text_label.setGeometry(0, 0, 100, 20)
        # text_label.setStyleSheet("color: yellow")

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

        self.follow_monster_status = QCheckBox(self)
        self.follow_monster_status.move(0, 320)
        follow_monster_status_text = QLabel("Follow Monster", self)
        follow_monster_status_text.setGeometry(17, 311, 100, 30)

        def list_monsters():
            continue_while = True
            game = win32gui.FindWindow(None, 'Medivia')
            procID = win32process.GetWindowThreadProcessId(game)
            procID = procID[1]
            process_handle = c.windll.kernel32.OpenProcess(0x1F0FFF, False, procID)
            modules = win32process.EnumProcessModules(process_handle)
            base_adr = modules[0]
            # win_cap = WindowCapture('Medivia', 1130, 840, 300, 78)
            win_cap = WindowCapture('Medivia', 675, 675, 525, 150)
            lower = np.array([9, 180, 150])
            upper = np.array([14, 190, 255])
            while True:
                if self.target_status.checkState() == 2:
                    value = read_memory(0xDBEEA8, base_adr, 0, procID)
                    value = c.c_ulonglong.from_buffer(value).value
                    if value == 0:
                        with lock:
                            img = win_cap.get_screenshot()
                        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
                        mask = cv.inRange(hsv, lower, upper)
                        output = cv.bitwise_and(img, img, mask=mask)
                        gray = cv.cvtColor(output, cv.COLOR_BGR2GRAY)
                        thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]
                        combined_list = get_text(thresh)
                        combined_list = sorted(combined_list, key=distance)
                        if combined_list:
                            for monster in combined_list:
                                for i in range(self.monster_list.count()):
                                    if monster[0] == self.monster_list.item(i).text().replace(" ", ""):
                                        click_right(monster[1] + 525, 1040 - monster[2] - 405 + 150 + 70, game)
                                        continue_while = False
                                        time.sleep(0.1)
                                        break
                                if not continue_while:
                                    continue_while = True
                                    break

        monster_thread = Thread(target=list_monsters)
        monster_thread.daemon = True  # Daemonize the thread to terminate it when the main thread exits
        monster_thread.start()

    def delete_list(self):
        selected_item = self.save_targeting_list.currentItem()
        if selected_item:
            os.remove(
                'Targeting/'f'{self.save_targeting_list.item(self.save_targeting_list.row(selected_item)).text()}.txt')
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
            f = open(
                "Targeting/"f"{self.save_targeting_list.item(self.save_targeting_list.row(selected_item)).text()}.txt")
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

