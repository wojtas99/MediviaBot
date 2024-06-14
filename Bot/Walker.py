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
        self.waypoint_listWidget = QListWidget(self)
        self.waypointProfile_listWidget = QListWidget(self)
        self.waypointProfile_lineEdit = QLineEdit(self)
        self.actionWaypoint_textEdit = QTextEdit(self)
        self.recordCaveBot_checkBox = QCheckBox("Auto Recording", self)
        self.startCaveBot_checkBox = QCheckBox("Start Walker", self)

        self.waypointOption_comboBox = QComboBox(self)

        self.layout = QGridLayout()
        self.setLayout(self.layout)
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
        pickWaypoint_button = QPushButton("Pick", self)
        actionWaypoint_button = QPushButton("Action", self)
        labelWaypoint_button = QPushButton("Label", self)

        # Line Edits
        self.actionWaypoint_textEdit.setFixedHeight(100)

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
        layout3.addWidget(pickWaypoint_button)
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

        # Add Widgets
        layout1.addWidget(self.startCaveBot_checkBox)
        layout2.addWidget(self.recordCaveBot_checkBox)

        # Add Layouts
        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        self.layout.addWidget(groupbox, 2, 1)

    # Save Waypoints To waypoint_listWidget
    def saveWaypointProfile(self) -> None:
        profile_name = self.waypointProfile_lineEdit.text()
        if profile_name:
            f = open("Waypoints/"f"{profile_name}.txt", "w")
            [f.write(f'{self.waypoint_listWidget.item(i).text()}\n') for i in range(self.waypoint_listWidget.count())]
            f.close()
            self.waypointProfile_listWidget.addItem(profile_name)
            self.waypointProfile_lineEdit.clear()

    # Load Waypoint Profile To waypoint_listWidget
    def loadWaypointProfile(self) -> None:
        self.waypoint_listWidget.clear()
        selected_item = self.waypointProfile_listWidget.currentItem().text()
        if selected_item:
            f = open(
                "Waypoints/"f"{selected_item}.txt")
            for waypoint in f:
                if waypoint != '\n':
                    self.waypoint_listWidget.addItem(waypoint.split("\n")[0])
            f.close()

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
        x = readMemory(myX, 0)
        y = readMemory(myY, 0)
        z = readMemory(myZ, 0)
        x = c.c_int.from_buffer(x).value
        y = c.c_int.from_buffer(y).value
        z = c.c_int.from_buffer(z).value
        self.waypoint_listWidget.addItem('I-X:'f'{x} Y:'f'{y} Z:'f'{z}')
        new_x = x
        new_y = y
        new_z = z
        while self.recordCaveBot_checkBox.checkState():
            x = readMemory(myX, 0)
            y = readMemory(myY, 0)
            z = readMemory(myZ, 0)
            x = c.c_int.from_buffer(x).value
            y = c.c_int.from_buffer(y).value
            z = c.c_int.from_buffer(z).value
            if (x != new_x or y != new_y) and z == new_z:
                self.waypoint_listWidget.addItem('I-X:'f'{x} Y:'f'{y} Z:'f'{z}')
            if z != new_z:
                if y > new_y and x == new_x:
                    self.waypoint_listWidget.addItem('S-X:'f'{x} Y:'f'{y} Z:'f'{z}')
                if y <= new_y and x == new_x:
                    self.waypoint_listWidget.addItem('N-X:'f'{x} Y:'f'{y} Z:'f'{z}')
                if x > new_x:
                    self.waypoint_listWidget.addItem('E-X:'f'{x} Y:'f'{y} Z:'f'{z}')
                if x < new_x:
                    self.waypoint_listWidget.addItem('W-X:'f'{x} Y:'f'{y} Z:'f'{z}')
            new_x = x
            new_y = y
            new_z = z
            time.sleep(0.2)

        # Starts thread that record waypoints
    def startWalker_thread(self) -> None:
        thread = Thread(target=self.followWaypoints)
        thread.daemon = True  # Daemonize the thread to terminate it when the main thread exits
        if self.startCaveBot_checkBox.checkState() == 2:
            thread.start()

    def followWaypoints(self) -> None:
        timer = 0
        i = 0 if self.waypoint_listWidget.currentRow() == -1 else self.waypoint_listWidget.currentRow()
        while i < self.waypoint_listWidget.count() and self.startCaveBot_checkBox.checkState():
            status = self.waypoint_listWidget.item(i).text().split("-")[0]
            numbers = re.sub(r'\D', ' ', self.waypoint_listWidget.item(i).text())
            wpt = [num for num in numbers.split(' ') if num]
            self.waypoint_listWidget.setCurrentRow(i)
            targetID = readMemory(attack, 0)
            targetID = c.c_ulonglong.from_buffer(targetID).value
            while targetID != 0:
                targetID = readMemory(attack, 0)
                targetID = c.c_ulonglong.from_buffer(targetID).value
                time.sleep(2)
            x = readMemory(myX, 0)
            y = readMemory(myY, 0)
            z = readMemory(myZ, 0)
            x = c.c_int.from_buffer(x).value
            y = c.c_int.from_buffer(y).value
            z = c.c_short.from_buffer(z).value
            if x == int(wpt[0]) and y == int(wpt[1]) and z == int(wpt[2]):
                timer = 0
                i += 1
                if i == self.waypoint_listWidget.count() - 1:
                    i = 0
                continue
            if 5 <= timer <= 10:
                leftClick(875 + (int(wpt[0]) - x) * 70, 475 + (int(wpt[1]) - y) * 70)
                timer += 2
                time.sleep(2)
                continue
            if 10 <= timer:
                i += 1
                if i == self.waypoint_listWidget.count() - 1:
                    i = 0
                continue
            if status == 'I':
                stand(wpt[0], wpt[1], wpt[2], x, y, z)
            if status == 'N':
                walkNorth(wpt[0], wpt[1], wpt[2], x, y, z)
            if status == 'S':
                walkSouth(wpt[0], wpt[1], wpt[2], x, y, z)
            if status == 'E':
                walkEast(wpt[0], wpt[1], wpt[2], x, y, z)
            if status == 'W':
                walkWest(wpt[0], wpt[1], wpt[2], x, y, z)
            time.sleep(0.1)
            timer += 0.1
