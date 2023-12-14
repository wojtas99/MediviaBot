from funkcje import *
from healing_tab_class import HealingTab
from rune_tab_class import RuneTab
from cave_tab_class import CaveTab
from target_tab_class import TargetTab
from loot_tab_class import LootTab


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('Icon.jpg'))
        self.resize(400, 500)
        #  Title and Size
        self.setWindowTitle("EasyBot")
        tab = QTabWidget(self)
        tab.addTab(TargetTab(), "Monster Targeting")
        tab.addTab(CaveTab(), "CaveBot")
        tab.addTab(HealingTab(), "Healing")
        tab.addTab(LootTab(), "Loot")
        tab.addTab(RuneTab(), "RuneMaker")
        vbox = QVBoxLayout(self)
        vbox.addWidget(tab)
        self.setLayout(vbox)











