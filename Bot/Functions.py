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




# Static addresses
myX = 0xBED9A0
myY = 0xBED9A4
myZ = 0xBED9A8
myName = 0xBEC870
attack = 0xBEC920

# Pointers
myStatsPtr = 0x00BEC918
myHPOffset = [0x558]
myHPMAXOffset = [0x560]
myMPOffset = [0x590]
myMPMAXOffset = [0x598]

monstersOnScreenPtr = 0x00C72C50
monstersOnScreenOffset = [0xC80, 0X338, 0X138, 0XFE0, 0X764]

containerPtr = 0x00C6FDD0
containerOffset = [0XE8, 0X2B0, 0X0, 0X1D8, 0XEA8]

# Global variables
screenX = [0] * 2
screenY = [0] * 2
screenWidth = [0] * 2
screenHeight = [0] * 2
bpX = [0] * 12
bpY = [0] * 12

game = win32gui.FindWindow(None, 'Medivia')
lock = threading.Lock()
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


def stand(monster_x, monster_y, monster_z, x, y, z):
    myx = int(monster_x) - x
    myy = int(monster_y) - y
    myz = int(monster_z) - z
    if myy == -1 and myx == 0 and myz == 0:
        win32gui.SendMessage(game, win32con.WM_KEYDOWN, win32con.VK_UP, 0x01480001)
        win32gui.SendMessage(game, win32con.WM_KEYUP, win32con.VK_UP, 0x01480001)
        return
    if myy == 1 and myx == 0 and myz == 0:
        win32gui.SendMessage(game, win32con.WM_KEYDOWN, win32con.VK_DOWN, 0x01500001)
        win32gui.SendMessage(game, win32con.WM_KEYUP, win32con.VK_DOWN, 0x01500001)
        return
    if myx == -1 and myy == 0 and myz == 0:
        win32gui.SendMessage(game, win32con.WM_KEYDOWN, win32con.VK_LEFT, 0x014B0001)
        win32gui.SendMessage(game, win32con.WM_KEYUP, win32con.VK_LEFT, 0x014B0001)
        return
    if myx == 1 and myy == 0 and myz == 0:
        win32gui.SendMessage(game, win32con.WM_KEYDOWN, win32con.VK_RIGHT, 0x014D0001)
        win32gui.SendMessage(game, win32con.WM_KEYUP, win32con.VK_RIGHT, 0x014D0001)
        return


def walkNorth(monster_x, monster_y, monster_z, x, y, z):
    myx = int(monster_x) - x
    myy = int(monster_y) - y
    myz = int(monster_z) - z
    if ((myy == -1 or myy == -2) or (myy == 0 and myx == 0)) and abs(myz) <= 1:
        win32gui.SendMessage(game, win32con.WM_KEYDOWN, win32con.VK_UP, 0x01480001)
        win32gui.SendMessage(game, win32con.WM_KEYUP, win32con.VK_UP, 0x01480001)
        return


def walkSouth(monster_x, monster_y, monster_z, x, y, z):
    myx = int(monster_x) - x
    myy = int(monster_y) - y
    myz = int(monster_z) - z
    if (myy == 1 or myy == 2) and abs(myz) <= 1:
        win32gui.SendMessage(game, win32con.WM_KEYDOWN, win32con.VK_DOWN, 0x01500001)
        win32gui.SendMessage(game, win32con.WM_KEYUP, win32con.VK_DOWN, 0x01500001)
        return


def walkWest(monster_x, monster_y, monster_z, x, y, z):
    myx = int(monster_x) - x
    myy = int(monster_y) - y
    myz = int(monster_z) - z
    if (myx == -1 or myx == -2) and abs(myz) <= 1:
        win32gui.SendMessage(game, win32con.WM_KEYDOWN, win32con.VK_LEFT, 0x014B0001)
        win32gui.SendMessage(game, win32con.WM_KEYUP, win32con.VK_LEFT, 0x014B0001)
        return


def walkEast(monster_x, monster_y, monster_z, x, y, z):
    myx = int(monster_x) - x
    myy = int(monster_y) - y
    myz = int(monster_z) - z
    if (myx == 1 or myx == 2) and abs(myz) <= 1:
        win32gui.SendMessage(game, win32con.WM_KEYDOWN, win32con.VK_RIGHT, 0x014D0001)
        win32gui.SendMessage(game, win32con.WM_KEYUP, win32con.VK_RIGHT, 0x014D0001)
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
    win32gui.PostMessage(game, win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(845, 460))
    win32gui.PostMessage(game, win32con.WM_LBUTTONDOWN, 1, win32api.MAKELONG(845, 460))
    win32gui.PostMessage(game, win32con.WM_LBUTTONUP, 0, win32api.MAKELONG(845, 460))
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




