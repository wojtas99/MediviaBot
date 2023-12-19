from funkcje import *
from healing_tab_class import HealingTab
from skill_tab_class import SkillTab
from cave_tab_class import CaveTab
from target_tab_class import TargetTab


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('Icon.jpg'))
        self.setFixedSize(410, 500)
        #  Title and Size
        self.setWindowTitle("EasyBot - " + nickname)
        tab = QTabWidget(self)
        tab.addTab(TargetTab(), "Monster Targeting")
        tab.addTab(CaveTab(), "CaveBot")
        tab.addTab(HealingTab(), "Healing")
        tab.addTab(SkillTab(), "Skill&&Fishing")
        vbox = QVBoxLayout(self)
        vbox.addWidget(tab)
        self.setLayout(vbox)


def main():
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec()


if __name__ == '__main__':
    main()








