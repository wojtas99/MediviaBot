import json
import time

import cv2
import win32gui

from Functions import *


class TargetLootTab(QWidget):
    def __init__(self, parent=None):
        super(TargetLootTab, self).__init__(parent)
        # Load Icon
        self.setWindowIcon(QIcon('Icon.jpg'))

        # Set Title and Size
        self.setWindowTitle("Targeting")
        self.setFixedSize(350, 400)
        # Variables
        # Check Boxes
        self.startLoot_checkBox = QCheckBox("Open Corpses", self)
        self.startTarget_checkBox = QCheckBox("Start Targeting", self)

        # Combo Boxes
        self.runeList_comboBox = QComboBox(self)
        self.attackDist_comboBox = QComboBox(self)

        # Line Edits
        self.targetLootProfile_lineEdit = QLineEdit(self)
        self.targetName_lineEdit = QLineEdit(self)
        self.itemName_lineEdit = QLineEdit(self)
        self.lootOption_lineEdit = QLineEdit(self)
        self.lootOption_lineEdit.setFixedWidth(20)
        self.lootOption_lineEdit.setMaxLength(2)
        self.hpFrom_lineEdit = QLineEdit(self)
        self.hpTo_lineEdit = QLineEdit(self)
        self.hpFrom_lineEdit.setMaxLength(3)
        self.hpTo_lineEdit.setMaxLength(2)

        # List Widgets
        self.targetLootProfile_listWidget = QListWidget(self)
        self.targetList_listWidget = QListWidget(self)
        self.lootList_listWidget = QListWidget(self)

        # Layouts
        self.layout = QGridLayout(self)
        self.setLayout(self.layout)

        # Init View
        self.targetList()
        self.saveLoadTargetLoot()
        self.setTarget()
        self.lootList()
        self.startTargetLoot()

    def targetList(self) -> None:
        groupbox = QGroupBox("Target List", self)
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Buttons
        deleteTarget_button = QPushButton("Del", self)
        clearTargets_button = QPushButton("Clear", self)

        # Buttons Functions
        deleteTarget_button.clicked.connect(self.deleteTarget)
        clearTargets_button.clicked.connect(self.clearTargetsList)

        # QHBox
        layout1 = QHBoxLayout(self)

        # Add Widgets
        layout1.addWidget(deleteTarget_button)
        layout1.addWidget(clearTargets_button)

        # Add Layouts
        groupbox_layout.addWidget(self.targetList_listWidget)
        groupbox_layout.addLayout(layout1)
        self.layout.addWidget(groupbox, 0, 0, 2, 1)

    def saveLoadTargetLoot(self) -> None:
        groupbox = QGroupBox("Save&&Load", self)
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Buttons
        saveTargetLoot_button = QPushButton("Save", self)
        loadTargetLoot_button = QPushButton("Load", self)

        # Buttons Functions
        saveTargetLoot_button.clicked.connect(self.saveTargetLoot)
        loadTargetLoot_button.clicked.connect(self.loadTargetLoot)

        # List Widgets
        for file in os.listdir("Targeting"):
            self.targetLootProfile_listWidget.addItem(f"{file.split('.')[0]}")
        # QHBox
        layout1 = QHBoxLayout(self)
        layout2 = QHBoxLayout(self)

        # Add Widgets
        layout1.addWidget(QLabel("Name:", self))
        layout1.addWidget(self.targetLootProfile_lineEdit)
        layout2.addWidget(saveTargetLoot_button)
        layout2.addWidget(loadTargetLoot_button)

        # Add Layouts
        groupbox_layout.addWidget(self.targetLootProfile_listWidget)
        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        self.layout.addWidget(groupbox, 2, 0)

    def setTarget(self) -> None:
        groupbox = QGroupBox("Define Target", self)
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Buttons
        addTarget_button = QPushButton("Add", self)
        addTarget_button.setFixedWidth(50)

        # Buttons Functions
        addTarget_button.clicked.connect(self.addTarget)

        # Check Boxes Functions
        self.startTarget_checkBox.stateChanged.connect(self.createTargetImages)

        # Combo Boxes
        self.runeList_comboBox.addItem("NoRune")
        self.runeList_comboBox.addItem("HMM")
        self.runeList_comboBox.addItem("GFB")
        self.runeList_comboBox.addItem("SD")
        self.attackDist_comboBox.addItem("All")
        self.attackDist_comboBox.addItem("1")
        self.attackDist_comboBox.addItem("2")
        self.attackDist_comboBox.addItem("3")
        self.attackDist_comboBox.addItem("4")
        self.attackDist_comboBox.addItem("5")

        # Combo Boxes Functions
        self.runeList_comboBox.currentIndexChanged.connect(self.runeListChange)

        # Line Edit
        self.hpFrom_lineEdit.setEnabled(False)
        self.hpTo_lineEdit.setEnabled(False)

        # QHBox
        layout1 = QHBoxLayout(self)
        layout2 = QHBoxLayout(self)
        layout3 = QHBoxLayout(self)
        layout4 = QHBoxLayout(self)

        # Add Widgets
        layout1.addWidget(self.targetName_lineEdit)
        layout1.addWidget(addTarget_button)
        layout2.addWidget(QLabel("Attack Distance:", self))
        layout2.addWidget(self.attackDist_comboBox)
        layout3.addWidget(QLabel("Use Rune:", self))
        layout3.addWidget(self.runeList_comboBox)
        layout4.addWidget(QLabel("From:", self))
        layout4.addWidget(self.hpFrom_lineEdit)
        layout4.addWidget(QLabel("% To:", self))
        layout4.addWidget(self.hpTo_lineEdit)
        layout4.addWidget(QLabel("%", self))

        # Add Layouts
        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        groupbox_layout.addLayout(layout3)
        groupbox_layout.addLayout(layout4)
        self.layout.addWidget(groupbox, 0, 1, 1, 1)

    def startTargetLoot(self):
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

    def lootList(self) -> None:
        groupbox = QGroupBox("Loot List")
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
        layout1.addWidget(self.itemName_lineEdit)
        layout1.addWidget(self.lootOption_lineEdit)
        layout1.addWidget(addItem_button)
        layout1.addWidget(deleteItem_button)

        # Add Layouts
        groupbox_layout.addWidget(self.lootList_listWidget)
        groupbox_layout.addLayout(layout1)
        self.layout.addWidget(groupbox, 2, 1)

    def runeListChange(self, index):
        if index != 0:
            self.hpTo_lineEdit.setEnabled(True)
            self.hpFrom_lineEdit.setEnabled(True)
        else:
            self.hpFrom_lineEdit.setEnabled(False)
            self.hpTo_lineEdit.setEnabled(False)

    def addItem(self) -> None:
        itemName = self.itemName_lineEdit.text()
        lootContainer = self.lootOption_lineEdit.text()
        if itemName and lootContainer:
            for index in range(self.lootList_listWidget.count()):
                if itemName.upper() == self.lootList_listWidget.item(index).text().upper():
                    return
            itemData = {"Loot": int(lootContainer)}
            item = QListWidgetItem(itemName)
            item.setData(Qt.UserRole, itemData)
            self.itemName_lineEdit.clear()
            self.lootOption_lineEdit.clear()
            self.lootList_listWidget.addItem(item)

    def deleteItem(self) -> None:
        selected_item = self.lootList_listWidget.currentItem()
        if selected_item:
            self.lootList_listWidget.takeItem(self.lootList_listWidget.row(selected_item))

    def addTarget(self) -> None:
        monsterName = self.targetName_lineEdit.text()
        for index in range(self.targetList_listWidget.count()):
            if monsterName.upper() == self.targetList_listWidget.item(index).text().split(' | ')[0].upper():
                return
        monsterData = {"Distance": self.attackDist_comboBox.currentText(),
                        "Rune": self.runeList_comboBox.currentText(),
                        "HpFrom": self.hpFrom_lineEdit.text(), "HpTo": self.hpTo_lineEdit.text()}
        monster = QListWidgetItem(monsterName)
        if monsterData['Distance'] == 'All':
            monsterData['Distance'] = 0
        if monsterData['HpFrom'] == '':
            monsterData['HpFrom'] = 0
        if monsterData['HpTo'] == '':
            monsterData['HpTo'] = 0
        if monsterData['Rune'] == 'HMM':
            monsterData['Rune'] = 5
        if monsterData['Rune'] == 'SD':
            monsterData['Rune'] = 6
        if monsterData['Rune'] == 'GFB':
            monsterData['Rune'] = 7
        if monsterData['Rune'] == 'NoRune':
            monsterData['Rune'] = 0
        monster.setData(Qt.UserRole, monsterData)
        self.runeList_comboBox.setCurrentIndex(0)
        self.attackDist_comboBox.setCurrentIndex(0)
        self.targetName_lineEdit.clear()
        self.hpFrom_lineEdit.clear()
        self.hpTo_lineEdit.clear()
        self.targetList_listWidget.addItem(monster)

    def deleteTarget(self) -> None:
        selected_monster = self.targetList_listWidget.currentItem()
        if selected_monster:
            self.targetList_listWidget.takeItem(self.targetList_listWidget.row(selected_monster))

    def clearTargetsList(self) -> None:
        self.targetList_listWidget.clear()

    def saveTargetLoot(self) -> None:
        targetLootName = self.targetLootProfile_lineEdit.text()
        for index in range(self.targetLootProfile_listWidget.count()):
            if targetLootName.upper() == self.targetLootProfile_listWidget.item(index).text().upper():
                return
        if targetLootName:
            targetList = []
            for i in range(self.targetList_listWidget.count()):
                item = self.targetList_listWidget.item(i)
                targetName = item.text()
                targetData = item.data(Qt.UserRole)
                targetList.append({"name": targetName, "data": targetData})
            with open(f"Targeting/{targetLootName}.json", "w") as f:
                json.dump(targetList, f, indent=4)
            lootingList = []
            for i in range(self.lootList_listWidget.count()):
                item = self.lootList_listWidget.item(i)
                itemName = item.text()
                itemData = item.data(Qt.UserRole)
                lootingList.append({"name": itemName, "data": itemData})
            with open(f"Looting/{targetLootName}.json", "w") as f:
                json.dump(lootingList, f, indent=4)
            self.targetLootProfile_listWidget.addItem(targetLootName)
            self.targetLootProfile_lineEdit.clear()

    def loadTargetLoot(self) -> None:
        targetLootName = self.targetLootProfile_listWidget.currentItem().text()
        if targetLootName:
            with open(f"Targeting/{targetLootName}.json", "r") as f:
                targetList = json.load(f)
                self.targetList_listWidget.clear()
                for entry in targetList:
                    targetName = entry["name"]
                    targetData = entry["data"]
                    target = QListWidgetItem(targetName)
                    target.setData(Qt.UserRole, targetData)
                    self.targetList_listWidget.addItem(target)
            with open(f"Looting/{targetLootName}.json", "r") as f:
                lootList = json.load(f)
                self.lootList_listWidget.clear()
                for entry in lootList:
                    itemName = entry["name"]
                    itemData = entry["data"]
                    item = QListWidgetItem(itemName)
                    item.setData(Qt.UserRole, itemData)
                    self.lootList_listWidget.addItem(item)
            self.targetLootProfile_lineEdit.setText(targetLootName)

    def createTargetImages(self) -> None:
        fnt = ImageFont.truetype("./Tahoma.ttf", 15) # Load Font
        backgroundColor = (0, 0, 0)
        if self.startTarget_checkBox.checkState() == 2:
            for i in range(0, self.targetList_listWidget.count()):
                image = Image.new('RGB', (8 * len(self.targetList_listWidget.item(i).text()), 20), backgroundColor)
                draw = ImageDraw.Draw(image)
                draw.multiline_text((0, 0), self.targetList_listWidget.item(i).text(), font=fnt, fill=(219, 127, 62))
                opencvImage = cv.cvtColor(np.array(image), cv.COLOR_RGB2BGR)
                cv.imwrite('TargetImages/' + self.targetList_listWidget.item(i).text() + '.png', opencvImage)
            thread = Thread(target=self.startAttackLoot_Thread)
            thread.daemon = True
            thread.start()

    # Target monsters
    def startAttackLoot_Thread(self) -> None:
        wincapTarget = WindowCapture('Medivia - ' + nickname, screenWidth[0] - screenX[0], screenHeight[0] - screenY[0], screenX[0] + 10, screenY[0] + 25)
        wincapLoot = WindowCapture('Medivia - ' + nickname, screenWidth[1] - screenX[1], screenHeight[1] - screenY[1], screenX[1], screenY[1])
        hsvColor = cv.cvtColor(np.uint8([[[138, 148, 255]]]), cv.COLOR_BGR2HSV)
        lowerFilter = np.array([hsvColor[0][0][0] - 10, 180, 145])
        upperFilter = np.array([hsvColor[0][0][0] + 10, 185, 255])
        sqmSize = int((screenWidth[0] - screenX[0]) / 15.5)
        characterX = int(sqmSize*7.5 + screenX[0])
        characterY = int(sqmSize*5.5 + screenY[0]) + 20
        offsetX = int(sqmSize * 0.5)
        offsetY = int(sqmSize * 0.6)
        while self.startTarget_checkBox.checkState() == 2:
            for targetIndex in range(self.targetList_listWidget.count()):
                targetName = self.targetList_listWidget.item(targetIndex).text()
                targetData = self.targetList_listWidget.item(targetIndex).data(Qt.UserRole)
                targetDist = int(targetData['Distance'])
                targetRune = int(targetData['Rune'])
                targetHpFrom = int(targetData['HpFrom'])
                targetHpTo = int(targetData['HpTo'])
                if [x for x in os.listdir('TargetImages/') if x.split('.')[0] == targetName]:
                    img = wincapTarget.get_screenshot()
                    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
                    mask = cv.inRange(hsv, lowerFilter, upperFilter)
                    result = cv.bitwise_and(img, img, mask=mask)
                    loadedImage = cv.imread('TargetImages/'f'{targetName}' + '.png')
                    result = cv.matchTemplate(result, loadedImage, cv.TM_CCOEFF_NORMED)
                    locations = list(zip(*(np.where(result >= 0.5)[::-1])))
                    if locations:
                        loot = 0
                        locations = mergeClosePoints(locations, 10)
                        locations = [(int(x) + screenX[0], int(y) + screenY[0] + 25) for x, y in locations]
                        locations = sorted(locations, key=lambda point: sortMonstersByDist(point, characterX, characterY))
                        targetID = c.c_ulonglong.from_buffer(readMemory(attack, 0)).value
                        if targetID == 0:
                            targetX, targetY = locations[0]
                            targetX += offsetX
                            targetY += offsetY
                            if (targetDist != 0 and abs(targetX - characterX) < targetDist * (sqmSize + 25)
                                    and abs(targetY - characterY) < targetDist * (sqmSize + 25)):
                                rightClick(targetX, targetY)
                            elif targetDist == 0:
                                rightClick(targetX, targetY)
                        while targetID:
                            loot = 1
                            targetID = c.c_ulonglong.from_buffer(readMemory(attack, 0)).value
                            if targetID != 0:
                                targetHP = c.c_int.from_buffer(readMemory(targetID - baseAddress, 0xE8)).value
                                targetY = c.c_int.from_buffer(readMemory(targetID - baseAddress, 0x3C)).value
                                targetX = c.c_int.from_buffer(readMemory(targetID - baseAddress, 0x38)).value
                                if targetRune != 0 and targetHpFrom >= targetHP > targetHpTo:
                                    lock.acquire()
                                    rightClick(bpX[targetRune], bpY[targetRune])
                                    x = targetX - c.c_int.from_buffer(readMemory(myX, 0)).value
                                    y = targetY - c.c_int.from_buffer(readMemory(myY, 0)).value
                                    x = characterX + x * sqmSize
                                    y = characterY + y * sqmSize
                                    leftClick(x, y)
                                    lock.release()
                                    time.sleep(0.9)
                            time.sleep(0.2)
                        if loot and self.startLoot_checkBox.checkState() == 2:
                            x = targetX - c.c_int.from_buffer(readMemory(myX, 0)).value
                            y = targetY - c.c_int.from_buffer(readMemory(myY, 0)).value
                            x = characterX + x * sqmSize
                            y = characterY + y * sqmSize
                            rightClick(x, y)
                            time.sleep(0.3)
                            for itemIndex in range(self.lootList_listWidget.count()):
                                for _ in range(3):
                                    itemName = self.lootList_listWidget.item(itemIndex).text()
                                    itemData = self.lootList_listWidget.item(itemIndex).data(Qt.UserRole)
                                    lootContainer = itemData['Loot']
                                    file_name = [x for x in os.listdir('ItemImages/') if x.split('.')[0] == itemName]
                                    if file_name:
                                        screenshot = wincapLoot.get_screenshot()
                                        if '.png' in file_name[0]:
                                            loadedImage = cv.imread('ItemImages/'f'{itemName}' + '.png')
                                            result = cv.matchTemplate(screenshot, loadedImage, cv.TM_CCOEFF_NORMED)
                                            locations = list(zip(*(np.where(result >= 0.85))[::-1]))
                                            locations = mergeClosePoints(locations, 15)
                                            locations = sorted(locations, key=lambda point: (point[1], point[0]), reverse=True)
                                            locations = [[int(x), int(y)] for x, y in locations]
                                            for x, y in locations:
                                                if lootContainer > -1:
                                                    collectItem(x + screenX[1], y + screenY[1], bpX[lootContainer],
                                                                bpY[lootContainer])
                                                elif lootContainer == -1:
                                                    rightClick(x + screenX[1], y + screenY[1])
                                                elif lootContainer == -2:
                                                    dragDrop(x + screenX[1], y + screenY[1], characterX, characterY)
                                                time.sleep(0.25)
                                        else:
                                            for itemName in os.listdir('ItemImages/' + file_name[0]):
                                                loadedImage = cv.imread('ItemImages/'f'{file_name[0]}''/' + itemName)
                                                result = cv.matchTemplate(screenshot, loadedImage, cv.TM_CCOEFF_NORMED)
                                                locations = list(zip(*(np.where(result >= 0.70))[::-1]))
                                                locations = mergeClosePoints(locations, 15)
                                                locations = sorted(locations, key=lambda point: (point[1], point[0]), reverse=True)
                                                locations = [[int(x), int(y)] for x, y in locations]
                                                for x, y in locations:
                                                    if lootContainer > -1:
                                                        collectItem(x + screenX[1], y + screenY[1], bpX[lootContainer],
                                                                    bpY[lootContainer])
                                                    elif lootContainer == -1:
                                                        rightClick(x + screenX[1], y + screenY[1])
                                                    elif lootContainer == -2:
                                                        dragDrop(x + screenX[1], y + screenY[1], characterX, characterY)
                                                    time.sleep(0.25)
                time.sleep(0.1)
