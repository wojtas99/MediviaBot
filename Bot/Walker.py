import json
import time

from Functions import *


class WalkerTab(QWidget):
    def __init__(self):
        super().__init__()
        # Load Icon
        self.setWindowIcon(QIcon('Icon.jpg'))

        # Set Title and Size
        self.setWindowTitle("Walker")
        self.setFixedSize(350, 350)
        # Variables
        # List Widgets
        self.waypoint_listWidget = QListWidget(self)
        self.waypointProfile_listWidget = QListWidget(self)

        # Line/Text Edits
        self.waypointProfile_lineEdit = QLineEdit(self)
        self.actionWaypoint_textEdit = QTextEdit(self)

        # Check Boxes
        self.recordCaveBot_checkBox = QCheckBox("Auto Recording", self)
        self.startCaveBot_checkBox = QCheckBox("Start Walker", self)

        # Combo Boxes
        self.waypointOption_comboBox = QComboBox(self)

        # Layouts
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        # Initialize
        self.saveLoadWaypoints()
        self.waypointList()
        self.addWaypoins()
        self.startWalker()

    def saveLoadWaypoints(self) -> None:
        groupbox = QGroupBox("Save&&Load")
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Buttons
        saveWaypointProfile_button = QPushButton("Save")
        saveWaypointProfile_button.clicked.connect(self.saveWaypointProfile)

        loadWaypointProfile_button = QPushButton("Load")
        loadWaypointProfile_button.clicked.connect(self.loadWaypointProfile)

        # List Widgets
        for file in os.listdir("Waypoints"):
            self.waypointProfile_listWidget.addItem(f"{file.split('.')[0]}")

        # QHBox
        layout1 = QHBoxLayout(self)
        layout2 = QHBoxLayout(self)

        # Add Widgets
        layout1.addWidget(QLabel("Name:", self))
        layout1.addWidget(self.waypointProfile_lineEdit)
        layout2.addWidget(saveWaypointProfile_button)
        layout2.addWidget(loadWaypointProfile_button)

        # Add Layouts
        groupbox_layout.addWidget(self.waypointProfile_listWidget)
        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        self.layout.addWidget(groupbox, 2, 0)

    def waypointList(self) -> None:
        groupbox = QGroupBox("Waypoints")
        groupbox_layout = QVBoxLayout()
        groupbox.setLayout(groupbox_layout)

        # Buttons
        deleteWaypoint_button = QPushButton("Del", self)
        deleteWaypoint_button.clicked.connect(self.deleteWaypoint)

        clearWaypointList_button = QPushButton("Clear", self)
        clearWaypointList_button.clicked.connect(self.clearWaypointList)

        # Buttons Functions

        # List Widgets Functions
        self.waypoint_listWidget.currentItemChanged.connect(self.checkWaypoint)

        # QHBox
        layout1 = QHBoxLayout()
        layout1.addWidget(deleteWaypoint_button)
        layout1.addWidget(clearWaypointList_button)

        # Add Layouts
        groupbox_layout.addWidget(self.waypoint_listWidget)
        groupbox_layout.addLayout(layout1)
        self.layout.addWidget(groupbox, 0, 0, 1, 1)

    def addWaypoins(self) -> None:
        groupbox = QGroupBox("Add Waypoints")
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Combo Boxes
        self.waypointOption_comboBox.addItem("Center")
        self.waypointOption_comboBox.addItem("North")
        self.waypointOption_comboBox.addItem("South")
        self.waypointOption_comboBox.addItem("East")
        self.waypointOption_comboBox.addItem("West")
        self.waypointOption_comboBox.addItem("North-East")
        self.waypointOption_comboBox.addItem("North-West")
        self.waypointOption_comboBox.addItem("South-East")
        self.waypointOption_comboBox.addItem("South-West")

        # Buttons
        standWaypoint_button = QPushButton("Stand", self)
        ropeWaypoint_button = QPushButton("Rope", self)
        shovelWaypoint_button = QPushButton("Shovel", self)
        ladderWaypoint_button = QPushButton("Ladder", self)
        actionWaypoint_button = QPushButton("Action", self)
        labelWaypoint_button = QPushButton("Label", self)

        # Button Functions
        standWaypoint_button.clicked.connect(lambda: self.addWaypoint(0))
        ropeWaypoint_button.clicked.connect(lambda: self.addWaypoint(1))
        shovelWaypoint_button.clicked.connect(lambda: self.addWaypoint(2))
        ladderWaypoint_button.clicked.connect(lambda: self.addWaypoint(3))
        actionWaypoint_button.clicked.connect(lambda: self.addWaypoint(4))
        labelWaypoint_button.clicked.connect(lambda: self.addWaypoint(5))

        # Line Edits
        self.actionWaypoint_textEdit.setFixedHeight(50)

        # QHBox
        layout1 = QHBoxLayout(self)
        layout2 = QHBoxLayout(self)
        layout3 = QHBoxLayout(self)
        layout4 = QHBoxLayout(self)

        # Add Widgets
        layout1.addWidget(self.waypointOption_comboBox)
        layout2.addWidget(standWaypoint_button)
        layout2.addWidget(actionWaypoint_button)
        layout2.addWidget(labelWaypoint_button)
        layout3.addWidget(ropeWaypoint_button)
        layout3.addWidget(shovelWaypoint_button)
        layout3.addWidget(ladderWaypoint_button)
        layout4.addWidget(self.actionWaypoint_textEdit)

        # Add Layouts
        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        groupbox_layout.addLayout(layout3)
        groupbox_layout.addLayout(layout4)

        self.layout.addWidget(groupbox, 0, 1, 2, 1)

    def startWalker(self) -> None:
        groupbox = QGroupBox("Start")
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # QHBox
        layout1 = QHBoxLayout(self)
        layout2 = QHBoxLayout(self)

        # Check Boxes
        self.startCaveBot_checkBox.stateChanged.connect(self.startWalker_thread)
        self.recordCaveBot_checkBox.stateChanged.connect(self.startRecord_thread)

        # Add Widgets
        layout1.addWidget(self.startCaveBot_checkBox)
        layout2.addWidget(self.recordCaveBot_checkBox)

        # Add Layouts
        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        self.layout.addWidget(groupbox, 2, 1)

    # Save Waypoints To waypoint_listWidget
    def saveWaypointProfile(self) -> None:
        waypointName = self.waypointProfile_lineEdit.text()
        for index in range(self.waypointProfile_listWidget.count()):
            if waypointName.upper() == self.waypointProfile_listWidget.item(index).text().upper():
                return
        if waypointName:
            waypointList = []
            for i in range(self.waypoint_listWidget.count()):
                item = self.waypoint_listWidget.item(i)
                itemName = item.text()
                itemData = item.data(Qt.UserRole)
                waypointList.append({"name": itemName, "data": itemData})
            with open(f"Waypoints/{waypointName}.json", "w") as f:
                json.dump(waypointList, f, indent=4)
            self.waypointProfile_listWidget.addItem(waypointName)
            self.waypointProfile_lineEdit.clear()

    # Load Waypoint Profile To waypoint_listWidget
    def loadWaypointProfile(self) -> None:
        waypointName = self.waypointProfile_listWidget.currentItem().text()
        if waypointName:
            with open(f"Waypoints/{waypointName}.json", "r") as f:
                waypointList = json.load(f)
                self.waypoint_listWidget.clear()
                for entry in waypointList:
                    itemName = entry["name"]
                    itemData = entry["data"]
                    waypoint = QListWidgetItem(itemName)
                    waypoint.setData(Qt.UserRole, itemData)
                    self.waypoint_listWidget.addItem(waypoint)

    # Check Waypoints
    def checkWaypoint(self):
        waypoint = self.waypoint_listWidget.item(self.waypoint_listWidget.currentRow()).data(Qt.UserRole)
        if waypoint['Action'] > 3:
            self.actionWaypoint_textEdit.setText(waypoint['Direction'])
        else:
            self.actionWaypoint_textEdit.clear()

    # Add Waypoints
    def addWaypoint(self, index):
        if index == 0:  # Stand
            x = c.c_int.from_buffer(readMemory(myXAddress, 0)).value
            y = c.c_int.from_buffer(readMemory(myYAddress, 0)).value
            z = c.c_short.from_buffer(readMemory(myZAddress, 0)).value
            waypointData = {"Action": 0,
                            'Direction': self.waypointOption_comboBox.currentIndex(),
                            'X': x, 'Y': y, 'Z': z}
            waypoint = QListWidgetItem(f'Stand: {x} {y} {z}')
            waypoint.setData(Qt.UserRole, waypointData)
            self.waypoint_listWidget.addItem(waypoint)
        elif index == 1:  # Rope
            x = c.c_int.from_buffer(readMemory(myXAddress, 0)).value
            y = c.c_int.from_buffer(readMemory(myYAddress, 0)).value
            z = c.c_short.from_buffer(readMemory(myZAddress, 0)).value
            waypointData = {"Action": 1,
                            'Direction': self.waypointOption_comboBox.currentIndex(),
                            'X': x, 'Y': y, 'Z': z}
            waypoint = QListWidgetItem(f'Rope: {x} {y} {z}')
            waypoint.setData(Qt.UserRole, waypointData)
            self.waypoint_listWidget.addItem(waypoint)
        elif index == 2:  # Shovel
            x = c.c_int.from_buffer(readMemory(myXAddress, 0)).value
            y = c.c_int.from_buffer(readMemory(myYAddress, 0)).value
            z = c.c_short.from_buffer(readMemory(myZAddress, 0)).value
            waypointData = {"Action": 2,
                            'Direction': self.waypointOption_comboBox.currentIndex(),
                            'X': x, 'Y': y, 'Z': z}
            waypoint = QListWidgetItem(f'Shovel: {x} {y} {z}')
            waypoint.setData(Qt.UserRole, waypointData)
            self.waypoint_listWidget.addItem(waypoint)
        elif index == 3:  # Ladder
            x = c.c_int.from_buffer(readMemory(myXAddress, 0)).value
            y = c.c_int.from_buffer(readMemory(myYAddress, 0)).value
            z = c.c_short.from_buffer(readMemory(myZAddress, 0)).value
            waypointData = {"Action": 3,
                            'Direction': self.waypointOption_comboBox.currentIndex(),
                            'X': x, 'Y': y, 'Z': z}
            waypoint = QListWidgetItem(f'Ladder: {x} {y} {z}')
            waypoint.setData(Qt.UserRole, waypointData)
            self.waypoint_listWidget.addItem(waypoint)
        elif index == 4:  # Action
            x = c.c_int.from_buffer(readMemory(myXAddress, 0)).value
            y = c.c_int.from_buffer(readMemory(myYAddress, 0)).value
            z = c.c_short.from_buffer(readMemory(myZAddress, 0)).value
            actionText = self.actionWaypoint_textEdit.document().toRawText()
            if actionText:
                waypointData = {"Action": 4,
                                'Direction': actionText,
                                'X': x, 'Y': y, 'Z': z}
                waypoint = QListWidgetItem(f'Action: {x} {y} {z}')
                waypoint.setData(Qt.UserRole, waypointData)
                self.waypoint_listWidget.addItem(waypoint)
                self.actionWaypoint_textEdit.clear()
        elif index == 5:  # Label
            x = c.c_int.from_buffer(readMemory(myXAddress, 0)).value
            y = c.c_int.from_buffer(readMemory(myYAddress, 0)).value
            z = c.c_short.from_buffer(readMemory(myZAddress, 0)).value
            labelName = self.actionWaypoint_textEdit.document().toRawText()
            if labelName:
                waypointData = {"Action": 5,
                                'Direction': labelName,
                                'X': x, 'Y': y, 'Z': z}
                waypoint = QListWidgetItem(f'{labelName}')
                waypoint.setData(Qt.UserRole, waypointData)
                self.waypoint_listWidget.addItem(waypoint)
                self.actionWaypoint_textEdit.clear()

    # Delete Selected Waypoint from waypoint_listWidget
    def deleteWaypoint(self, index) -> None:
        self.waypoint_listWidget.takeItem(index)

    # Clear all Waypoints from waypoint_listWidget
    def clearWaypointList(self) -> None:
        self.waypoint_listWidget.clear()

    # Starts thread that record waypoints
    def startRecord_thread(self) -> None:
        thread = Thread(target=self.recordWaypoints)
        thread.daemon = True  # Daemonize the thread to terminate it when the main thread exits
        if self.recordCaveBot_checkBox.checkState() == 2:
            thread.start()

    # Thread that record our waypoints
    def recordWaypoints(self) -> None:
        myX = c.c_int.from_buffer(readMemory(myXAddress, 0)).value
        myY = c.c_int.from_buffer(readMemory(myYAddress, 0)).value
        myZ = c.c_short.from_buffer(readMemory(myZAddress, 0)).value
        waypointData = {"Action": 0,
                        'Direction': 0,
                        'X': myX, 'Y': myY, 'Z': myZ}
        waypoint = QListWidgetItem(f'Stand: {myX} {myY} {myZ}')
        waypoint.setData(Qt.UserRole, waypointData)
        self.waypoint_listWidget.addItem(waypoint)
        oldX = myX
        oldY = myY
        oldZ = myZ
        while self.recordCaveBot_checkBox.checkState():
            myX = c.c_int.from_buffer(readMemory(myXAddress, 0)).value
            myY = c.c_int.from_buffer(readMemory(myYAddress, 0)).value
            myZ = c.c_short.from_buffer(readMemory(myZAddress, 0)).value
            if (myX != oldX or myY != oldY) and myZ == oldZ:
                waypointData = {"Action": 0,
                                'Direction': 0,
                                'X': myX, 'Y': myY, 'Z': myZ}
                waypoint = QListWidgetItem(f'Stand: {myX} {myY} {myZ}')
                waypoint.setData(Qt.UserRole, waypointData)
                self.waypoint_listWidget.addItem(waypoint)
            if myZ != oldZ:
                if myX < oldX:
                    waypointData = {"Action": 0,
                                    'Direction': 4,
                                    'X': myX, 'Y': myY, 'Z': myZ}
                    waypoint = QListWidgetItem(f'Stand: {myX} {myY} {myZ}')
                    waypoint.setData(Qt.UserRole, waypointData)
                    self.waypoint_listWidget.addItem(waypoint)
                elif myX > oldX:
                    waypointData = {"Action": 0,
                                    'Direction': 3,
                                    'X': myX, 'Y': myY, 'Z': myZ}
                    waypoint = QListWidgetItem(f'Stand: {myX} {myY} {myZ}')
                    waypoint.setData(Qt.UserRole, waypointData)
                    self.waypoint_listWidget.addItem(waypoint)
                elif myY > oldY:
                    waypointData = {"Action": 0,
                                    'Direction': 2,
                                    'X': myX, 'Y': myY, 'Z': myZ}
                    waypoint = QListWidgetItem(f'Stand: {myX} {myY} {myZ}')
                    waypoint.setData(Qt.UserRole, waypointData)
                    self.waypoint_listWidget.addItem(waypoint)
                else:
                    waypointData = {"Action": 0,
                                    'Direction': 1,
                                    'X': myX, 'Y': myY, 'Z': myZ}
                    waypoint = QListWidgetItem(f'Stand: {myX} {myY} {myZ}')
                    waypoint.setData(Qt.UserRole, waypointData)
                    self.waypoint_listWidget.addItem(waypoint)
            oldX = myX
            oldY = myY
            oldZ = myZ
            time.sleep(0.02)

    def startWalker_thread(self) -> None:
        thread = Thread(target=self.followWaypoints)
        thread.daemon = True  # Daemonize the thread to terminate it when the main thread exits
        if self.startCaveBot_checkBox.checkState() == 2:
            thread.start()

    def followWaypoints(self) -> None:
        currentWpt = self.waypoint_listWidget.currentRow()
        if currentWpt == -1:
            currentWpt = 0
        timer = 0
        while self.startCaveBot_checkBox.checkState():
            self.waypoint_listWidget.setCurrentRow(currentWpt)
            wptData = self.waypoint_listWidget.item(currentWpt).data(Qt.UserRole)
            wptAction = wptData['Action']
            wptDirection = wptData['Direction']
            mapX = wptData['X']
            mapY = wptData['Y']
            mapZ = wptData['Z']
            myX = c.c_int.from_buffer(readMemory(myXAddress, 0)).value
            myY = c.c_int.from_buffer(readMemory(myYAddress, 0)).value
            myZ = c.c_short.from_buffer(readMemory(myZAddress, 0)).value
            if myX == mapX and myY == mapY and myZ == mapZ and wptAction == 0:
                timer = 0
                currentWpt += 1
                if currentWpt == self.waypoint_listWidget.count():
                    currentWpt = 0
                time.sleep(0.1)
                continue
            if not lock.locked():
                if wptAction == 0:
                    walk(wptDirection, myX, myY, myZ, mapX, mapY, mapZ)
                elif wptAction == 3:
                    time.sleep(0.5)
                    rightClick(coordinatesX[0], coordinatesY[0])  # Click On Ladder
                    currentWpt += 1
            time.sleep(0.1)
            if not lock.locked():
                timer += 0.1
            if timer > 10:  # Search for the nearest wpt
                for index in range(self.waypoint_listWidget.count()):
                    self.waypoint_listWidget.setCurrentRow(index)
                    wptData = self.waypoint_listWidget.item(index).data(Qt.UserRole)
                    mapX = wptData['X']
                    mapY = wptData['Y']
                    mapZ = wptData['Z']
                    myX = c.c_int.from_buffer(readMemory(myXAddress, 0)).value
                    myY = c.c_int.from_buffer(readMemory(myYAddress, 0)).value
                    myZ = c.c_short.from_buffer(readMemory(myZAddress, 0)).value
                    if myZ == mapZ and abs(mapX - myX) < 4 and abs(mapY - myY) < 4:
                        currentWpt = index
                        timer = 0
                        leftClick(coordinatesX[0] + (mapX - myX) * 75, coordinatesY[0] + (mapY - myY) * 75)
                        time.sleep(5)
                        break
                    time.sleep(0.1)
            if timer > 5:
                leftClick(coordinatesX[0] + (mapX - myX) * 75, coordinatesY[0] + (mapY - myY) * 75)
                time.sleep(5)
                timer += 5
