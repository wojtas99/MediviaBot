import math

import win32gui
import win32con
import win32api
import win32process
import pytesseract
import ctypes as c
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Wojciech\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"


def collect(loot_x, loot_y, hwnd):
    win32gui.PostMessage(hwnd, win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(loot_x, loot_y))
    win32gui.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, 1, win32api.MAKELONG(loot_x, loot_y))
    win32gui.PostMessage(hwnd, win32con.WM_MOUSEMOVE, 1, win32api.MAKELONG(1681, 505))
    win32gui.PostMessage(hwnd, win32con.WM_LBUTTONUP, 0, win32api.MAKELONG(1681, 505))
    win32gui.PostMessage(hwnd, win32con.WM_RBUTTONDOWN, 2, win32api.MAKELONG(1681, 505))
    win32gui.PostMessage(hwnd, win32con.WM_RBUTTONUP, 0, win32api.MAKELONG(1681, 505))
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
    k = 0
    coordinates = []
    for monster in new_text:
        height = 0
        width = 0
        monster = "".join(monster.split())
        for i in range(k, len(monster) + k):
            height += int(new_data[i][1])
            width += int(new_data[i][2])
        k += len(monster)
        height = int(height/len(monster))
        width = int(width/len(monster))
        coordinates.append(height + 324)
        coordinates.append(1080 - width - 112)
    return coordinates, new_text


def distance(points):
    return math.sqrt((points[0]-900)**2 + (points[1] - 450)**2)


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

