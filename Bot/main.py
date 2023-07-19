import cv2 as cv
import pytesseract
import numpy as np
from PyQt5.QtWidgets import *
from window_capture import WindowCapture
from funkcje import *
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Wojciech\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"


def get_text(screenshot):
    text = pytesseract.image_to_string(screenshot)
    data = pytesseract.image_to_boxes(screenshot)
    text = text.split(" ")
    blank_text = []
    for i in text:
        i = i.split("\n")
        for s in i:
            if s != '':
                blank_text.append(s)
    new_text = []
    for line in blank_text:
        if line != '':
            new_text.append(line)
    new_data = []
    for line in data.splitlines():
        line = line.split(" ", 3)
        if line[0] != '~':
            new_data.append(line[0:3])
    height = 0
    width = 0
    k = 0
    coordinates = []
    for monster in new_text:
        height = 0
        width = 0
        monster = "".join(monster.split())
        for i in range(k, len(monster)+k):
            height += int(new_data[i][1])
            width += int(new_data[i][2])
        k += len(monster)
        height = int(height/len(monster))
        width = int(width/len(monster))
        coordinates.append(height + 294)
        coordinates.append(1080 - width - 124)
    return coordinates, new_text


app = QApplication([])
main_window = QWidget()
main_window.show()
main_window.setWindowTitle("Gra")
textfield = QLineEdit(main_window)
textfield.setGeometry(100, 100, 300, 30)
textfield.show()


win_cap = WindowCapture('Medivia')

game = win32gui.FindWindow(None, 'Medivia')
while(True):
    img = win_cap.get_screenshot()
    lower = np.array([9, 180, 150])
    upper = np.array([14, 190, 255])
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsv, lower, upper)
    nazwa = textfield.text()
    print(nazwa)
    output = cv.bitwise_and(img, img, mask=mask)
    coordinates, monsters = get_text(output)
    for index, monster in enumerate(monsters):
        if monster == 'Rat':
            Open(coordinates[index*2], coordinates[index*2+1], game)
app.exec()





