import cv2

from Functions import *


class GeneralTab(QWidget):
    def __init__(self, parent=None):
        super(GeneralTab, self).__init__(parent)
        # Variables
        # Check Boxes
        self.startLoot_checkBox = QCheckBox("Loot Monsters", self)
        self.startTarget_checkBox = QCheckBox("Run Targeting", self)

        # Combo Boxes
        self.runeList_comboBox = QComboBox(self)
        self.attackDist_comboBox = QComboBox(self)

        # Line Edits
        self.generalProfile_line = QLineEdit(self)
        self.monsterName_line = QLineEdit(self)
        self.itemName_line = QLineEdit(self)
        self.itemOption_line = QLineEdit(self)
        self.itemOption_line.setFixedWidth(20)
        self.itemOption_line.setMaxLength(2)
        self.hpFrom_line = QLineEdit(self)
        self.hpTo_line = QLineEdit(self)
        self.hpFrom_line.setMaxLength(3)
        self.hpTo_line.setMaxLength(2)

        # List Widgets
        self.generalProfile_listWidget = QListWidget(self)
        self.targetList_listWidget = QListWidget(self)
        self.looting_listWidget = QListWidget(self)

        # Layouts
        self.layout = QGridLayout(self)
        self.setLayout(self.layout)

        # Init View
        self.targetList()
        self.save_load()
        self.target()
        self.looting()
        self.start()

    def targetList(self) -> None:
        groupbox = QGroupBox("Targeting List", self)
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Buttons
        deleteMonster_button = QPushButton("Del", self)
        clearMonsters_button = QPushButton("Clear", self)

        # Buttons Functions
        deleteMonster_button.clicked.connect(self.deleteMonster)
        clearMonsters_button.clicked.connect(self.clearMonsterList)

        # QHBox
        layout1 = QHBoxLayout(self)

        # Add Widgets
        layout1.addWidget(deleteMonster_button)
        layout1.addWidget(clearMonsters_button)

        # Add Layouts
        groupbox_layout.addWidget(self.targetList_listWidget)
        groupbox_layout.addLayout(layout1)
        groupbox.setFixedSize(150, 250)
        self.layout.addWidget(groupbox, 0, 0, 2, 1)

    def save_load(self) -> None:
        groupbox = QGroupBox("Save&&Load Targeting", self)
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Buttons
        saveProfile_button = QPushButton("Save", self)
        loadProfile_button = QPushButton("Load", self)

        # Buttons Functions
        saveProfile_button.clicked.connect(self.saveProfile)
        loadProfile_button.clicked.connect(self.loadProfile)

        # List Widgets
        for file in os.listdir("Targeting"):
            self.generalProfile_listWidget.addItem(f"{file.split('.')[0]}")

        # QHBox
        layout1 = QHBoxLayout(self)
        layout2 = QHBoxLayout(self)

        # Add Widgets
        layout1.addWidget(QLabel("Name:", self))
        layout1.addWidget(self.generalProfile_line)
        layout2.addWidget(saveProfile_button)
        layout2.addWidget(loadProfile_button)

        # Add Layouts
        groupbox_layout.addWidget(self.generalProfile_listWidget)
        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        groupbox.setFixedWidth(150)
        self.layout.addWidget(groupbox, 2, 0)

    def target(self) -> None:
        groupbox = QGroupBox("Define Monster", self)
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Buttons
        addMonster_button = QPushButton("Add", self)
        addMonster_button.setFixedWidth(50)

        # Buttons Functions
        addMonster_button.clicked.connect(self.addMonster)

        # Check Boxes Functions
        self.startTarget_checkBox.stateChanged.connect(self.createMonsterImages)

        # Combo Boxes
        self.runeList_comboBox.addItem("")
        self.runeList_comboBox.addItem("HMM")
        self.runeList_comboBox.addItem("GFB")
        self.runeList_comboBox.addItem("SD")
        self.attackDist_comboBox.addItem("")
        self.attackDist_comboBox.addItem("1")
        self.attackDist_comboBox.addItem("2")
        self.attackDist_comboBox.addItem("3")
        self.attackDist_comboBox.addItem("4")
        self.attackDist_comboBox.addItem("5")

        # QHBox
        layout1 = QHBoxLayout(self)
        layout2 = QHBoxLayout(self)
        layout3 = QHBoxLayout(self)
        layout4 = QHBoxLayout(self)

        # Add Widgets
        layout1.addWidget(self.monsterName_line)
        layout1.addWidget(addMonster_button)
        layout2.addWidget(QLabel("Attack Distance:", self))
        layout2.addWidget(self.attackDist_comboBox)
        layout3.addWidget(QLabel("Use Rune:", self))
        layout3.addWidget(self.runeList_comboBox)
        layout4.addWidget(QLabel("From:", self))
        layout4.addWidget(self.hpFrom_line)
        layout4.addWidget(QLabel("% To:", self))
        layout4.addWidget(self.hpTo_line)
        layout4.addWidget(QLabel("%", self))

        # Add Layouts
        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        groupbox_layout.addLayout(layout3)
        groupbox_layout.addLayout(layout4)
        self.layout.addWidget(groupbox, 0, 1, 1, 1)

    def start(self):
        groupbox = QGroupBox("Start")
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # QHBox
        layout1 = QHBoxLayout(self)
        layout2 = QHBoxLayout(self)

        # Add Widgets
        layout1.addWidget(self.startLoot_checkBox)
        layout2.addWidget(self.startTarget_checkBox)

        # Add Layouts
        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        self.layout.addWidget(groupbox, 1, 1, 1, 1)

    def looting(self) -> None:
        groupbox = QGroupBox("Looting")
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Buttons
        addItem_button = QPushButton("Add", self)
        deleteItem_button = QPushButton("Del", self)

        addItem_button.setFixedWidth(40)
        deleteItem_button.setFixedWidth(40)

        # Buttons Functions
        addItem_button.clicked.connect(self.addItem)
        deleteItem_button.clicked.connect(self.deleteItem)

        # QHBox
        layout1 = QHBoxLayout(self)

        # Add Widgets
        layout1.addWidget(self.itemName_line)
        layout1.addWidget(self.itemOption_line)
        layout1.addWidget(addItem_button)
        layout1.addWidget(deleteItem_button)

        # Add Layouts
        groupbox_layout.addWidget(self.looting_listWidget)
        groupbox_layout.addLayout(layout1)
        self.layout.addWidget(groupbox, 2, 1)

    def addItem(self) -> None:
        item_name = self.itemName_line.text()
        for index in range(self.looting_listWidget.count()):
            if item_name == self.looting_listWidget.item(index).text().split(' |')[0]:
                self.itemName_line.clear()
                self.itemOption_line.clear()
                return
        item_option = self.itemOption_line.text()
        if item_name and item_option:
            self.looting_listWidget.addItem(f"{item_name} | {item_option}")
            self.itemName_line.clear()
            self.itemOption_line.clear()

    def deleteItem(self) -> None:
        selected_item = self.looting_listWidget.currentItem()
        if selected_item:
            self.looting_listWidget.takeItem(self.looting_listWidget.row(selected_item))

    def addMonster(self) -> None:
        monster_name = self.monsterName_line.text()
        for index in range(self.targetList_listWidget.count()):
            if monster_name == self.targetList_listWidget.item(index).text().split(' | ')[0]:
                self.monsterName_line.clear()
                return
        if monster_name:
            if self.attackDist_comboBox.currentText():
                monster_name += ' | ' + self.attackDist_comboBox.currentText()
            if self.runeList_comboBox.currentText() and self.hpFrom_line.text() and self.hpTo_line.text():
                monster_name += ' | ' + self.runeList_comboBox.currentText() + ' ' + self.hpFrom_line.text() + '-' + self.hpTo_line.text()
            self.runeList_comboBox.setCurrentIndex(0)
            self.attackDist_comboBox.setCurrentIndex(0)
            self.monsterName_line.clear()
            self.hpFrom_line.clear()
            self.hpTo_line.clear()
            self.targetList_listWidget.addItem(monster_name)

    def deleteMonster(self) -> None:
        selected_monster = self.targetList_listWidget.currentItem()
        if selected_monster:
            self.targetList_listWidget.takeItem(self.targetList_listWidget.row(selected_monster))

    def clearMonsterList(self) -> None:
        self.targetList_listWidget.clear()

    def saveProfile(self) -> None:
        profile_name = self.generalProfile_line.text()
        if profile_name:
            f = open("Targeting/"f"{profile_name}.txt", "w")
            [f.write(f'{self.targetList_listWidget.item(i).text()}\n') for i in
             range(self.targetList_listWidget.count())]
            f.close()
            f = open("Looting/"f"{profile_name}.txt", "w")
            [f.write(f'{self.looting_listWidget.item(i).text()}\n') for i in range(self.looting_listWidget.count())]
            f.close()
            self.generalProfile_listWidget.addItem(profile_name)
            self.generalProfile_line.clear()

    def loadProfile(self) -> None:
        self.targetList_listWidget.clear()
        self.looting_listWidget.clear()
        selected_item = self.generalProfile_listWidget.currentItem().text()
        if selected_item:
            f = open(
                "Targeting/"f"{selected_item}.txt")
            for monster in f:
                if monster != '\n':
                    self.targetList_listWidget.addItem(monster.split("\n")[0])
            f.close()
            f = open(
                "Looting/"f"{selected_item}.txt")
            for item in f:
                if item != '\n':
                    self.looting_listWidget.addItem(item.split("\n")[0])
            f.close()

    def createMonsterImages(self) -> None:
        fnt = ImageFont.truetype("./Tahoma.ttf", 15)
        background_color = (0, 0, 0)
        if self.startTarget_checkBox.checkState() == 2:
            for i in range(0, self.targetList_listWidget.count()):
                image = Image.new('RGB', (8 * len(self.targetList_listWidget.item(i).text()), 20), background_color)
                draw = ImageDraw.Draw(image)
                draw.multiline_text((0, 0), self.targetList_listWidget.item(i).text(), font=fnt, fill=(219, 127, 62))
                opencv_image = cv.cvtColor(np.array(image), cv.COLOR_RGB2BGR)
                cv.imwrite('Monsters/' + self.targetList_listWidget.item(i).text() + '.png', opencv_image)
            thread = Thread(target=self.attackMonsters)
            thread.daemon = True
            thread.start()

    # Target monsters
    def attackMonsters(self) -> None:
        win_cap_target = WindowCapture('Medivia - ' + nickname, screenWidth[0] - screenX[0],
                                       screenHeight[0] - screenY[0], screenX[0] + 10, screenY[0] + 25)
        win_cap_loot = WindowCapture('Medivia - ' + nickname, screenWidth[1] - screenX[1],
                                     screenHeight[1] - screenY[1], screenX[1], screenY[1])
        bgr_color = np.uint8([[[138, 148, 255]]])
        hsv_color = cv.cvtColor(bgr_color, cv.COLOR_BGR2HSV)
        lower = np.array([hsv_color[0][0][0] - 10, 180, 145])
        upper = np.array([hsv_color[0][0][0] + 10, 185, 255])
        loot = 0
        timer = 0
        savedX = 0
        savedY = 0
        while self.startTarget_checkBox.checkState() == 2:
            for monster_index in range(self.targetList_listWidget.count()):
                monster = self.targetList_listWidget.item(monster_index).text()
                count = 0
                monsterHp = ''
                monsterHpFrom = 0
                monsterHpTo = 0
                for i in monster:
                    if i == '|':
                        count = count + 1
                monster_name = monster.split(' | ')[0]
                if count > 0:
                    monster_dist = monster.split(' | ')[1]
                    if count > 1:
                        monster_dist = int(monster_dist)
                        monster_rune = monster.split(' | ')[2]
                        monsterHp = monster_rune.split(' ')[1]
                        monster_rune = monster_rune.split(' ')[0]
                        monsterHpFrom = int(monsterHp.split('-')[0])
                        monsterHpTo = int(monsterHp.split('-')[1])
                    elif len(monster_dist) > 1 and count == 1:
                        monster_rune = monster.split(' | ')[1]
                        monsterHp = monster_rune.split(' ')[1]
                        monster_rune = monster_rune.split(' ')[0]
                        monsterHpFrom = int(monsterHp.split('-')[0])
                        monsterHpTo = int(monsterHp.split('-')[1])
                        monster_dist = 0
                    else:
                        monster_dist = int(monster_dist)
                if [x for x in os.listdir('Monsters/') if x.split('.')[0] == monster_name]:
                    img = win_cap_target.get_screenshot()
                    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
                    mask = cv.inRange(hsv, lower, upper)
                    result = cv.bitwise_and(img, img, mask=mask)
                    template = cv.imread('Monsters/'f'{monster_name}' + '.png')
                    result = cv.matchTemplate(result, template, cv.TM_CCOEFF_NORMED)
                    locations = list(zip(*(np.where(result >= 0.5)[::-1])))
                    if locations:
                        locations = merge_close_points(locations, 10)
                        locations = sorted(locations, key=sort_monsters_by_distance)
                        monsterX, monsterY = locations[0]
                        targetID = read_memory(attack, 0)
                        targetID = c.c_ulonglong.from_buffer(targetID).value
                        if not targetID:
                            click_right(int(monsterX) + screenX[0] + int((screenWidth[0] - screenX[0]) / 22),
                                        int(monsterY) + screenY[0] + int((screenHeight[0] - screenY[0]) / 9))
                        while targetID:
                            loot = 1
                            targetID = read_memory(attack, 0)
                            targetID = c.c_ulonglong.from_buffer(targetID).value
                            savedX = monsterX
                            savedY = monsterY
                            monsterY = read_memory(targetID - base_adr, 0x3C)
                            monsterY = c.c_int.from_buffer(monsterY).value
                            monsterX = read_memory(targetID - base_adr, 0x38)
                            monsterX = c.c_int.from_buffer(monsterX).value
                            if 15 <= timer:
                                timer = 0
                                win32gui.SendMessage(game, win32con.WM_KEYDOWN, win32con.VK_ESCAPE, 0x01480001)
                                win32gui.SendMessage(game, win32con.WM_KEYUP, win32con.VK_ESCAPE, 0x01480001)
                                break
                            timer += 0.1
                            time.sleep(0.1)
                        if loot and self.startLoot_checkBox.checkState() == 2:
                            timer = 0
                            loot = 0
                            x = read_memory(myX, 0)
                            x = c.c_int.from_buffer(x).value
                            y = read_memory(myY, 0)
                            y = c.c_int.from_buffer(y).value
                            x = savedX - x
                            y = savedY - y
                            box = int((screenWidth[0] - screenX[0])/15.5)
                            x = int((screenWidth[0] + screenX[0] + 10) / 2) + x * box
                            y = int((screenHeight[0] + screenY[0] + 25) / 2) + y * box
                            containers = read_pointer(containerPtr, containerOffset)
                            containers = c.c_int.from_buffer(containers).value
                            tmp = read_pointer(containerPtr, containerOffset)
                            tmp = c.c_int.from_buffer(tmp).value
                            while tmp == containers:
                                click_right(x, y)
                                time.sleep(0.2)
                                tmp = read_pointer(containerPtr, containerOffset)
                                tmp = c.c_int.from_buffer(tmp).value
                            for _ in range(0, 2):
                                for item_index in range(0, self.looting_listWidget.count()):
                                    item_name = self.looting_listWidget.item(item_index).text().split('|')[0][:-1]
                                    option = self.looting_listWidget.item(item_index).text().split('|')[1][1:]
                                    file_name = [x for x in os.listdir('Loot/') if x.split('.')[0] == item_name]
                                    screenshot = win_cap_loot.get_screenshot()
                                    if file_name:
                                        if '.png' in file_name[0]:
                                            template = cv.imread('Loot/'f'{item_name}' + '.png')
                                            result = cv.matchTemplate(screenshot, template, cv.TM_CCOEFF_NORMED)
                                            locations = list(zip(*(np.where(result >= 0.85))[::-1]))
                                            locations = merge_close_points(locations, 15)
                                            locations = sorted(locations, key=lambda point: (point[1], point[0]), reverse=True)
                                            locations = [[int(x), int(y)] for x, y in locations]
                                            for x, y in locations:
                                                if 'c' in option or option == 'c':
                                                    index = 0
                                                    if len(option) > 1:
                                                        index = int(option[1])
                                                    collect_items(x + screenX[1], y + screenY[1], bpX[index], bpY[index])
                                                    time.sleep(0.15)
                                        else:
                                            for item_name in os.listdir('Loot/' + file_name[0]):
                                                template = cv.imread('Loot/'f'{file_name[0]}''/' + item_name)
                                                result = cv.matchTemplate(screenshot, template, cv.TM_CCOEFF_NORMED)
                                                locations = list(zip(*(np.where(result >= 0.85))[::-1]))
                                                locations = merge_close_points(locations, 15)
                                                locations = sorted(locations, key=lambda point: (point[1], point[0]), reverse=True)
                                                locations = [[int(x), int(y)] for x, y in locations]
                                                for x, y in locations:
                                                    if 'c' in option or option == 'c':
                                                        index = 0
                                                        if len(option) > 1:
                                                            index = int(option[1])
                                                        collect_items(x + screenX[1], y + screenY[1], bpX[index], bpY[index])
                                                        time.sleep(0.15)
                time.sleep(0.1)
