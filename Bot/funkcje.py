
import win32con, win32gui,win32api
def Collect(loot_x, loot_y, hwnd):
    win32gui.PostMessage(hwnd, win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(loot_x, loot_y))
    win32gui.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, 1, win32api.MAKELONG(loot_x, loot_y))
    win32gui.PostMessage(hwnd, win32con.WM_MOUSEMOVE, 1, win32api.MAKELONG(1681, 505))
    win32gui.PostMessage(hwnd, win32con.WM_LBUTTONUP, 0, win32api.MAKELONG(1681, 505))
    win32gui.PostMessage(hwnd, win32con.WM_RBUTTONDOWN, 2, win32api.MAKELONG(1681, 505))
    win32gui.PostMessage(hwnd, win32con.WM_RBUTTONUP, 0, win32api.MAKELONG(1681, 505))
    return
def CollectItems(loot_x, loot_y, hwnd):
    win32gui.PostMessage(hwnd, win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(loot_x, loot_y))
    win32gui.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, 1, win32api.MAKELONG(loot_x, loot_y))
    win32gui.PostMessage(hwnd, win32con.WM_MOUSEMOVE, 1, win32api.MAKELONG(1681, 555))
    win32gui.PostMessage(hwnd, win32con.WM_LBUTTONUP, 0, win32api.MAKELONG(1681, 555))
    win32gui.PostMessage(hwnd, win32con.WM_RBUTTONDOWN, 2, win32api.MAKELONG(1681, 555))
    win32gui.PostMessage(hwnd, win32con.WM_RBUTTONUP, 0, win32api.MAKELONG(1681, 555))
    return
def Open(loot_x, loot_y, hwnd):
    win32gui.PostMessage(hwnd, win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(loot_x, loot_y))
    win32gui.PostMessage(hwnd, win32con.WM_RBUTTONDOWN, 2, win32api.MAKELONG(loot_x, loot_y))
    win32gui.PostMessage(hwnd, win32con.WM_RBUTTONUP, 0, win32api.MAKELONG(loot_x, loot_y))
    return
def Drop(loot_x, loot_y, hwnd):
    win32gui.PostMessage(hwnd, win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(loot_x, loot_y))
    win32gui.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, 1, win32api.MAKELONG(loot_x, loot_y))
    win32gui.PostMessage(hwnd, win32con.WM_MOUSEMOVE, 1, win32api.MAKELONG(845, 468))
    win32gui.PostMessage(hwnd, win32con.WM_LBUTTONUP, 0, win32api.MAKELONG(845, 468))
