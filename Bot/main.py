import time

from Functions import *
from HealingTab import HealingTab
from TrainingTab import SkillTab
from Walker import WalkerTab
from TargetLoot import TargetLootTab
from Settings import SettingsTab
import urllib
from urllib import request
from PIL import ImageSequence


def add_Items_from_URL() -> None:
    tmp = 0
    with open('Loot.txt', 'r') as f:
        for item in f:
            item = item.strip()
            name = item.split('/')[-1]
            name = name.replace("_", " ")
            if name in os.listdir('ItemImages/'):
                continue
            urllib.request.urlretrieve(item, f'ItemImages/{name}')
            gif = Image.open(f'ItemImages/{name}')
            if gif.format == 'GIF':
                frames_dir = f'ItemImages/{name.split(".gif")[0]}'
                os.makedirs(frames_dir, exist_ok=True)
                for i, frame in enumerate(ImageSequence.Iterator(gif)):
                    frame = frame.convert('RGBA')
                    background = Image.open('background.png').convert('RGBA')
                    background.paste(frame, (0, 0), frame)
                    background.save(f'{frames_dir}/{name.split(".gif")[0]}{i}.png')
                gif.close()
                os.remove(f'ItemImages/{name}')
            else:
                image1 = Image.open(f'ItemImages/{name}').convert('RGBA')
                image2 = Image.open('background.png').convert('RGBA')
                image2.paste(image1, (0, 0), image1)
                image2.save(f'ItemImages/{name}')


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        # Load Icon
        self.setWindowIcon(QIcon('Icon.jpg'))

        # Set Title and Size
        self.setFixedSize(400, 100)
        #self.setWindowTitle("EasyBot - " + nickname)

        # Instances
        self.targetLootTab_instance = None
        self.walkerTab_instance = None
        self.healingTab_instance = None
        self.settingsTab_instance = None

        # Layout
        self.layout = QGridLayout(self)
        self.setLayout(self.layout)

        # Buttons
        self.targetLootTab_button = QPushButton('Targeting', self)
        self.walkerTab_button = QPushButton('Walker', self)
        self.healingTab_button = QPushButton('Healing', self)
        self.settingsTab_button = QPushButton('Settings', self)

        # Buttons Functions
        self.targetLootTab_button.clicked.connect(self.targetLoot)
        self.walkerTab_button.clicked.connect(self.walker)
        self.healingTab_button.clicked.connect(self.healing)
        self.settingsTab_button.clicked.connect(self.settings)

        # Add Widgets
        self.layout.addWidget(self.walkerTab_button, 0, 0)
        self.layout.addWidget(self.targetLootTab_button, 1, 0)
        self.layout.addWidget(self.healingTab_button, 0, 1)
        self.layout.addWidget(self.settingsTab_button, 1, 1)

    def settings(self):
        if self.settingsTab_instance is None:
            self.settingsTab_instance = SettingsTab()
        self.settingsTab_instance.show()

    def walker(self):
        if self.walkerTab_instance is None:
            self.walkerTab_instance = WalkerTab()
        self.walkerTab_instance.show()

    def targetLoot(self):
        if self.targetLootTab_instance is None:
            self.targetLootTab_instance = TargetLootTab()
        self.targetLootTab_instance.show()

    def healing(self):
        if self.healingTab_instance is None:
            self.healingTab_instance = HealingTab()
        self.healingTab_instance.show()


def main():
    os.makedirs("Targeting", exist_ok=True)
    os.makedirs("Looting", exist_ok=True)
    os.makedirs("TargetImages", exist_ok=True)
    os.makedirs("Settings", exist_ok=True)
    os.makedirs("Waypoints", exist_ok=True)
    os.makedirs("ItemImages", exist_ok=True)
    add_Items_from_URL()
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec()
    win32gui.SetWindowText(game, "Medivia")


if __name__ == '__main__':
    main()










