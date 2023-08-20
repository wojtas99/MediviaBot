import math
import win32gui
import win32con
import win32api
import win32process
import pytesseract
import ctypes as c
from typing import List, Tuple
from PIL import Image
import threading
from PyQt5.QtWidgets import *
from window_capture import WindowCapture
from threading import Thread
import re
from win32con import VK_LBUTTON
import numpy as np
import cv2 as cv
import os
import time
from PyQt5.QtGui import QMovie
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Wojciech\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

lock = threading.Lock()


def collect_items(loot_x, loot_y, bp_x, bp_y, hwnd):
    win32gui.PostMessage(hwnd, win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(loot_x, loot_y))
    win32gui.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, 1, win32api.MAKELONG(loot_x, loot_y))
    win32gui.PostMessage(hwnd, win32con.WM_MOUSEMOVE, 1, win32api.MAKELONG(bp_x, bp_y))
    win32gui.PostMessage(hwnd, win32con.WM_LBUTTONUP, 0, win32api.MAKELONG(bp_x, bp_y))
    win32gui.PostMessage(hwnd, win32con.WM_RBUTTONDOWN, 2, win32api.MAKELONG(bp_x, bp_y))
    win32gui.PostMessage(hwnd, win32con.WM_RBUTTONUP, 0, win32api.MAKELONG(bp_x, bp_y))
    return


def drop_items(loot_x, loot_y, hwnd):
    win32gui.PostMessage(hwnd, win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(loot_x, loot_y))
    win32gui.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, 1, win32api.MAKELONG(loot_x, loot_y))
    win32gui.PostMessage(hwnd, win32con.WM_MOUSEMOVE, 1, win32api.MAKELONG(845, 468))
    win32gui.PostMessage(hwnd, win32con.WM_LBUTTONUP, 0, win32api.MAKELONG(845, 468))


def click_right(x, y, hwnd):
    win32gui.PostMessage(hwnd, win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(x, y))
    win32gui.PostMessage(hwnd, win32con.WM_RBUTTONDOWN, 2, win32api.MAKELONG(x, y))
    win32gui.PostMessage(hwnd, win32con.WM_RBUTTONUP, 0, win32api.MAKELONG(x, y))
    return


def click_left(x, y, hwnd):
    win32gui.PostMessage(hwnd, win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(x, y))
    win32gui.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, 1, win32api.MAKELONG(x, y))
    win32gui.PostMessage(hwnd, win32con.WM_LBUTTONUP, 0, win32api.MAKELONG(x, y))
    return


def read_memory(address_read, base_adr, offset, proc_id):
    process_handle = c.windll.kernel32.OpenProcess(0x1F0FFF, False, proc_id)
    target_adr = address_read + base_adr + offset
    address = c.c_void_p(target_adr)
    size = c.sizeof(c.c_longlong)
    buffer = c.create_string_buffer(size)
    bytes_read = c.c_size_t()
    c.windll.kernel32.ReadProcessMemory(process_handle, address, buffer, size, c.byref(bytes_read))
    c.windll.kernel32.CloseHandle(process_handle)
    return buffer


def get_text(screenshot):
    data = pytesseract.image_to_boxes(screenshot)
    new_data = []
    for line in data.splitlines():
        line = line.split(" ", 3)
        if line[0] != '~':
            new_data.append(line[0:3])
    monster = []
    monsters = []
    height = 0
    width = 0
    counter = 0
    for i in range(0, len(new_data)-1):
        if abs(int(new_data[i+1][1]) - int(new_data[i][1])) < 20 and abs(int(new_data[i + 1][2]) - int(new_data[i][2])) < 20:
            monster.append(new_data[i][0])
            width += int(new_data[i][1])
            height += int(new_data[i][2])
            counter += 1
            if i == len(new_data) - 2:
                monster.append(new_data[i + 1][0])
                monsters.append("".join(monster))
                height = int(height / counter)
                width = int(width / counter)
                monsters.append(width)
                monsters.append(height)
        else:
            monster.append(new_data[i][0])
            monsters.append("".join(monster))
            if counter != 0:
                height = int(height / counter)
                width = int(width / counter)
            counter = 0
            monsters.append(width)
            monsters.append(height)
            width = 0
            height = 0
            monster.clear()
    merged = []
    for i in range(0, len(monsters) - 2, 3):
        tmp = [monsters[i], monsters[i + 1], monsters[i + 2]]
        merged.append(tmp)
    return merged
'''
def get_text(screenshot):
    text = pytesseract.image_to_string(screenshot)
    data = pytesseract.image_to_boxes(screenshot)
    text = text.split(" ")
    blank_text = []
    for i in text:
        i = i.split("\n")
        for s in i:
            if s != '' and len(s) >= 3:
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
    k = 0
    coordinates = []
    for monster in new_text:
        monster = "".join(monster.split())
        height = int(new_data[int(len(monster)/2) + k][1])
        width = int(new_data[int(len(monster)/2) + k][2])
        k += len(monster)
        coordinates.append(height + 290)
        coordinates.append(1080 - width - 128)
    print(coordinates)
    print(new_text)
    return coordinates, new_text
'''


def distance(points):
    return math.sqrt((int(points[1])-450)**2 + (int(points[2]) - 450)**2)


def read_offsets(address, extra_offset, hwnd):
    procID = win32process.GetWindowThreadProcessId(hwnd)
    procID = procID[1]
    process_handler = c.windll.kernel32.OpenProcess(0x1F0FFF, False, procID)
    modules = win32process.EnumProcessModules(process_handler)
    moduleBase = modules[0]
    target_adr = moduleBase + address
    address = c.c_void_p(target_adr)
    size = c.sizeof(c.c_longlong)
    buffer = c.create_string_buffer(size)
    bytes_read = c.c_size_t()
    c.windll.kernel32.ReadProcessMemory(process_handler, address, buffer, size, c.byref(bytes_read))
    value = c.c_longlong.from_buffer(buffer).value
    target_adr = value + extra_offset
    c.windll.kernel32.CloseHandle(process_handler)
    return target_adr


def merge_close_points(points: List[Tuple[float, float]], threshold: float = 0.5) -> List[Tuple[int, int]]:
    merged_points = []
    merged_indices = set()
    for i in range(len(points)):
        if i in merged_indices:
            continue
        x1, y1 = points[i]
        merged_x, merged_y = x1, y1
        count = 1
        for j in range(i + 1, len(points)):
            if j in merged_indices:
                continue
            x2, y2 = points[j]
            dist = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
            if dist < threshold:
                merged_x += x2
                merged_y += y2
                count += 1
                merged_indices.add(j)
        merged_x /= count
        merged_y /= count
        merged_points.append((int(merged_x), int(merged_y)))
    return merged_points


def find_rectangle(result, monster, threshold=0.5):
    locations = np.where(result >= threshold)
    locations = list(zip(*locations[::-1]))
    rectangles = []
    for loc in locations:
        rect = [int(loc[0]), int(loc[1]), monster.shape[1], monster.shape[0]]
        rectangles.append(rect)
    return rectangles


def find_points(rectangles):
    points = []
    for (x, y, w, h) in rectangles:
        center_x = x + int(w / 2)
        center_y = y + int(h / 2)
        points.append((center_x, center_y))
    return points


