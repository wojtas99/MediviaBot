import cv2 as cv
import numpy as np
from PyQt5.QtWidgets import *
from window_capture import WindowCapture
from funkcje import *
from PyQt5.QtCore import QTimer
from main_window_class import MainWindow
from threading import Thread


def main():
    win_cap = WindowCapture('Medivia')
    game = win32gui.FindWindow(None, 'Medivia')
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()

    def list_monsters():
        while True:
            img = win_cap.get_screenshot()
            lower = np.array([9, 180, 150])
            upper = np.array([14, 190, 255])
            hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
            mask = cv.inRange(hsv, lower, upper)
            output = cv.bitwise_and(img, img, mask=mask)
            coordinates, monsters = get_text(output)
            print(monsters)
            for index, monster in enumerate(monsters):
                if monster == 'Rat':
                    use(coordinates[index * 2], coordinates[index * 2 + 1], game)

    monster_thread = Thread(target=list_monsters)
    monster_thread.daemon = True  # Daemonize the thread to terminate it when the main thread exits
    monster_thread.start()
    app.exec()


if __name__ == '__main__':
    main()






