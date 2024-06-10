from Functions import *
from HealingTab import HealingTab
from TrainingTab import SkillTab
from WalkerTab import CaveTab
from GeneralTab import GeneralTab
from SettingsTab import LootTab
import urllib
from urllib import request


def add_Items_from_URL() -> None:
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


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('Icon.jpg'))
        self.setFixedSize(410, 500)
        #  Title and Size
        self.setWindowTitle("EasyBot - " + nickname)
        tab = QTabWidget(self)
        tab.addTab(GeneralTab(), "Target&&Loot")
        tab.addTab(CaveTab(), "Walker")
        tab.addTab(HealingTab(), "Healing&&Attack")
        #tab.addTab(SkillTab(), "Training")
        tab.addTab(LootTab(), "Settings")
        vbox = QVBoxLayout(self)
        vbox.addWidget(tab)
        self.setLayout(vbox)


def main():
    add_Items_from_URL()
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec()
    win32gui.SetWindowText(game, "Medivia")


if __name__ == '__main__':
    main()









