import time
import urllib
from urllib import request
from funkcje import *


class TargetTab(QWidget):
    def __init__(self, parent=None):
        super(TargetTab, self).__init__(parent)

        # Variables
        self.startLoot_checkBox = None
        self.startTarget_checkBox = None
        self.targetingProfile_line = None
        self.targetingProfile_listWidget = None
        self.monsterName_line = None
        self.targeting_listWidget = None
        self.looting_listWidget = None
        self.itemOption_line = None
        self.itemName_line = None

        self.layout = QGridLayout()
        self.setLayout(self.layout)
        # Functions
        self.groupbox1()
        self.groupbox2()
        self.groupbox3()
        self.groupbox4()
        self.addItemfromURL()

    def groupbox1(self) -> None:
        groupbox = QGroupBox("Save&&Load Targeting")
        groupbox_layout = QVBoxLayout()
        groupbox.setLayout(groupbox_layout)

        # Buttons
        saveTargetingProfile_button = QPushButton("Save")
        saveTargetingProfile_button.clicked.connect(self.saveTargetingProfile)

        loadTargetingProfile_button = QPushButton("Load")
        loadTargetingProfile_button.clicked.connect(self.loadTargetingProfile)

        deleteTargetingProfile_button = QPushButton("Del")

        # Labels
        targetingProfile_label = QLabel("Name:", self)

        # Edit Lines
        self.targetingProfile_line = QLineEdit()

        # List Widgets
        self.targetingProfile_listWidget = QListWidget(self)
        for file in os.listdir("Targeting"):
            self.targetingProfile_listWidget.addItem(f"{file.split('.')[0]}")

        # QHBox
        layout1 = QHBoxLayout()
        layout1.addWidget(targetingProfile_label)
        layout1.addWidget(self.targetingProfile_line)
        layout2 = QHBoxLayout()
        layout2.addWidget(saveTargetingProfile_button)
        layout2.addWidget(loadTargetingProfile_button)
        layout2.addWidget(deleteTargetingProfile_button)

        # Add Layouts
        groupbox_layout.addWidget(self.targetingProfile_listWidget)
        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        self.layout.addWidget(groupbox, 1, 0)
        groupbox.setFixedWidth(150)

    def groupbox2(self) -> None:
        groupbox = QGroupBox("Targeting List")
        groupbox_layout = QVBoxLayout()
        groupbox.setLayout(groupbox_layout)

        # Buttons
        left_button = QPushButton("<", self)
        left_button.setFixedWidth(20)
        left_button.clicked.connect(self.monsterUp)

        right_button = QPushButton(">", self)
        right_button.setFixedWidth(20)
        right_button.clicked.connect(self.monsterDown)

        deleteMonster_button = QPushButton("Del", self)
        deleteMonster_button.clicked.connect(self.deleteMonster)

        clearMonsterList_button = QPushButton("Clear", self)
        clearMonsterList_button.clicked.connect(self.clearMonsterList)

        # List Widgets
        self.targeting_listWidget = QListWidget(self)

        # QHBox
        layout1 = QHBoxLayout()
        layout1.addWidget(left_button)
        layout1.addWidget(right_button)
        layout1.addWidget(deleteMonster_button)
        layout1.addWidget(clearMonsterList_button)

        # Add Layouts
        groupbox_layout.addWidget(self.targeting_listWidget)
        groupbox_layout.addLayout(layout1)
        groupbox.setFixedSize(150, 250)
        self.layout.addWidget(groupbox, 0, 0)

    def groupbox3(self) -> None:
        groupbox = QGroupBox("Define Monster")
        groupbox_layout = QVBoxLayout()
        groupbox.setLayout(groupbox_layout)

        # Buttons
        addMonster_button = QPushButton("Add", self)
        addMonster_button.setFixedWidth(50)
        addMonster_button.clicked.connect(self.addMonster)

        # Check Boxes
        self.startLoot_checkBox = QCheckBox(self)
        self.startLoot_checkBox.setFixedWidth(15)
        self.startTarget_checkBox = QCheckBox(self)
        self.startTarget_checkBox.setFixedWidth(15)
        self.startTarget_checkBox.stateChanged.connect(self.createMonsterImages)

        # Labels
        targetingList_label = QLabel("Name:", self)
        startLoot_label = QLabel("Loot Monsters", self)
        startTarget_label = QLabel("Start Target", self)

        # Edit Lines
        self.monsterName_line = QLineEdit()

        # QHBox
        layout1 = QHBoxLayout()
        layout1.addWidget(targetingList_label)
        layout1.addWidget(self.monsterName_line)
        layout1.addWidget(addMonster_button)
        layout2 = QHBoxLayout()
        layout2.addWidget(self.startLoot_checkBox)
        layout2.addWidget(startLoot_label)
        layout2.addWidget(self.startTarget_checkBox)
        layout2.addWidget(startTarget_label)

        # Add Layouts
        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        groupbox.setFixedSize(200, 80)
        self.layout.addWidget(groupbox, 0, 1, alignment=Qt.AlignTop | Qt.AlignLeft)

    def groupbox4(self) -> None:
        groupbox = QGroupBox("Looting")
        groupbox_layout = QVBoxLayout()
        groupbox.setLayout(groupbox_layout)

        # Buttons
        addItem_button = QPushButton("Add", self)
        addItem_button.setFixedWidth(40)
        addItem_button.clicked.connect(self.addItem)

        deleteItem_button = QPushButton("Del", self)
        deleteItem_button.clicked.connect(self.deleteItem)
        deleteItem_button.setFixedWidth(40)

        # Edit Lines
        self.itemName_line = QLineEdit()
        self.itemOption_line = QLineEdit()
        self.itemOption_line.setFixedWidth(20)
        self.itemOption_line.setMaxLength(2)

        # List Widgets
        self.looting_listWidget = QListWidget(self)

        # QHBox
        layout1 = QHBoxLayout()
        layout1.addWidget(self.itemName_line)
        layout1.addWidget(self.itemOption_line)
        layout1.addWidget(addItem_button)
        layout1.addWidget(deleteItem_button)

        # Add Layouts
        groupbox_layout.addWidget(self.looting_listWidget)
        groupbox_layout.addLayout(layout1)
        groupbox.setFixedWidth(200)
        self.layout.addWidget(groupbox, 1, 1)

    # Add Items from url to looting_listWidget
    def addItemfromURL(self) -> None:
        tmp = 0
        f = open('Loot.txt', 'r')
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
            image1.save('Loot/'+name)
            image1 = Image.open('Loot/'+name)
            image2 = Image.open('background.png')
            image1 = image1.convert('RGBA')
            image2 = image2.convert('RGBA')
            image2.paste(image1, (0, 0), image1)
            image2.save('Loot/'+name)

    # Add Item To looting_listWidget
    def addItem(self) -> None:
        item_name = self.itemName_line.text()
        item_option = self.itemOption_line.text()
        if item_name and item_option:
            self.looting_listWidget.addItem(f"{item_name} | {item_option}")
            self.itemName_line.clear()
            self.itemOption_line.clear()

    # Delete Item from looting_listWidget
    def deleteItem(self) -> None:
        selected_item = self.looting_listWidget.currentItem()
        if selected_item:
            self.looting_listWidget.takeItem(self.looting_listWidget.row(selected_item))

    # Add Monster To targeting_listWidget
    def addMonster(self) -> None:
        monster_name = self.monsterName_line.text()
        if monster_name:
            self.targeting_listWidget.addItem(monster_name)
            self.monsterName_line.clear()

    # Delete Monster from targeting_listWidget
    def deleteMonster(self) -> None:
        selected_monster = self.targeting_listWidget.currentItem()
        if selected_monster:
            self.targeting_listWidget.takeItem(self.targeting_listWidget.row(selected_monster))

    # Clear Monster List in  targeting_listWidget
    def clearMonsterList(self) -> None:
        self.targeting_listWidget.clear()

    def monsterDown(self) -> None:
        selected = self.targeting_listWidget.currentRow()
        if 0 <= selected < self.targeting_listWidget.count() - 1:
            monster_name = self.targeting_listWidget.item(selected).text()
            self.targeting_listWidget.item(selected).setText(self.targeting_listWidget.item(selected+1).text())
            self.targeting_listWidget.item(selected + 1).setText(monster_name)
            self.targeting_listWidget.setCurrentRow(selected + 1)

    def monsterUp(self) -> None:
        selected = self.targeting_listWidget.currentRow()
        if selected > 0:
            monster_name = self.targeting_listWidget.item(selected).text()
            self.targeting_listWidget.item(selected).setText(self.targeting_listWidget.item(selected - 1).text())
            self.targeting_listWidget.item(selected - 1).setText(monster_name)
            self.targeting_listWidget.setCurrentRow(selected - 1)

    # Add Target Profile To targetingProfile_listWidget
    def saveTargetingProfile(self) -> None:
        profile_name = self.targetingProfile_line.text()
        if profile_name:
            f = open("Targeting/"f"{profile_name}.txt", "w")
            [f.write(f'{self.targeting_listWidget.item(i).text()}\n') for i in range(self.targeting_listWidget.count())]
            f.close()
            f = open("Looting/"f"{profile_name}.txt", "w")
            [f.write(f'{self.looting_listWidget.item(i).text()}\n') for i in range(self.looting_listWidget.count())]
            f.close()
            self.targetingProfile_listWidget.addItem(profile_name)
            self.targetingProfile_line.clear()

    # Load Target Profile To targeting_listWidget
    def loadTargetingProfile(self) -> None:
        self.targeting_listWidget.clear()
        selected_item = self.targetingProfile_listWidget.currentItem().text()
        if selected_item:
            f = open(
                "Targeting/"f"{selected_item}.txt")
            for monster in f:
                if monster != '\n':
                    self.targeting_listWidget.addItem(monster.split("\n")[0])
            f.close()
            f = open(
                "Looting/"f"{selected_item}.txt")
            for item in f:
                if item != '\n':
                    self.looting_listWidget.addItem(item.split("\n")[0])
            f.close()

    # Create an Image from monster names
    def createMonsterImages(self) -> None:
        fnt = ImageFont.truetype("./Tahoma.ttf", 15)
        background_color = (0, 0, 0)
        if self.startTarget_checkBox.checkState() == 2:
            for i in range(0, self.targeting_listWidget.count()):
                image = Image.new('RGB', (8*len(self.targeting_listWidget.item(i).text()), 20), background_color)
                draw = ImageDraw.Draw(image)
                draw.multiline_text((0, 0), self.targeting_listWidget.item(i).text(), font=fnt, fill=(219, 127, 62))
                opencv_image = cv.cvtColor(np.array(image), cv.COLOR_RGB2BGR)
                cv.imwrite('Monsters/'+self.targeting_listWidget.item(i).text()+'.png', opencv_image)
            thread = Thread(target=self.attackMonsters)
            thread.daemon = True
            thread.start()

    # Target monsters
    def attackMonsters(self) -> None:
        win_cap_target = WindowCapture('Medivia - ' + nickname, 675, 675, 525, 150)
        win_cap_loot = WindowCapture('Medivia - ' + nickname, 190, 680, 1730, 350)
        bgr_color = np.uint8([[[138, 148, 255]]])
        hsv_color = cv.cvtColor(bgr_color, cv.COLOR_BGR2HSV)
        lower = np.array([hsv_color[0][0][0] - 10, 180, 145])
        upper = np.array([hsv_color[0][0][0] + 10, 185, 255])
        loot = 0
        timer = 0
        savedX = 0
        savedY = 0
        while self.startTarget_checkBox.checkState() == 2:
            for monster_index in range(self.targeting_listWidget.count()):
                monster_name = self.targeting_listWidget.item(monster_index).text()
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
                            click_right(int(monsterX) + 545, int(monsterY) + 180)
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
                            x = read_memory(my_x, 0)
                            x = c.c_int.from_buffer(x).value
                            y = read_memory(my_y, 0)
                            y = c.c_int.from_buffer(y).value
                            x = savedX - x
                            y = savedY - y
                            x = 855 + x * 70
                            y = 460 + y * 70
                            click_right(x, y)
                            time.sleep(0.2)
                            for _ in range(0, 2):
                                for item_index in range(0, self.looting_listWidget.count()):
                                    item_name = self.looting_listWidget.item(item_index).text().split('|')[0][:-1]
                                    option = self.looting_listWidget.item(item_index).text().split('|')[1][1:]
                                    file_name = [x for x in os.listdir('Loot/') if x.split('.')[0] == item_name]
                                    if '.png' in file_name[0]:
                                        screenshot = win_cap_loot.get_screenshot()
                                        template = cv.imread('Loot/'f'{item_name}' + '.png')
                                        result = cv.matchTemplate(screenshot, template, cv.TM_CCOEFF_NORMED)
                                        locations = list(zip(*(np.where(result >= 0.85))[::-1]))
                                        locations = merge_close_points(locations, 15)
                                        locations = sorted(locations, key=lambda point: (point[1], point[0]), reverse=True)
                                        for x, y in locations:
                                            if option == 'u':
                                                click_right(int(x) + 1740, int(y) + 336)
                                                time.sleep(0.15)
                                            else:
                                                collect_items(int(x) + 1740, int(y) + 336, 1630, 340)
                                                time.sleep(0.15)
                                    elif file_name:
                                        for item_name in os.listdir('Loot/' + file_name[0]):
                                            screenshot = win_cap_loot.get_screenshot()
                                            template = cv.imread('Loot/'f'{file_name[0]}''/' + item_name)
                                            result = cv.matchTemplate(screenshot, template, cv.TM_CCOEFF_NORMED)
                                            locations = list(zip(*(np.where(result >= 0.85))[::-1]))
                                            locations = merge_close_points(locations, 15)
                                            locations = sorted(locations, key=lambda point: (point[1], point[0]), reverse=True)
                                            for x, y in locations:
                                                if option == 'u':
                                                    click_right(int(x) + 1740, int(y) + 336)
                                                    time.sleep(0.15)
                                                else:
                                                    collect_items(int(x) + 1740, int(y) + 336, 1680, 350)
                                                    time.sleep(0.15)
                time.sleep(0.1)

