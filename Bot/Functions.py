from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import math
import win32api, win32process, win32con, win32gui, win32ui
import ctypes as c
from PIL import Image, ImageFont, ImageDraw
import threading
from threading import Thread
import re
import cv2 as cv
import numpy as np
import os
import time
import requests
from win32con import VK_LBUTTON

# Keystrokes codes
lParam = [0X00480001, 0x00500001, 0X004D0001, 0X004B0001,  # 8, 2, 6, 4
          0X00490001, 0X00470001, 0X00510001, 0X004F0001]  # 9, 7, 3, 1


# Static addresses
myXAddress = 0xBED9A0
myYAddress = 0xBED9A4
myZAddress = 0xBED9A8
myName = 0xBEC870
attack = 0xBEC920

# Pointers
myStatsPtr = 0x00BEC918
myHPOffset = [0x558]
myHPMAXOffset = [0x560]
myMPOffset = [0x590]
myMPMAXOffset = [0x598]

monstersOnScreenPtr = 0x00BECA58
monstersOnScreenOffset = [0x858, 0xE0, 0XF68, 0X4F8, 0XE64]

containerPtr = 0x00C6FDD0
containerOffset = [0XE8, 0X2B0, 0X0, 0X1D8, 0XEA8]

# Global variables
screenX = [0] * 1
screenY = [0] * 1
screenWidth = [0] * 1
screenHeight = [0] * 1
coordinatesX = [0] * 11
coordinatesY = [0] * 11

game = win32gui.FindWindow(None, 'Medivia')
lock = threading.Lock()
testy = threading.Lock()
procID = win32process.GetWindowThreadProcessId(game)
procID = procID[1]
processHandle = c.windll.kernel32.OpenProcess(0x1F0FFF, False, procID)
modules = win32process.EnumProcessModules(processHandle)
baseAddress = modules[0]


def readMemory(address_read, offset):
    target_adr = address_read + baseAddress + offset
    address = c.c_void_p(target_adr)
    buffer = c.create_string_buffer(256)
    bytes_read = c.c_size_t()
    c.windll.kernel32.ReadProcessMemory(processHandle, address, buffer, 256, c.byref(bytes_read))
    return buffer


def readPointer(address, extra_offset):
    target_adr = baseAddress + address
    address = c.c_void_p(target_adr)
    buffer = c.create_string_buffer(256)
    bytes_read = c.c_size_t()
    c.windll.kernel32.ReadProcessMemory(processHandle, address, buffer, 256, c.byref(bytes_read))
    for offset in extra_offset:
        address = c.c_ulonglong.from_buffer(buffer).value
        address += offset
        address = c.c_void_p(address)
        c.windll.kernel32.ReadProcessMemory(processHandle, address, buffer, 256, c.byref(bytes_read))
    return buffer


nickname = readMemory(myName, 0)
nickname = nickname.value
nickname = nickname.decode('utf-8')
#win32gui.SetWindowText(game, "Medivia - " + nickname)


def sortMonstersByDist(point, characterX, characterY):
    return math.sqrt((point[0] - characterX) ** 2 + (point[1] - characterY) ** 2)


def mergeClosePoints(points, distance_threshold):
    merged_points = []
    merged_indices = set()

    def merge_distance(point1, point2):
        return np.sqrt(np.sum((point1 - point2)**2))
    for i in range(len(points)):
        if i not in merged_indices:
            current_point = points[i]
            merged_point = np.array(current_point)
            for j in range(i + 1, len(points)):
                if merge_distance(np.array(current_point), np.array(points[j])) < distance_threshold:
                    merged_point = (merged_point + np.array(points[j])) / 2
                    merged_indices.add(j)
            merged_points.append(tuple(merged_point))
    return merged_points


def walk(wptDirection, myX, myY, myZ, mapX, mapY, mapZ) -> None:
    x = mapX - myX
    y = mapY - myY
    z = mapZ - myZ
    if wptDirection != 0:
        if wptDirection == 1 and ((-2 <= y < 0) or (y == 0 == x)) and abs(z) <= 1:  # Walk North
            win32gui.PostMessage(game, win32con.WM_KEYDOWN, 0, lParam[0])
            win32gui.PostMessage(game, win32con.WM_KEYUP, 0, lParam[0])
            return
        if wptDirection == 2 and 0 < y <= 2 and abs(z) <= 1:  # Walk South
            win32gui.PostMessage(game, win32con.WM_KEYDOWN, 0, lParam[1])
            win32gui.PostMessage(game, win32con.WM_KEYUP, 0, lParam[1])
            return
        if wptDirection == 3 and 0 < x <= 2 and abs(z) <= 1:  # Walk East
            win32gui.PostMessage(game, win32con.WM_KEYDOWN, 0, lParam[2])
            win32gui.PostMessage(game, win32con.WM_KEYUP, 0, lParam[2])
            return
        if wptDirection == 4 and -2 <= x < 0 and abs(z) <= 1:  # Walk West
            win32gui.PostMessage(game, win32con.WM_KEYDOWN, 0, lParam[3])
            win32gui.PostMessage(game, win32con.WM_KEYUP, 0, lParam[3])
            return
    else:
        if x == 1 and y == 0 and z == 0:  # Walk East
            win32gui.PostMessage(game, win32con.WM_KEYDOWN, 0, lParam[2])
            win32gui.PostMessage(game, win32con.WM_KEYUP, 0, lParam[2])
            return
        if x == -1 and y == 0 and z == 0:  # Walk West
            win32gui.PostMessage(game, win32con.WM_KEYDOWN, 0, lParam[3])
            win32gui.PostMessage(game, win32con.WM_KEYUP, 0, lParam[3])
            return
        if x == 0 and y == 1 and z == 0:  # Walk South
            win32gui.PostMessage(game, win32con.WM_KEYDOWN, 0, lParam[1])
            win32gui.PostMessage(game, win32con.WM_KEYUP, 0, lParam[1])
            return
        if x == 0 and y == -1 and z == 0:  # Walk North
            win32gui.PostMessage(game, win32con.WM_KEYDOWN, 0, lParam[0])
            win32gui.PostMessage(game, win32con.WM_KEYUP, 0, lParam[0])
            return


def collectItem(loot_x, loot_y, bp_x, bp_y):
    win32gui.PostMessage(game, win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(loot_x, loot_y))
    win32gui.PostMessage(game, win32con.WM_LBUTTONDOWN, 1, win32api.MAKELONG(loot_x, loot_y))
    win32gui.PostMessage(game, win32con.WM_MOUSEMOVE, 1, win32api.MAKELONG(bp_x, bp_y))
    win32gui.PostMessage(game, win32con.WM_LBUTTONUP, 0, win32api.MAKELONG(bp_x, bp_y))
    win32gui.PostMessage(game, win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(bp_x, bp_y))
    win32gui.PostMessage(game, win32con.WM_RBUTTONDOWN, 2, win32api.MAKELONG(bp_x, bp_y))
    win32gui.PostMessage(game, win32con.WM_RBUTTONUP, 0, win32api.MAKELONG(bp_x, bp_y))
    return


def rightClick(x, y):
    win32gui.PostMessage(game, win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(x, y))
    win32gui.PostMessage(game, win32con.WM_RBUTTONDOWN, 2, win32api.MAKELONG(x, y))
    win32gui.PostMessage(game, win32con.WM_RBUTTONUP, 0, win32api.MAKELONG(x, y))
    return


def leftClick(x, y):
    win32gui.PostMessage(game, win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(x, y))
    win32gui.PostMessage(game, win32con.WM_LBUTTONDOWN, 1, win32api.MAKELONG(x, y))
    win32gui.PostMessage(game, win32con.WM_LBUTTONUP, 0, win32api.MAKELONG(x, y))
    return


def dragDrop(x, y, characterX, characterY):
    win32gui.PostMessage(game, win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(x, y))
    win32gui.PostMessage(game, win32con.WM_LBUTTONDOWN, 1, win32api.MAKELONG(x, y))
    win32gui.PostMessage(game, win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(characterX, characterY))
    win32gui.PostMessage(game, win32con.WM_LBUTTONUP, 0, win32api.MAKELONG(characterX, characterY))
    return


def useOnMe(x, y):
    win32gui.PostMessage(game, win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(x, y))
    win32gui.PostMessage(game, win32con.WM_RBUTTONDOWN, 2, win32api.MAKELONG(x, y))
    win32gui.PostMessage(game, win32con.WM_RBUTTONUP, 0, win32api.MAKELONG(x, y))
    win32gui.PostMessage(game, win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(coordinatesX[0], coordinatesY[0]))
    win32gui.PostMessage(game, win32con.WM_LBUTTONDOWN, 1, win32api.MAKELONG(coordinatesX[0], coordinatesY[0]))
    win32gui.PostMessage(game, win32con.WM_LBUTTONUP, 0, win32api.MAKELONG(coordinatesX[0], coordinatesY[0]))
    return


def pressHotkey(hotkey):
    win32gui.PostMessage(game, win32con.WM_KEYDOWN, 111+hotkey, 0x003B0001)
    win32gui.PostMessage(game, win32con.WM_KEYUP, 111+hotkey, 0x003B0001)
    return


def antyIdle():
    win32gui.PostMessage(game, win32con.WM_KEYDOWN, win32con.VK_CONTROL, 0x011D0001)
    win32gui.SendMessage(game, win32con.WM_KEYDOWN, win32con.VK_RIGHT, 0x014D0001)
    win32gui.SendMessage(game, win32con.WM_KEYUP, win32con.VK_RIGHT, 0x014D0001)
    time.sleep(0.2)
    win32gui.SendMessage(game, win32con.WM_KEYDOWN, win32con.VK_LEFT, 0x014B0001)
    win32gui.SendMessage(game, win32con.WM_KEYUP, win32con.VK_LEFT, 0x014B0001)
    time.sleep(0.2)
    win32gui.SendMessage(game, win32con.WM_KEYDOWN, win32con.VK_RIGHT, 0x014D0001)
    win32gui.SendMessage(game, win32con.WM_KEYUP, win32con.VK_RIGHT, 0x014D0001)
    time.sleep(0.2)
    win32gui.SendMessage(game, win32con.WM_KEYDOWN, win32con.VK_LEFT, 0x014B0001)
    win32gui.SendMessage(game, win32con.WM_KEYUP, win32con.VK_LEFT, 0x014B0001)
    win32gui.PostMessage(game, win32con.WM_KEYUP, win32con.VK_CONTROL, 0xC11D0001)


class WindowCapture:
    w = 0
    h = 0
    hwnd = None

    def __init__(self, window_name, w, h, x, y):
        self.hwnd = win32gui.FindWindow(None, window_name)
        if not self.hwnd:
            raise Exception('Window not found: {}'.format(window_name))
        self.w = w
        self.h = h
        self.x = x
        self.y = y

    def get_screenshot(self):
        # get the window image data
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (self.w, self.h), dcObj, (self.x, self.y), win32con.SRCCOPY)
        # convert the raw data into a format opencv can read
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (self.h, self.w, 4)
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())
        img = img[..., :3]
        img = np.ascontiguousarray(img)
        return img




