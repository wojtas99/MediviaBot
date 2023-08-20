from funkcje import *
from rune_tab_class import RuneTab
from cave_tab_class import CaveTab
from target_tab_class import TargetTab
from loot_tab_class import LootTab


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(500, 500)
        #  Title and Size
        self.setWindowTitle("EasyBot")
        tab = QTabWidget(self)
        tab.addTab(TargetTab(), "Monster Targeting")
        tab.addTab(CaveTab(), "CaveBot")
        tab.addTab(RuneTab(), "RuneMaker")
        tab.addTab(LootTab(), "Loot")
        vbox = QVBoxLayout(self)
        vbox.addWidget(tab)
        self.setLayout(vbox)











