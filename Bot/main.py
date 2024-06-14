import time

from Functions import *
from HealingTab import HealingTab
from TrainingTab import SkillTab
from WalkerTab import CaveTab
from TargetLoot import TargetLootTab
from Settings import LootTab
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
        self.setWindowIcon(QIcon('Icon.jpg'))
        self.setFixedSize(410, 500)
        #  Title and Size
        self.setWindowTitle("EasyBot - " + nickname)
        tab = QTabWidget(self)
        tab.addTab(TargetLootTab(), "Target&&Loot")
        tab.addTab(CaveTab(), "Walker")
        tab.addTab(HealingTab(), "Healing")
        #tab.addTab(SkillTab(), "Training")
        tab.addTab(LootTab(), "Settings")
        vbox = QVBoxLayout(self)
        vbox.addWidget(tab)
        self.setLayout(vbox)


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









