from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import math
import win32gui
import win32con
import win32api
import win32process
import ctypes as c
from PIL import Image, ImageFont, ImageDraw
import threading
from threading import Thread
from window_capture import WindowCapture
import re
import numpy as np
import cv2 as cv
import os
import time
import requests
from win32con import VK_LBUTTON
lock = threading.Lock()
game = win32gui.FindWindow(None, 'Medivia')
procID = win32process.GetWindowThreadProcessId(game)
procID = procID[1]
process_handle = c.windll.kernel32.OpenProcess(0x1F0FFF, False, procID)
modules = win32process.EnumProcessModules(process_handle)
base_adr = modules[0]

attack = 0xDBD828
my_x = 0xDBE5C8
my_y = 0xDBE5CC
my_z = 0xDBE5D0
maxHp = 0X00DBD820
maxHpOffsets = [0X538]
myHpOffsets = [0X530]
myManaOffsets = [0X568]


def read_memory(address_read, offset):
    process_handler = c.windll.kernel32.OpenProcess(0x1F0FFF, False, procID)
    target_adr = address_read + base_adr + offset
    address = c.c_void_p(target_adr)
    size = c.sizeof(c.c_longlong)
    buffer = c.create_string_buffer(size)
    bytes_read = c.c_size_t()
    c.windll.kernel32.ReadProcessMemory(process_handler, address, buffer, size, c.byref(bytes_read))
    c.windll.kernel32.CloseHandle(process_handler)
    return buffer


def read_pointer(address, extra_offset):
    process_handler = c.windll.kernel32.OpenProcess(0x1F0FFF, False, procID)
    target_adr = base_adr + address
    address = c.c_void_p(target_adr)
    size = c.sizeof(c.c_longlong)
    buffer = c.create_string_buffer(size)
    bytes_read = c.c_size_t()
    c.windll.kernel32.ReadProcessMemory(process_handler, address, buffer, size, c.byref(bytes_read))
    for offset in extra_offset:
        address = c.c_ulonglong.from_buffer(buffer).value
        address += offset
        address = c.c_void_p(address)
        c.windll.kernel32.ReadProcessMemory(process_handler, address, buffer, size, c.byref(bytes_read))
    c.windll.kernel32.CloseHandle(process_handler)
    return buffer


def sort_monsters_by_distance(points):
    return math.sqrt((int(points[0])-450)**2 + (int(points[1]) - 450)**2)


def merge_close_points(points, distance_threshold):
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


def go_stand(monster_x, monster_y, monster_z, x, y, z):
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


def go_north(monster_x, monster_y, monster_z, x, y, z):
    myx = int(monster_x) - x
    myy = int(monster_y) - y
    myz = int(monster_z) - z
    if ((myy == -1 or myy == -2) or (myy == 0 and myx == 0)) and abs(myz) <= 1:
        win32gui.SendMessage(game, win32con.WM_KEYDOWN, win32con.VK_UP, 0x01480001)
        win32gui.SendMessage(game, win32con.WM_KEYUP, win32con.VK_UP, 0x01480001)
        return


def go_south(monster_x, monster_y, monster_z, x, y, z):
    myx = int(monster_x) - x
    myy = int(monster_y) - y
    myz = int(monster_z) - z
    if (myy == 1 or myy == 2) and abs(myz) <= 1:
        win32gui.SendMessage(game, win32con.WM_KEYDOWN, win32con.VK_DOWN, 0x01500001)
        win32gui.SendMessage(game, win32con.WM_KEYUP, win32con.VK_DOWN, 0x01500001)
        return


def go_west(monster_x, monster_y, monster_z, x, y, z):
    myx = int(monster_x) - x
    myy = int(monster_y) - y
    myz = int(monster_z) - z
    if (myx == -1 or myx == -2) and abs(myz) <= 1:
        win32gui.SendMessage(game, win32con.WM_KEYDOWN, win32con.VK_LEFT, 0x014B0001)
        win32gui.SendMessage(game, win32con.WM_KEYUP, win32con.VK_LEFT, 0x014B0001)
        return


def go_east(monster_x, monster_y, monster_z, x, y, z):
    myx = int(monster_x) - x
    myy = int(monster_y) - y
    myz = int(monster_z) - z
    if (myx == 1 or myx == 2) and abs(myz) <= 1:
        win32gui.SendMessage(game, win32con.WM_KEYDOWN, win32con.VK_RIGHT, 0x014D0001)
        win32gui.SendMessage(game, win32con.WM_KEYUP, win32con.VK_RIGHT, 0x014D0001)
        return


def collect_items(loot_x, loot_y, bp_x, bp_y):
    win32gui.PostMessage(game, win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(loot_x, loot_y))
    win32gui.PostMessage(game, win32con.WM_LBUTTONDOWN, 1, win32api.MAKELONG(loot_x, loot_y))
    win32gui.PostMessage(game, win32con.WM_MOUSEMOVE, 1, win32api.MAKELONG(bp_x, bp_y))
    win32gui.PostMessage(game, win32con.WM_LBUTTONUP, 0, win32api.MAKELONG(bp_x, bp_y))
    return


def click_right(x, y):
    win32gui.PostMessage(game, win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(x, y))
    win32gui.PostMessage(game, win32con.WM_RBUTTONDOWN, 2, win32api.MAKELONG(x, y))
    win32gui.PostMessage(game, win32con.WM_RBUTTONUP, 0, win32api.MAKELONG(x, y))
    return


def click_left(x, y):
    win32gui.PostMessage(game, win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(x, y))
    win32gui.PostMessage(game, win32con.WM_LBUTTONDOWN, 1, win32api.MAKELONG(x, y))
    win32gui.PostMessage(game, win32con.WM_LBUTTONUP, 0, win32api.MAKELONG(x, y))
    return


def use_on_myself(x, y):
    win32gui.PostMessage(game, win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(x, y))
    win32gui.PostMessage(game, win32con.WM_RBUTTONDOWN, 2, win32api.MAKELONG(x, y))
    win32gui.PostMessage(game, win32con.WM_RBUTTONUP, 0, win32api.MAKELONG(x, y))
    win32gui.PostMessage(game, win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(845, 460))
    win32gui.PostMessage(game, win32con.WM_LBUTTONDOWN, 1, win32api.MAKELONG(845, 460))
    win32gui.PostMessage(game, win32con.WM_LBUTTONUP, 0, win32api.MAKELONG(845, 460))
    return


def press_hotkey(hotkey):
    win32gui.PostMessage(game, win32con.WM_KEYDOWN, 111+hotkey, 0x003B0001)
    win32gui.PostMessage(game, win32con.WM_KEYUP, 111+hotkey, 0x003B0001)
    return


