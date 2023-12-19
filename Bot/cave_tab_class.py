from funkcje import *


class CaveTab(QWidget):
    def __init__(self):
        super().__init__()

        # Variables
        self.waypointProfile_listWidget = None
        self.waypointProfile_line = None
        self.recordCaveBot_checkBox = None
        self.startCaveBot_checkBox = None
        self.waypoint_listWidget = None

        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.groupbox1()
        self.groupbox2()
        self.groupbox3()

    def groupbox1(self) -> None:
        groupbox = QGroupBox("Save&&Load Waypoints")
        groupbox_layout = QVBoxLayout()
        groupbox.setLayout(groupbox_layout)

        # Buttons
        saveWaypointProfile_button = QPushButton("Save")
        saveWaypointProfile_button.clicked.connect(self.saveWaypointProfile)

        loadWaypointProfile_button = QPushButton("Load")
        loadWaypointProfile_button.clicked.connect(self.loadWaypointProfile)

        # Labels
        waypointProfile_label = QLabel("Name:", self)

        # Edit Lines
        self.waypointProfile_line = QLineEdit()

        # List Widgets
        self.waypointProfile_listWidget = QListWidget(self)
        for file in os.listdir("Waypoints"):
            self.waypointProfile_listWidget.addItem(f"{file.split('.')[0]}")

        # QHBox
        layout1 = QHBoxLayout()
        layout1.addWidget(waypointProfile_label)
        layout1.addWidget(self.waypointProfile_line)
        layout2 = QHBoxLayout()
        layout2.addWidget(saveWaypointProfile_button)
        layout2.addWidget(loadWaypointProfile_button)

        # Add Layouts
        groupbox_layout.addWidget(self.waypointProfile_listWidget)
        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        groupbox.setFixedWidth(150)
        self.layout.addWidget(groupbox, 1, 0, alignment=Qt.AlignTop | Qt.AlignLeft)

    def groupbox2(self) -> None:
        groupbox = QGroupBox("Waypoints")
        groupbox_layout = QVBoxLayout()
        groupbox.setLayout(groupbox_layout)

        # Buttons
        deleteWaypoint_button = QPushButton("Del", self)
        deleteWaypoint_button.clicked.connect(self.deleteWaypoint)

        clearWaypointList_button = QPushButton("Clear", self)
        clearWaypointList_button.clicked.connect(self.clearWaypointList)

        # List Widgets
        self.waypoint_listWidget = QListWidget(self)

        # QHBox
        layout1 = QHBoxLayout()
        layout1.addWidget(deleteWaypoint_button)
        layout1.addWidget(clearWaypointList_button)

        # Add Layouts
        groupbox_layout.addWidget(self.waypoint_listWidget)
        groupbox_layout.addLayout(layout1)
        groupbox.setFixedSize(175, 250)
        self.layout.addWidget(groupbox, 0, 0, alignment=Qt.AlignTop | Qt.AlignLeft)

    def groupbox3(self) -> None:
        groupbox = QGroupBox("Add Waypoints")
        groupbox_layout = QVBoxLayout()
        groupbox.setLayout(groupbox_layout)

        # Buttons
        addWaypointStand_button = QPushButton("Stand", self)

        addWaypointNorth_button = QPushButton("North", self)

        addWaypointSouth_button = QPushButton("South", self)

        addWaypointEast_button = QPushButton("East", self)

        addWaypointWest_button = QPushButton("West", self)

        addWaypointAction_button = QPushButton("Action", self)

        addWaypointLadder_button = QPushButton("Ladder", self)

        addWaypointShovel_button = QPushButton("Shovel", self)

        addWaypointLure_button = QPushButton("Ladder", self)

        # Check Boxes
        self.startCaveBot_checkBox = QCheckBox(self)
        self.startCaveBot_checkBox.setFixedWidth(15)
        self.startCaveBot_checkBox.stateChanged.connect(self.startWalker_thread)
        self.recordCaveBot_checkBox = QCheckBox(self)
        self.recordCaveBot_checkBox.setFixedWidth(15)
        self.recordCaveBot_checkBox.stateChanged.connect(self.startRecord_thread)

        # Labels
        startCaveBot_label = QLabel("Follow Waypoints", self)
        recordCaveBot_label = QLabel("Auto Recording", self)

        # QHBox
        layout1 = QHBoxLayout()
        layout1.addWidget(addWaypointStand_button)
        layout1.addWidget(addWaypointNorth_button)
        layout1.addWidget(addWaypointAction_button)
        layout2 = QHBoxLayout()
        layout2.addWidget(addWaypointWest_button)
        layout2.addWidget(addWaypointSouth_button)
        layout2.addWidget(addWaypointEast_button)
        layout3 = QHBoxLayout()
        layout3.addWidget(addWaypointLadder_button)
        layout3.addWidget(addWaypointShovel_button)
        layout3.addWidget(addWaypointLure_button)
        layout4 = QHBoxLayout()
        layout4.addWidget(self.recordCaveBot_checkBox)
        layout4.addWidget(recordCaveBot_label)
        layout5 = QHBoxLayout()
        layout5.addWidget(self.startCaveBot_checkBox)
        layout5.addWidget(startCaveBot_label)

        # Add Layouts
        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        groupbox_layout.addLayout(layout3)
        groupbox_layout.addLayout(layout4)
        groupbox_layout.addLayout(layout5)
        groupbox.setFixedWidth(200)
        self.layout.addWidget(groupbox, 0, 1, alignment=Qt.AlignTop | Qt.AlignLeft)

    # Save Waypoints To waypoint_listWidget
    def saveWaypointProfile(self) -> None:
        profile_name = self.waypointProfile_line.text()
        if profile_name:
            f = open("Waypoints/"f"{profile_name}.txt", "w")
            [f.write(f'{self.waypoint_listWidget.item(i).text()}\n') for i in range(self.waypoint_listWidget.count())]
            f.close()
            self.waypointProfile_listWidget.addItem(profile_name)
            self.waypointProfile_line.clear()

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
    def deleteWaypoint(self) -> None:
        print("xd")

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
        x = read_memory(my_x, 0)
        y = read_memory(my_y, 0)
        z = read_memory(my_z, 0)
        x = c.c_int.from_buffer(x).value
        y = c.c_int.from_buffer(y).value
        z = c.c_int.from_buffer(z).value
        self.waypoint_listWidget.addItem('I-X:'f'{x} Y:'f'{y} Z:'f'{z}')
        new_x = x
        new_y = y
        new_z = z
        while self.recordCaveBot_checkBox.checkState():
            x = read_memory(my_x, 0)
            y = read_memory(my_y, 0)
            z = read_memory(my_z, 0)
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
            targetID = read_memory(attack, 0)
            targetID = c.c_ulonglong.from_buffer(targetID).value
            while targetID != 0:
                targetID = read_memory(attack, 0)
                targetID = c.c_ulonglong.from_buffer(targetID).value
                time.sleep(2)
            x = read_memory(my_x, 0)
            y = read_memory(my_y, 0)
            z = read_memory(my_z, 0)
            x = c.c_int.from_buffer(x).value
            y = c.c_int.from_buffer(y).value
            z = c.c_int.from_buffer(z).value
            if x == int(wpt[0]) and y == int(wpt[1]) and z == int(wpt[2]):
                timer = 0
                i += 1
                if i == self.waypoint_listWidget.count() - 1:
                    i = 0
                continue
            if 5 <= timer <= 10:
                click_left(875 + (int(wpt[0]) - x)*70, 475 + (int(wpt[1]) - y)*70)
                timer += 2
                time.sleep(2)
                continue
            if 10 <= timer:
                i += 1
                if i == self.waypoint_listWidget.count() - 1:
                    i = 0
                continue
            if status == 'I':
                go_stand(wpt[0], wpt[1], wpt[2], x, y, z)
            if status == 'N':
                go_north(wpt[0], wpt[1], wpt[2], x, y, z)
            if status == 'S':
                go_south(wpt[0], wpt[1], wpt[2], x, y, z)
            if status == 'E':
                go_east(wpt[0], wpt[1], wpt[2], x, y, z)
            if status == 'W':
                go_west(wpt[0], wpt[1], wpt[2], x, y, z)
            time.sleep(0.1)
            timer += 0.1
