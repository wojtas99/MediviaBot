import time

from funkcje import *


class CaveTab(QWidget):
    def __init__(self):
        super().__init__()

        self.waypoints_list = QListWidget(self)
        self.waypoints_list.setGeometry(0, 20, 170, 200)

        label_text = QLabel("Waypoints", self)
        label_text.setGeometry(0, 0, 100, 20)

        self.save_wpt_list = QListWidget(self)
        self.save_wpt_list.setGeometry(300, 320, 120, 80)
        for file in os.listdir("Waypoints"):
            self.save_wpt_list.addItem(f"{file.split('.')[0]}")

        self.save_wpt_text = QLabel("Name", self)
        self.save_wpt_text.setGeometry(301, 400, 100, 20)

        self.save_wpt_textfield = QLineEdit(self)
        self.save_wpt_textfield.setGeometry(335, 401, 85, 20)

        self.save_wpt_button = QPushButton("Save", self)
        self.save_wpt_button.setGeometry(334, 421, 41, 20)
        self.save_wpt_button.clicked.connect(self.save_waypoints_list)

        self.load_wpt_button = QPushButton("Load", self)
        self.load_wpt_button.setGeometry(380, 421, 41, 20)
        self.load_wpt_button.clicked.connect(self.load_waypoints_list)

        self.delete_wpt_button = QPushButton("Del", self)
        self.delete_wpt_button.setGeometry(299, 421, 31, 20)
        self.delete_wpt_button.clicked.connect(self.delete_list)

        left = QPushButton("<", self)
        left.setGeometry(0, 220, 30, 25)
        right = QPushButton(">", self)
        right.setGeometry(31, 220, 30, 25)

        del_waypoint = QPushButton("Del", self)
        del_waypoint.setGeometry(111, 220, 40, 25)
        del_waypoint.clicked.connect(self.delete_wpt_item)

        clear_waypoint = QPushButton("Clear", self)
        clear_waypoint.setGeometry(66, 220, 40, 25)
        clear_waypoint.clicked.connect(self.clear_wpt_list)

        cave_status = QCheckBox(self)
        cave_status.move(0, 260)
        cave_status_text = QLabel("Follow Waypoints", self)
        cave_status_text.setGeometry(17, 251, 100, 30)

        stand = QPushButton("Stand", self)
        stand.setGeometry(200, 20, 40, 25)
        stand.clicked.connect(self.stand_add)

        north = QPushButton("North", self)
        north.setGeometry(241, 20, 40, 25)
        north.clicked.connect(self.north_add)

        action = QPushButton("Action", self)
        action.setGeometry(282, 20, 40, 25)

        south = QPushButton("South", self)
        south.setGeometry(241, 46, 40, 25)
        south.clicked.connect(self.south_add)

        west = QPushButton("West", self)
        west.setGeometry(200, 46, 40, 25)

        east = QPushButton("East", self)
        east.setGeometry(282, 46, 40, 25)

        auto_rec_label = QLabel("Auto Recording", self)
        auto_rec_label.setGeometry(17, 281, 100, 30)
        auto_rec_box = QCheckBox(self)
        auto_rec_box.move(0, 290)

        def auto_rec_thread():
            thread = Thread(target=auto_rec)
            thread.daemon = True  # Daemonize the thread to terminate it when the main thread exits
            if auto_rec_box.checkState() == 2:
                thread.start()

        auto_rec_box.stateChanged.connect(auto_rec_thread)

        def follow_wpt_thread():
            thread = Thread(target=follow_wpt)
            thread.daemon = True  # Daemonize the thread to terminate it when the main thread exits
            if cave_status.checkState() == 2:
                thread.start()

        cave_status.stateChanged.connect(follow_wpt_thread)

        def auto_rec():
            x = read_memory(my_x, 0)
            y = read_memory(my_y, 0)
            z = read_memory(my_z, 0)
            x = c.c_int.from_buffer(x).value
            y = c.c_int.from_buffer(y).value
            z = c.c_int.from_buffer(z).value
            self.waypoints_list.addItem('I-X:'f'{x} Y:'f'{y} Z:'f'{z}')
            new_x = x
            new_y = y
            new_z = z
            while auto_rec_box.checkState():
                x = read_memory(my_x, 0)
                y = read_memory(my_y, 0)
                z = read_memory(my_z, 0)
                x = c.c_int.from_buffer(x).value
                y = c.c_int.from_buffer(y).value
                z = c.c_int.from_buffer(z).value
                if (x != new_x or y != new_y) and z == new_z:
                    self.waypoints_list.addItem('I-X:'f'{x} Y:'f'{y} Z:'f'{z}')
                if z != new_z:
                    if y > new_y and x == new_x:
                        self.waypoints_list.addItem('S-X:'f'{x} Y:'f'{y} Z:'f'{z}')
                    if y <= new_y and x == new_x:
                        self.waypoints_list.addItem('N-X:'f'{x} Y:'f'{y} Z:'f'{z}')
                    if x > new_x:
                        self.waypoints_list.addItem('E-X:'f'{x} Y:'f'{y} Z:'f'{z}')
                    if x < new_x:
                        self.waypoints_list.addItem('W-X:'f'{x} Y:'f'{y} Z:'f'{z}')
                new_x = x
                new_y = y
                new_z = z
                time.sleep(0.2)

        def follow_wpt():
            timer = 0
            waypoint_count = self.waypoints_list.count()
            while cave_status.checkState():
                i = 0
                while i < waypoint_count:
                    status = self.waypoints_list.item(i).text().split("-")[0]
                    numbers = re.sub(r'\D', ' ', self.waypoints_list.item(i).text())
                    wpt = [num for num in numbers.split(' ') if num]
                    self.waypoints_list.setCurrentRow(i)
                    i += 1
                    while cave_status.checkState():
                        targetID = read_memory(attack, 0)
                        targetID = c.c_ulonglong.from_buffer(targetID).value
                        while targetID != 0:
                            targetID = read_memory(attack, 0)
                            targetID = c.c_ulonglong.from_buffer(targetID).value
                            time.sleep(2)
                        time.sleep(0.1)
                        x = read_memory(my_x, 0)
                        y = read_memory(my_y, 0)
                        z = read_memory(my_z, 0)
                        x = c.c_int.from_buffer(x).value
                        y = c.c_int.from_buffer(y).value
                        z = c.c_int.from_buffer(z).value
                        if x == int(wpt[0]) and y == int(wpt[1]) and z == int(wpt[2]):
                            timer = 0
                            break
                        else:
                            timer += 1
                            if timer > 50:
                                for k in range(0, self.waypoints_list.count()):
                                    i = k
                                    numbers = re.sub(r'\D', ' ', self.waypoints_list.item(i).text())
                                    wpt = [num for num in numbers.split(' ') if num]
                                    self.waypoints_list.setCurrentRow(i)
                                    x = read_memory(my_x, 0)
                                    y = read_memory(my_y, 0)
                                    z = read_memory(my_z, 0)
                                    x = c.c_int.from_buffer(x).value
                                    y = c.c_int.from_buffer(y).value
                                    z = c.c_int.from_buffer(z).value
                                    if (abs(x - int(wpt[0])) <= 4) and (abs(y - int(wpt[1]))) <= 4 and z == int(wpt[2]):
                                        myx = int(wpt[0]) - x
                                        myy = int(wpt[1]) - y
                                        myx = 875 + myx * 70
                                        myy = 475 + myy * 70
                                        click_left(myx, myy)
                                        timer = 0
                                        time.sleep(5)
                                        break
                                    time.sleep(0.1)
                            if 20 <= timer < 50:
                                myx = int(wpt[0]) - x
                                myy = int(wpt[1]) - y
                                myx = 875 + myx * 70
                                myy = 475 + myy * 70
                                click_left(myx, myy)
                                timer += 20
                                time.sleep(3)
                            if status == 'I':
                                go_stand(wpt[0], wpt[1], wpt[2], x, y, z)
                                continue
                            if status == 'N':
                                go_north(wpt[0], wpt[1], wpt[2], x, y, z)
                                continue
                            if status == 'S':
                                go_south(wpt[0], wpt[1], wpt[2], x, y, z)
                                continue
                            if status == 'E':
                                go_east(wpt[0], wpt[1], wpt[2], x, y, z)
                                continue
                            if status == 'W':
                                go_west(wpt[0], wpt[1], wpt[2], x, y, z)
                                continue

    def delete_wpt_item(self):
        selected_item = self.waypoints_list.currentItem()
        if selected_item:
            self.waypoints_list.takeItem(self.waypoints_list.row(selected_item))

    def clear_wpt_list(self):
        self.waypoints_list.clear()

    def delete_list(self):
        selected_item = self.save_wpt_list.currentItem()
        if selected_item:
            os.remove(
                'Waypoints/'f'{self.save_wpt_list.item(self.save_wpt_list.row(selected_item)).text()}.txt')
            self.save_wpt_list.takeItem(self.save_wpt_list.row(selected_item))

    def save_waypoints_list(self):
        if self.save_wpt_textfield.text() != '':
            f = open("Waypoints/"f"{self.save_wpt_textfield.text()}.txt", "w")
            self.save_wpt_list.addItem(f'{self.save_wpt_textfield.text()}')
            self.save_wpt_textfield.clear()
            for i in range(self.waypoints_list.count()):
                f.write(f'{self.waypoints_list.item(i).text()}\n')
            f.close()

    def load_waypoints_list(self):
        self.waypoints_list.clear()
        selected_item = self.save_wpt_list.currentItem()
        if selected_item:
            f = open(
                "Waypoints/"f"{self.save_wpt_list.item(self.save_wpt_list.row(selected_item)).text()}.txt")
            for wpt in f:
                if wpt != '\n':
                    self.waypoints_list.addItem(wpt.split('\n')[0])
            f.close()

    def stand_add(self):
        x = read_memory(my_x, 0)
        y = read_memory(my_y, 0)
        z = read_memory(my_z, 0)
        x = c.c_int.from_buffer(x).value
        y = c.c_int.from_buffer(y).value
        z = c.c_int.from_buffer(z).value
        self.waypoints_list.addItem('I-X:'f'{x} Y:'f'{y} Z:'f'{z}')

    def north_add(self):
        x = read_memory(my_x, 0)
        y = read_memory(my_y, 0)
        z = read_memory(my_z, 0)
        x = c.c_int.from_buffer(x).value
        y = c.c_int.from_buffer(y).value
        z = c.c_int.from_buffer(z).value
        self.waypoints_list.addItem('N-X:'f'{x} Y:'f'{y} Z:'f'{z}')

    def south_add(self):
        x = read_memory(my_x, 0)
        y = read_memory(my_y, 0)
        z = read_memory(my_z, 0)
        x = c.c_int.from_buffer(x).value
        y = c.c_int.from_buffer(y).value
        z = c.c_int.from_buffer(z).value
        self.waypoints_list.addItem('S-X:'f'{x} Y:'f'{y} Z:'f'{z}')
